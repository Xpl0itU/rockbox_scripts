# Rockbox Scripts

A collection of Python scripts for managing and updating Rockbox firmware on iPod devices, along with tools for organizing music files.

## Scripts

### `album_art_fix.py`

This script organizes music files, extracts cover images from audio files, and processes the cover images to ensure a consistent format. It is designed to enhance the organization of a music collection.

#### Usage

```bash
python album_art_fix.py /path/to/music_directory
```

### `sync_music.py`

This script synchronizes music between a source and target directory. It uses `rsync` for efficient file transfer and incorporates the functionality of `album_art_fix.py` to fix album art before syncing.

#### Usage

```bash
python sync_music.py /path/to/source_directory /path/to/target_directory
```

### `update_rockbox.py`

This script updates the Rockbox firmware on an iPod, specifically targeting the iPod 6G. It checks for the latest Rockbox SVN revision, compares it with the current revision, and updates the firmware if necessary.

#### Usage

```bash
python update_rockbox.py /path/to/ipod_mount_point
```

## Getting Started

1. Clone the repository.
1. Install the dependencies:
```bash
pip install -U -r requirements.txt
```

## Acknowledgments

- [@SupItsZaire](https://github.com/SupItsZaire) for their [Rockbox Cover Art Fixer](https://github.com/SupItsZaire/rockbox-cover-art-fixer) script
