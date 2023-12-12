from datetime import datetime, timedelta
import os
import re
import requests
import tempfile
from zipfile import ZipFile


def update_rockbox(mount_point: str) -> None:
    rockbox_info = os.path.join(mount_point, ".rockbox", "rockbox-info.txt")

    build_info = requests.get("https://www.rockbox.org/dl.cgi?bin=ipod6g").text
    if not build_info or datetime.today().strftime("%Y-%m-%d") not in build_info:
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        build_info = requests.get(
            f"https://www.rockbox.org/dl.cgi?bin=ipod6g&date={yesterday}"
        ).text

    latest_svn = max(re.findall(r"[a-z0-9]{7}", build_info))
    current_svn = open(rockbox_info).read().split("Version:")[1][:7].strip()

    print(f"\nLatest Rockbox SVN Revision: {latest_svn}")
    print(f"Current Rockbox SVN Revision: {current_svn}\n")

    if current_svn and latest_svn:
        if current_svn != latest_svn:
            print("Updating iPod rockbox to the latest revision...")
            dl_url = "http://download.rockbox.org/daily/ipod6g/rockbox-ipod6g.zip"
            zip_name = os.path.basename(dl_url)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_zip_path = os.path.join(temp_dir, zip_name)
                with open(temp_zip_path, "wb") as f:
                    f.write(requests.get(dl_url).content)

                with ZipFile(temp_zip_path, "r") as zip_ref:
                    zip_ref.extractall(mount_point)

            print("OK\n")
        else:
            print("Rockbox is already up to date.\n")


if __name__ == "__main__":
    import typer

    typer.run(update_rockbox)
