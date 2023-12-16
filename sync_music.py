import album_art_fix
import tempfile
import sysrsync


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
            options=[
                "-ahS",
                "--delete",
                "--inplace",
                "--no-compress",
                "--no-p",
                "--no-g",
                "--no-o",
            ],
        )

        print("Extracting covers...")
        album_art_fix.main(tmpdir)

        print("Copying files to target directory...")
        sysrsync.run(
            source=tmpdir,
            destination=target_directory,
            sync_source_contents=True,
            options=[
                "-avhPS",
                "--delete",
                "--inplace",
                "--no-compress",
                "--modify-window=2",
                "--no-p",
                "--no-g",
                "--no-o",
            ],
        )


if __name__ == "__main__":
    import typer

    typer.run(sync_music)
