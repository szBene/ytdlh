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


def get_best_video_stream(streams: list[dict], resolution: str | None = None) -> dict:
    """
    returns the best video stream (of the given resolution, if provided)
    """
    pass


def get_best_audio_stream(streams: list[dict], bitrate: str | None = None, samplerate: str | None = None) -> dict:
    """
    returns the best audio stream (of the given bitrate and samplerate, if provided)
    if the best bitrate and best samplerate are not the same stream, the best bitrate stream is prioritized
    """
    pass


def download_video(video_url: str, video_stream: dict, audio_stream: dict, output_file: str | None = None, download_dir: str | None = None):
    """
    downloads the video using yt-dlp
    """
    pass
