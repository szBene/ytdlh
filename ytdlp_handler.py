"""
yt-dlp handler stuff
"""

from __future__ import annotations

import yt_dlp

# this stores the downloader settings
DOWNLOADER_OPTIONS: dict = {}


# sample downloader options:
# {
#     "compat_opts": [],
#     "http_headers": {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#         "Accept-Language": "en-us,en;q=0.5",
#         "Sec-Fetch-Mode": "navigate"
#     },
#     "forceprint": {},
#     "print_to_file": {},
#     "outtmpl": {
#         "default": "%(title)s [%(id)s].%(ext)s",
#         "chapter": "%(title)s - %(section_number)03d %(section_title)s [%(id)s].%(ext)s"
#     },
#     "epoch": 1706261823,
#     "_type": "video",
#     "_version": {
#         "version": "2023.12.30",
#         "current_git_head": null,
#         "release_git_head": "f10589e3453009bb523f55849bba144c9b91cf2a",
#         "repository": "yt-dlp/yt-dlp"
#     }
# }


def get_video_info(video_url: str) -> dict:
    """
    Retrieve the available video and audio streams from the given video url
    :param video_url: (string) the url of the video
    :return: a list of dictionaries containing the available formats
    """

    download_info: dict = {}

    global DOWNLOADER_OPTIONS
    with yt_dlp.YoutubeDL(DOWNLOADER_OPTIONS) as downloader:
        video_info: dict = downloader.sanitize_info(downloader.extract_info(video_url, download=False))

        download_info["id"] = video_info["id"]
        download_info["uploader"] = f'{video_info["uploader"]} ({video_info["uploader_id"]})'
        download_info["title"] = video_info["title"]
        download_info["thumbnail"] = video_info["thumbnail"]
        download_info["streams"] = video_info["formats"]  # todo remove storyboard formats
        download_info["yt-dlp-info"] = {}
        download_info["yt-dlp-info"]["version"] = video_info["_version"]
        download_info["yt-dlp-info"]["protocol"] = video_info["protocol"]
        download_info["yt-dlp-info"]["extractor"] = video_info["extractor"]
        download_info["yt-dlp-info"]["extractor_key"] = video_info["extractor_key"]

    return download_info


def get_best_video_streams(streams: list[dict]) -> list[dict]:
    """
    Returns the best video streams of each resolution with the highest bitrate
    !!! Ignores streams with audio for now. !!!
    :param streams: (dict) the available streams
    :return: (list[dict]) the best video streams for each resolution
    """
    # todo check if stream has audio (vcodec!="none"):
    #  does it interfere with merging later if a different audio stream is selected?

    resolutions: list[int] = [144, 240, 360, 480, 720, 1080, 1440, 2160]

    # preallocate list. premium streams are appended to the end of the list
    best_streams: list[dict] = [{"format_id": f"{r}p unavailable"} for r in resolutions]

    for i, res in enumerate(resolutions):
        best_bitrate: float = 0

        for stream in streams:
            if stream["vcodec"] != "none" and stream["acodec"] == "none" and stream["height"] == res:
                print("video only stream")
                # print(json.dumps(stream, indent=2))
                if stream["vbr"] > best_bitrate:
                    if "Premium" not in stream["format"]:
                        # print("better bitrate")
                        best_bitrate = stream["abr"]
                        best_streams[i] = stream
                    else:
                        # print("premium")
                        best_streams.append(stream)

    return best_streams


def get_best_audio_streams(streams: list[dict]) -> list[dict]:
    """
    Returns the best audio streams with the highest bitrate and highest samplerate.
    !!! Ignores streams with video for now. !!!
    :param streams: (dict) the available streams
    :return: (list[dict]) the best audio streams
    """
    # todo check if stream has audio (vcodec!="none"):
    #  does it interfere with merging later if a different audio stream is selected?

    best_bitrate: dict = {}
    best_samplerate: dict = {}
    premiums: list = []

    for stream in streams:
        if stream["resolution"] == "audio only" and stream["ext"] != "mp4":  # todo implement better check instead of mp4
            print("audio only stream")
            # print(json.dumps(stream, indent=2))
            if stream["abr"] >= best_bitrate.get("abr", 0):
                if "Premium" not in stream["format"]:
                    # print("better bitrate")
                    best_bitrate = stream
                else:
                    # print("premium")
                    premiums.append(stream)
            if stream["asr"] >= best_samplerate.get("asr", 0) and stream["abr"] >= best_samplerate.get("abr", 0):
                if "Premium" not in stream["format"]:
                    # print("better samplerate")
                    best_samplerate = stream
                else:
                    # print("premium")
                    premiums.append(stream)

    return [best_bitrate, best_samplerate] + premiums


def filter_video_streams(streams: list[dict], resolution: str | None = None, framerate: str | None = None) -> dict:
    """
    Filters the given video streams by resolution and framerate (if provided)
    :param streams: the list of available streams
    :param resolution: the desired resolution
    :param framerate: the desired framerate
    :return: the list of video streams that match the given resolution and framerate
    """

    best_stream: dict = {}
    matching_streams: list = []

    for i, stream in enumerate(streams):
        if "unavailable" not in stream["format_id"]:
            matching_streams.append(stream)

    if resolution:
        matching_streams = [stream for stream in matching_streams if stream["height"] == resolution]
        if not matching_streams:
            print(f"No streams with resolution {resolution}p found")

    if framerate:
        matching_streams = [stream for stream in matching_streams if stream["fps"] == framerate]
        if not matching_streams:
            print(f"No streams with framerate {framerate}fps found")

    if len(matching_streams) > 1:
        # auto select best quality stream based on bitrate, exclude premium streams
        best_bitrate: float = 0
        for stream in matching_streams:
            if stream["vbr"] > best_bitrate and "Premium" not in stream["format"]:
                best_bitrate = stream["vbr"]
                best_stream = stream
        return best_stream

    elif len(matching_streams) == 1:
        return matching_streams[0]

    else:
        print("No matching streams found")
        return {}


def filter_audio_streams(streams: list[dict], bitrate: str | None = None, samplerate: str | None = None) -> dict:
    """
    Filters the given audio streams by bitrate and samplerate (if provided)
    :param streams: the list of available streams
    :param bitrate: the desired bitrate
    :param samplerate: the desired samplerate
    :return: the list of audio streams that match the given bitrate and samplerate
    """

    best_stream: dict = {}
    matching_streams: list = []

    for i, stream in enumerate(streams):
        if "unavailable" not in stream["format_id"]:
            matching_streams.append(stream)

    if bitrate:
        matching_streams = [stream for stream in matching_streams if stream["abr"] == bitrate]
        if not matching_streams:
            print(f"No streams with bitrate {bitrate}kbps found")

    if samplerate:
        matching_streams = [stream for stream in matching_streams if stream["asr"] == samplerate]
        if not matching_streams:
            print(f"No streams with samplerate {samplerate}Hz found")

    if len(matching_streams) > 1:
        # auto select best quality stream based on bitrate, exclude premium streams
        best_bitrate: float = 0
        for stream in matching_streams:
            if stream["abr"] > best_bitrate and "Premium" not in stream["format"]:
                best_bitrate = stream["abr"]
                best_stream = stream
        return best_stream

    elif len(matching_streams) == 1:
        return matching_streams[0]

    else:
        print("No matching streams found")
        return {}


def download_video(video_url: str, video_stream: dict, audio_stream: dict, output_file: str | None = None, download_dir: str | None = None):
    """
    downloads the video using yt-dlp
    """
    pass
