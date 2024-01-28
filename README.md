# ytdlh

A simple video downloader helper for yt-dlp

_Disclaimer: this tool is provided as-is, without any warranty. I am not responsible for any damage caused by this
tool, as it is unable to cause any harm if used correctly._

## Usage

Prerequisites:

- Windows 10 or 11
- FFmpeg (see [Setup FFmpeg](#setup-ffmpeg))

### Setup ytdlh

- Get the latest version of `ytdlp-build.zip` and `install_ytdlh.bat` from the Assets section of the latest
  [release](https://github.com/szBene/ytdlh/releases) or pre-release
- Extract the contents into your user directory (`C:\Users\username`) for easy access (optional, but your terminal will
  open in this directory by default)
- Or use the installer script to install ytdlh into your user directory:
    - **Note**: the installer and uninstaller scripts may be blocked by Windows Defender SmartScreen or your
      antivirus of your choice. You can safely ignore this warning, as the scripts only extract the files into your
      user folder, and delete them when uninstalling or if an existing version is there. To be safe, make sure you
      don't have a `ytdlh` directory and a `ytdlh.bat` file in your user directory before running the installer script.
    - Run `install_ytdlh.bat` if you have the `ytdlp-build.zip` file in the same directory as the installer script
    - Or drag the `ytdlp-build.zip` file onto the `install_ytdlh.bat` file
- Open your terminal (cmd, powershell, etc.)
- Run `ytdlh.bat`:

```bash
ytdlh.bat [options] [url]
```

**Note**: `[options]` are not required, `[url]` is, except when using `--help` and `--version`

For example:

```bash
ytdlh.bat "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

This command will download an mp4 video file into your Downloads directory. Its name will be the title of
the video.

ytdlh selects the best video and audio streams available, by bitrate. The codec of the video stream will
not be converted automatically. This feature will be added in a [future update](#feature-updates).

Run `ytdlh.bat --help` for info on the available options

If you would like to uninstall ytdlh, run `uninstall_ytdlh.bat` (you can also get this script from
the [releases](https://github.com/szBene/ytdlh/releases)). This will remove the `ytdlh.bat` file and the `ytdlh`
directory from your user directory.

### Setup FFmpeg

Not sure if FFmpeg is installed?

- Open your terminal (cmd, powershell, etc.)
- Run `ffmpeg -version`
- If you get an error, FFmpeg is not installed
- If you get a version number, and a bunch of text, FFmpeg is installed

If you don't have FFmpeg installed, there are two ways to install it.

**Install FFmpeg**:

- Using a package manager:
    - [winget](https://docs.microsoft.com/en-us/windows/package-manager/winget/):
        - Open your terminal (cmd, powershell, etc.)
        - `winget install ffmpeg`
        - Accept the license agreement
    - [Chocolatey](https://chocolatey.org/install)
        - Open your terminal (cmd, powershell, etc.)
        - Run `choco install ffmpeg`
    - [Scoop](https://scoop.sh/)
        - Open your terminal (powershell)
        - Run `scoop install ffmpeg`
    - **Notes**:
        - winget should be installed by default on Windows 10 systems that have the 22H2 update installed. If you don't
          seem to have it, you can follow
          Microsoft's [instructions](https://learn.microsoft.com/en-us/windows/package-manager/winget/#install-winget)
          on how to install it
        - Chocolatey and Scoop are third-party package managers. If you don't have them installed, you can follow their
          respective installation instructions on their websites:
            - [Chocolatey](https://chocolatey.org/install)
            - [Scoop](https://github.com/ScoopInstaller/Install?tab=readme-ov-file#installation)
- Manually:
    - Open [this](https://ffmpeg.org/download.html) page in your browser
    - Hover over or click on the Windows icon
    - Click on "[Windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)"
    - Scroll down to the "[Release builds](https://www.gyan.dev/ffmpeg/builds/#release-builds)" section
    - Download `ffmpeg-release-full.7z`
    - Extract the contents of the archive into a directory of your choice
    - Add the directory to your PATH environment variable:
        - Open the start menu
        - Type "environment variables"
        - Click on "Edit the system environment variables"
        - Click on "Environment Variables..."
        - Under "System variables", select "Path" and click on "Edit..."
        - Click on "New"
        - Enter the path of the `bin` directory of the extracted archive
        - Click on "OK"
        - Click on "OK"
        - Click on "OK"
    - **Note:** if you installed FFmpeg manually, you will have to close and reopen your terminal for the changes to
      take effect. Alternatively, you can run `refreshenv` in your terminal to refresh the environment variables

___

## Set up for development (Windows)

Additional prerequisites:

- [Python 3.11.7](https://www.python.org/downloads/release/python-3117/)
    - make sure to check the "Add Python to PATH" option during installation
- [Git](https://git-scm.com/downloads)
- powershell (for using the build script)

```bash
git clone https://github.com/szBene/ytdlh.git
cd ytdlh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

(nope, no linux yet)

## Build

Don't trust the release version? No problem, you can build it yourself!

After [setting up for development](#set-up-for-development-windows), run the following command in your terminal:

```bash
pyinstaller -c --onefile --name ytdlh.exe main.py ytdlp_handler.py
```

This command will create a portable, self-contained executable of ytdlh.

You will find the executable in the `dist` directory. From there, follow the instructions in the [Usage](#usage)
section. However, instead of `ytdlh.bat`, you will have to run `ytdlh.exe`.

**NOTE:** this command, specifically the `--onefile` option, might build an executable that will result in a false
positive detection by your antivirus.
This happened to me with release [0.1.0](https://github.com/szBene/ytdlh/releases/tag/ytdlh-beta-0.1). In the
release notes, I included the Virustotal scan results of the executable.

I also created a [build script](build.bat), that doesn't use the `--onefile` option. It will create a zip file of the
built executable in the project's root directory. To use the ytdlh executable created with this method, you have two
options:

1. With the [runner](ytdlh.bat) script:
    - Extract the contents of the zip file directly into your user directory (`C:\Users\username`)
    - Open your terminal and run `ytdlh.bat` just like you would run `ytdlh.exe`
2. Without the runner script:
    - Extract the zip file into a directory of your choice
    - Move the contents of the `ytdlh` directory into your user directory (`C:\Users\username`)
    - Open your terminal and run `ytdlh.exe`

## Updates

This tool does not check for updates. For that, come back here from time to time

### Feature updates

There are a few features that I would like to add some time in the future, not in any particular order:

- [ ] set output video codec to H.264, set output audio codec to AAC (convert if necessary)
- [ ] more usage options:
    - [ ] manual output codec selection for video and audio
    - [ ] manual stream selection
    - [ ] pre-select resolution
    - [ ] pre-select fps
    - [ ] pre-select audio quality (bitrate or sampling rate)
- [ ] download audio only
- [ ] download video only
- [ ] download playlist
- [ ] download multiple videos at once

Feel free to open an issue if you have any other ideas.

Contributions are also welcome.

### Bug fixes

For any bugs or issues you find with the tool or this guide, please open an issue. I will try to fix them as soon as
possible.

Don't forget to include the version of ytdlh and the entire console output of the program(s).

Check back frequently, in case I have any followup questions or updates.
