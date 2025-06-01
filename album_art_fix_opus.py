import os
import shutil
import subprocess
import sys
import tempfile
import base64
import logging
import PIL
from PIL import Image, UnidentifiedImageError
from mutagen import File
from mutagen.flac import Picture, error as FLACError

SUPPORTED_EXTENSIONS = (".mp3", ".flac", ".opus")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
COVER_FILENAME = "cover.jpg"
TEMP_FOLDER_NAME = "cover_extraction_temp"

# Existing functions...

def extract_album_art_from_opus(file_path: str):
    file_ = File(file_path)  # Works with OggVorbis, FLAC, and potentially OggOpus files if tagged similarly

    # Attempt to extract 'METADATA_BLOCK_PICTURE' or equivalent tagged images
    pictures = file_.get("metadata_block_picture", []) + file_.tags.get("METADATA_BLOCK_PICTURE", [])
    for b64_data in pictures:
        try:
            data = base64.b64decode(b64_data)
        except (TypeError, ValueError):
            continue

        try:
            picture = Picture(data)
        except FLACError:
            continue

        extensions = {
            "image/jpeg": "jpeg",
            "image/png": "png",
            "image/gif": "gif",
        }
        ext = extensions.get(picture.mime, "jpeg")

        output_filename = os.path.splitext(os.path.basename(file_path))[0] + f'.{ext}'
        with open(output_filename, "wb") as h:
            h.write(picture.data)
        print(f"Cover image extracted from {file_path} and saved as {output_filename}")
         # Immediately resize the image after saving
        process_cover_image(output_filename)
        return output_filename

    print(f"No suitable album art found in {file_path}")
    return None

def handle_audio_files(directory: str, temp_folder: str):
    audio_files = [
        file for file in os.listdir(directory) if file.endswith(SUPPORTED_EXTENSIONS)
    ]
    for audio_file in audio_files:
        audio_file_path = os.path.join(directory, audio_file)
        if audio_file.endswith('.opus'):
            # Handle .opus files specifically
            cover_path = extract_album_art_from_opus(audio_file_path)
            if cover_path:
                # If a cover was extracted, move it to the desired location
                cover_dest_path = os.path.join(directory, COVER_FILENAME)
                shutil.move(cover_path, cover_dest_path)
                print(f"Cover image for .opus file moved to {cover_dest_path}")
        else:
            # Existing handling for other file types
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
                    print(f"Cover image extracted and saved as baseline JPEG in {directory}")
            except Exception as e:
                print(f"Error during extraction: {e}")




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
