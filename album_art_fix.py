import os
import shutil
import subprocess
import sys
import tempfile
from PIL import Image, UnidentifiedImageError
from mutagen import File

SUPPORTED_EXTENSIONS = (".mp3", ".flac")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
COVER_FILENAME = "cover.jpg"
TEMP_FOLDER_NAME = "cover_extraction_temp"


def sanitize_filename(filename: str):
    return "".join(
        c if c.isalnum() or c in [".", "_", "-", " "] else "_" for c in filename
    )


def get_album_tag(file_path: str):
    try:
        if file_path.endswith(SUPPORTED_EXTENSIONS):
            album_tag = File(file_path, easy=True)["album"]
            return album_tag[0] if isinstance(album_tag, list) else album_tag
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
        return None


def handle_audio_files(directory: str, temp_folder: str):
    audio_files = [
        file for file in os.listdir(directory) if file.endswith(SUPPORTED_EXTENSIONS)
    ]
    if audio_files:
        audio_file_path = os.path.join(directory, audio_files[0])
        temp_folder_path = os.path.join(temp_folder, TEMP_FOLDER_NAME)

        try:
            os.makedirs(temp_folder_path, exist_ok=True)

            encoding = sys.stdout.encoding or "utf-8"
            temp_cover_path = os.path.join(temp_folder_path, COVER_FILENAME)
            print(f"Running ffmpeg command for '{audio_file_path}'")
            result = subprocess.run(
                ["ffmpeg", "-i", audio_file_path, temp_cover_path],
                text=True,
                capture_output=True,
                encoding=encoding,
                check=False,
            )

            print(f"\nffmpeg command output: {result.stdout}")
            print(f"ffmpeg command error: {result.stderr}")

            if result.returncode == 0:
                cover_dest_path = os.path.join(directory, COVER_FILENAME)
                shutil.move(temp_cover_path, cover_dest_path)
                print(
                    f"Cover image extracted and saved as baseline JPEG in {directory}"
                )
        except Exception as e:
            print(f"Error during extraction: {e}")
        finally:
            pass


def organize_music_files(root_dir: str):
    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)

        if os.path.isfile(file_path) and file_path.endswith(SUPPORTED_EXTENSIONS):
            album_tag = get_album_tag(file_path)

            if album_tag:
                sanitized_album_tag = sanitize_filename(str(album_tag))
                album_folder = os.path.join(root_dir, sanitized_album_tag)
                if not os.path.exists(album_folder):
                    os.makedirs(album_folder)

                try:
                    shutil.move(file_path, os.path.join(album_folder, filename))
                    print(f"Moved '{filename}' to '{sanitized_album_tag}' folder.")
                except Exception as e:
                    print(f"Error moving '{filename}': {e}")


def process_cover_image(image_path: str):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img = img.resize((200, 200))
            img.save(image_path, "JPEG", quality=100, subsampling=0)
            print(
                f"Modified '{os.path.basename(image_path)}' in {os.path.dirname(image_path)}"
            )
    except UnidentifiedImageError as e:
        print(f"Error processing '{os.path.basename(image_path)}': {str(e)}")


def process_images(root_dir: str):
    processed_folders = set()
    try:
        folders_processed = 0

        for root, dirs, _ in os.walk(root_dir):
            if ".rockbox" in dirs:
                dirs.remove(".rockbox")

            cover_path = os.path.join(root, COVER_FILENAME)

            if root in processed_folders:
                continue

            if os.path.exists(cover_path) and os.path.getsize(cover_path) > 0:
                print(f"\nProcessing folder: {root}")
                process_cover_image(cover_path)
            else:
                handle_audio_files(
                    root,
                    os.path.join(tempfile.gettempdir(), TEMP_FOLDER_NAME),
                )
                folders_processed += 1
                processed_folders.add(root)

        if folders_processed > 0:
            print(f"\n{folders_processed} folder(s) processed.")
        else:
            print("\nNo folders to process. Exiting.")

    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")


def clear_temp_directory():
    temp_folder = tempfile.gettempdir()
    temp_folder_path = os.path.join(temp_folder, TEMP_FOLDER_NAME)

    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)
        print(f"Cleared directory: {temp_folder_path}")
    else:
        print(f"Directory does not exist: {temp_folder_path}")


def main(root_directory: str) -> None:
    organize_music_files(root_directory)
    process_images(root_directory)
    clear_temp_directory()


if __name__ == "__main__":
    import typer

    typer.run(main)
