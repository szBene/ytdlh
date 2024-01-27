# ytdlh

A simple video downloader helper for yt-dlp

## Usage

- Get the latest version of `ytdlp-build.zip` from [releases](https://github.com/szBene/ytdlh/releases)

- Extract the contents into your user directory (`C:\Users\username`) for easy access (optional, but your terminal will
  open in this directory by default)
- Or use the install script to install ytdlh into your user directory:
    - Run `install_ytdlh.bat` if you have the `ytdlp-build.zip` file in the same directory as the installer script
    - Or drag the `ytdlp-build.zip` file onto the `install_ytdlh.bat` file
- Open your terminal (cmd, powershell, etc.)
- Run `ytdlh.bat`:

```bash
ytdlh.bat [options] [url]
```

Note: `[options]` are not required, `[url]` is, except when using `--help` and `--version`

For example:

```bash
ytdlh.bat https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

will download a good quality mp4 video file into your Downloads directory. Its name will be the title of the video.

Run `ytdlh.bat --help` for info on the available options

If you would like to uninstall ytdlh, run `uninstall_ytdlh.bat`. This will delete the `ytdlh.bat` file and the `ytdlh`
directory from your user directory.

___

## Set up for development (Windows)

Prerequisites:

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
built
executable in the project's root directory. To use the ytdlh executable created with this method, you have two
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

- [ ] more usage options:
    - [ ] manual stream selection
    - [ ] pre-select resolution
    - [ ] pre-select fps
    - [ ] pre-select audio quality (bitrate and sampling rate separately)
- [ ] download audio only
- [ ] download video only
- [ ] download playlist
- [ ] download multiple videos at once

Feel free to open an issue if you have any other ideas.

Contributions are also welcome.

### Bug fixes

For any bugs or issues you find, please open an issue. I will try to fix them as soon as possible.

Don't forget to include the version of ytdlh and the entire console output of the program.
Check back frequently, in case I have any followup questions or updates.
