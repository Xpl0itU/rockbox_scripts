# Rockbox Scripts

A collection of Python scripts for managing and updating Rockbox firmware on Rockbox devices, along with tools for organizing music files.

## Scripts

### `app.py`

This script serves as a unified entry point to perform multiple tasks related to Rockbox devices, music synchronization, and playlist management.

#### Usage

```bash
python app.py --playlists-directory-name "Playlists" --music-directory-name "Music" /path/to/rockbox_mount /path/to/music
```

#### Parameters

- mount_point: The mount point of the Rockbox device.
- source_music_directory: The source directory containing the music files to be synchronized.
- playlists_directory_name (optional): The name of the directory where playlists will be exported (default is "Playlists").
- music_directory_name (optional): The name of the directory on the Rockbox device where music will be synchronized (default is "Music").

### `album_art_fix.py`

This script organizes music files, extracts cover images from audio files, and processes the cover images to ensure a consistent format. It is designed to enhance the organization of a music collection.

#### Usage

```bash
python album_art_fix.py /path/to/music_directory
```
### `album_art_fix_opus.py`

Mostly copied from the above script. Extracts cover images from .opus files, and processes the images into a 200x200 cover.jpg file that works well with Rockbox.

#### Usage

```bash
python album_art_fix_opus.py /path/to/music_directory
```

### `mac_playlist_export.py`

This script organizes exports all the user playlists in the macOS Music app to the specified directory as m3u.

#### Usage

```bash
python mac_playlist_export.py /path/to/store_playlists
```

### `sync_music.py`

This script synchronizes music between a source and target directory. It uses `rsync` for efficient file transfer and incorporates the functionality of `album_art_fix.py` to fix album art before syncing.

#### Usage

```bash
python sync_music.py /path/to/source_directory /path/to/target_directory
```

### `update_rockbox.py`

This script updates the Rockbox firmware on any Rockbox supported device, it autodetects the current device and updates it accordingly. It checks for the latest Rockbox SVN revision, compares it with the current revision, and updates the firmware if necessary.

#### Usage

```bash
python update_rockbox.py /path/to/rockbox_mount_point
```

## Getting Started

1. Clone the repository.
1. Install the dependencies:
```bash
pip install -U -r requirements.txt
```

## Acknowledgments

- [@SupItsZaire](https://github.com/SupItsZaire) for their [Rockbox Cover Art Fixer](https://github.com/SupItsZaire/rockbox-cover-art-fixer) script
