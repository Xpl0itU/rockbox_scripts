import tempfile
import sysrsync
import album_art_fix


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
        album_art_fix.main()

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
