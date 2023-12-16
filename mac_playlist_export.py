import os
import subprocess

APPLESCRIPT_EXPORT_CODE = """
tell application "Music"
    set playlistList to every user playlist
    set exportDirectory to "%s" & "/"

    repeat with aPlaylist in playlistList
        set playlistName to name of aPlaylist
        if playlistName is not equal to "Music" then
            try
                set exportPath to exportDirectory & playlistName & ".m3u"
                set exportFile to open for access exportPath with write permission

                write "#EXTM3U" & linefeed to exportFile
                write "#PLAYLIST:" & playlistName & linefeed to exportFile

                repeat with aTrack in tracks of aPlaylist
                    set trackLocation to get location of aTrack
                    if trackLocation is not missing value then
                        set posixLocation to POSIX path of trackLocation
                        set relativePath to text ((offset of "Media.localized" in posixLocation) + 15) thru -1 of posixLocation
                        write relativePath & linefeed to exportFile
                    end if
                end repeat

                close access exportFile
            on error errMsg
                display dialog "Error processing playlist: " & errMsg
            end try
        end if
    end repeat
end tell
    """


def run_applescript(applescript_code):
    subprocess.run(["osascript", "-e", applescript_code])


def export_playlists(export_directory: str = os.getcwd()):
    run_applescript(APPLESCRIPT_EXPORT_CODE % export_directory)


if __name__ == "__main__":
    import typer

    typer.run(export_playlists)
