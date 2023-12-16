import mac_playlist_export
import os.path
import platform
import sync_music
import update_rockbox


def main(
    mount_point: str,
    source_music_directory: str,
    playlists_directory_name: str = "Playlists",
    music_directory_name: str = "Music",
):
    if platform.system() == "Darwin":
        print("Detected macOS, exporting playlists...")
        mac_playlist_export.export_playlists(
            os.path.join(mount_point, playlists_directory_name)
        )
    sync_music.sync_music(
        source_music_directory, os.path.join(mount_point, music_directory_name)
    )
    update_rockbox.update_rockbox(mount_point)
    print("Done")


if __name__ == "__main__":
    import typer

    typer.run(main)
