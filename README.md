# ytdlh

A simple video downloader helper for yt-dlp

## Usage

- Get the latest version of ytdlp.exe from the [releases](https://github.com/szBene/ytdlh/releases)

- Put it into your user directory (`C:\Users\username`) for easy access (optional, but your terminal will open in
  this directory by default)

- Open your terminal (cmd, powershell, etc.)

- Run `ytdlh.exe`:

```bash
ytdlh.exe [options] [url]
```

Note: `[options]` are not required, `[url]` is, except for `--help` and `--version`

For example:

```bash
ytdlh.exe https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

will download a good quality video into your Downloads directory

Run `ytdlh.exe --help` for info on the available options

___

## Set up for development (Windows)

Prerequisites:

- [Python 3.11.7](https://www.python.org/downloads/release/python-3117/)
    - make sure to check the "Add Python to PATH" option during installation
- [Git](https://git-scm.com/downloads)

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

After [setting up for development](#set-up-for-development-windows), run the following command:

```bash
pyinstaller -c --onefile --name ytdlh.exe main.py ytdlp_handler.py
```

You will find the executable in the `dist` directory. from there, follow the instructions in the [Usage](#usage) section

## Updates

This tool does not check for updates. for that, come back here from time to time

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

Don't forget to include the version of ytdlh (run `ytdlh.exe --version`) and the console output of the program.
Check back frequently, in case I have any followup questions or updates.
