"""
yt-dlp handler
"""

# todo implement better check method for video only and audio only streams
# todo check if audio stream interferes with video that already has audio and vice versa
#  and remove exclusions when selecting best streams

from __future__ import annotations

from yt_dlp import YoutubeDL

DOWNLOADER: YoutubeDL
video_info_raw: dict


def init_downloader(options: dict) -> None:
    """
    Initialize the yt-dlp downloader
    :return: None
    """

    global DOWNLOADER
    DOWNLOADER = YoutubeDL(options)


def get_video_info(video_url: str) -> dict:
    """
    Retrieve the available video and audio streams from the given video url
    :param video_url: (string) the url of the video
    :return: a list of dictionaries containing the available formats
    """

    download_info: dict = {}

    global DOWNLOADER, video_info_raw
    video_info_raw = DOWNLOADER.extract_info(video_url, download=False)  # save original info
    video_info: dict = DOWNLOADER.sanitize_info(video_info_raw)  # make info json serializable

    download_info["id"] = video_info["id"]
    download_info["uploader"] = f'{video_info["uploader"]} ({video_info["uploader_id"]})'
    download_info["title"] = video_info["title"]
    download_info["thumbnail"] = video_info["thumbnail"]
    download_info["streams"] = video_info["formats"]
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

    resolutions: list[int] = [144, 240, 360, 480, 720, 1080, 1440, 2160]

    # preallocate list. premium streams are appended to the end of the list
    best_streams: list[dict] = [{"format_id": f"{r}p unavailable"} for r in resolutions]

    for i, res in enumerate(resolutions):
        best_bitrate: float = 0

        for stream in streams:
            if stream["vcodec"] != "none" and stream["acodec"] == "none" and stream["height"] == res:
                if stream["vbr"] > best_bitrate:
                    best_bitrate = stream["abr"]
                    best_streams[i] = stream

    return best_streams


def get_best_audio_streams(streams: list[dict]) -> list[dict]:
    """
    Returns the best audio streams with the highest bitrate and highest samplerate.
    !!! Ignores streams with video for now. !!!
    :param streams: (dict) the available streams
    :return: (list[dict]) the best audio streams
    """

    best_bitrate: dict = {}
    best_samplerate: dict = {}
    premiums: list = []

    for stream in streams:
        if stream["resolution"] == "audio only" and stream["ext"] != "mp4":
            if stream["abr"] >= best_bitrate.get("abr", 0):
                best_bitrate = stream
            if stream["asr"] >= best_samplerate.get("asr", 0) and stream["abr"] >= best_samplerate.get("abr", 0):
                best_samplerate = stream

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
            if stream["vbr"] > best_bitrate:
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
            if stream["abr"] > best_bitrate:
                best_bitrate = stream["abr"]
                best_stream = stream
        return best_stream

    elif len(matching_streams) == 1:
        return matching_streams[0]

    else:
        print("No matching streams found")
        return {}


def download_video(video_url: str, video_stream_id: str, audio_stream_id: str) -> None:
    """
    Download the video with the selected streams to the given directory with the given filename
    :param video_url: the url of the video
    :param video_stream_id: (str) ID of the selected video stream
    :param audio_stream_id: (str) ID of the selected audio stream
    :return: None
    """
    global DOWNLOADER

    # todo convert video codec to H.264 and audio codec to AAC for compatibility

    DOWNLOADER.params["format"] = f"{video_stream_id}+{audio_stream_id}"
    DOWNLOADER.params["requested_format"] = [video_stream_id, audio_stream_id]
    DOWNLOADER.__init__(DOWNLOADER.params)  # "reload", format selection does not work otherwise

    # download
    DOWNLOADER.download([video_url])
