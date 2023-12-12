import tempfile
import sysrsync
from album_art_fix import (
    restore_backups,
    organize_music_files,
    process_images,
    clear_temp_directory,
)


def sync_music(source_directory: str, target_directory: str) -> None:
    # Fix the album art before syncing, I plan using this
    # with an iTunes library folder, and I don't want to
    # touch the source directory
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Copying files to temporary directory using rsync...")
        sysrsync.run(
            source=source_directory,
            destination=tmpdir,
            sync_source_contents=True,
            options=["-ahPWS", "--delete", "--inplace", "--no-compress"],
        )

        print("Extracting covers...")
        restore_backups(tmpdir)
        organize_music_files(tmpdir)
        process_images(tmpdir)
        clear_temp_directory()

        print("Copying files to target directory...")
        sysrsync.run(
            source=tmpdir,
            destination=target_directory,
            sync_source_contents=True,
            options=["-avhPWS", "--delete", "--inplace", "--no-compress"],
        )


if __name__ == "__main__":
    import typer

    typer.run(sync_music)
