from bs4 import BeautifulSoup
import os
import re
import requests
import tempfile
from zipfile import ZipFile


def update_rockbox(mount_point: str) -> None:
    rockbox_info = os.path.join(mount_point, ".rockbox", "rockbox-info.txt")

    build_info = (
        BeautifulSoup(
            requests.get(
                "https://www.rockbox.org/dl.cgi?bin=ipod6g",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
                },
            ).content,
            features="html.parser",
        )
        .find("table", class_="rockbox")
        .find_all("tr")[1]
        .find_all("td")[1]
        .find("a")
        .text
    )

    latest_svn = re.findall(r"[a-z0-9]{10}", build_info)[0]
    detected_device = None
    current_svn = None
    with open(rockbox_info, "r") as rockbox_info_file:
        rockbox_info_file_contents = rockbox_info_file.read()
        detected_device = (
            rockbox_info_file_contents.split("Target:")[1].split("\n")[0].strip()
        )
        current_svn = rockbox_info_file_contents.split("Version:")[1][:11].strip()

    print(f"\nDetected Device: {detected_device}")
    print(f"Latest Rockbox SVN Revision: {latest_svn}")
    print(f"Current Rockbox SVN Revision: {current_svn}\n")

    if current_svn and latest_svn:
        if current_svn != latest_svn:
            print("Updating iPod rockbox to the latest revision...")
            dl_url = f"http://download.rockbox.org/daily/{detected_device}/rockbox-{detected_device}.zip"
            zip_name = os.path.basename(dl_url)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_zip_path = os.path.join(temp_dir, zip_name)
                with open(temp_zip_path, "wb") as f:
                    f.write(
                        requests.get(
                            dl_url,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
                            },
                        ).content
                    )

                with ZipFile(temp_zip_path, "r") as zip_ref:
                    zip_ref.extractall(mount_point)

            print("OK\n")
        else:
            print("Rockbox is already up to date.\n")


if __name__ == "__main__":
    import typer

    typer.run(update_rockbox)
