"""
parses cmd arguments:
- video url
optional:
- m manual a/v stream selection
- o output file name
- d download directory
- r resolution (chooses the best quality of selected resolution): 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p
- f framerate (user will be prompted later)
- bitrate (user will be prompted later)
- samplerate (user will be prompted later)
"""
from __future__ import annotations

import argparse
import os

from ytdlp_handler import *

# todo optimize imports
# todo better formatting

parser = argparse.ArgumentParser(description="Download videos with the best or chosen quality")

parser.add_argument("video_url", help="The url of the video to download", type=str)
parser.add_argument("-m", "--manual",
                    help="Choose the video and audio streams manually. User will be prompted to enter audio and video stream IDs",
                    action="store_true")
parser.add_argument("-o", "--output", help="Output file name. The video title by default", type=str, required=False)
parser.add_argument("-d", "--directory", help="Output directory", type=str, required=False)
# todo consider adding option to manually set output format
parser.add_argument("-r", "--resolution",
                    help="The resolution of the video to download. The highest framerate and bitrate will be preferred by default.",
                    choices=[144, 240, 360, 480, 720, 1080, 1440, 2160], type=int, required=False)  # todo consider changing this to manual selection
# todo implement manually selecting the following options
parser.add_argument("-fr", "--framerate",
                    help="Video framerate. User will be prompted to choose from available options",
                    type=str, required=False)
parser.add_argument("-b", "--bitrate",
                    help="The bitrate of the audio to download. User will be prompted to choose from available options",
                    type=str, required=False)
parser.add_argument("-s", "--samplerate",
                    help="The samplerate of the audio to download. User will be prompted to choose from available options",
                    type=str, required=False)

args = parser.parse_args()


def main(arguments):
    """
    main function
    :return:
    """
    # todo implement manual selection

    # init settings
    DOWNLOADER_OPTIONS["path"] = arguments.directory or os.path.join(os.path.expanduser("~"), "Downloads")
    DOWNLOADER_OPTIONS["merge_output_format"] = "mp4"
    DOWNLOADER_OPTIONS["format"] = "mp4"
    DOWNLOADER_OPTIONS["outtmpl"] = {
        "default": f"{arguments.output}.%(ext)s" if arguments.output else "%(title)s [%(id)s].%(ext)s",
        "chapter": "%(title)s - %(section_number)03d %(section_title)s [%(id)s].%(ext)s"
    }

    # init downloader
    init_downloader(DOWNLOADER_OPTIONS)

    # get available streams
    video_info: dict = get_video_info(arguments.video_url)

    # get available streams
    streams: list[dict] = video_info["streams"]

    # get best video streams
    best_video_streams: list[dict] = get_best_video_streams(streams)

    # get best audio streams
    best_audio_streams = get_best_audio_streams(streams)

    # selected audio and video streams
    video_stream: dict = filter_video_streams(best_video_streams, arguments.resolution, arguments.framerate)
    audio_stream: dict = filter_audio_streams(best_audio_streams, arguments.bitrate, arguments.samplerate)

    # download video
    download_video(arguments.video_url, video_stream, audio_stream, arguments.output, arguments.directory)


if __name__ == "__main__":
    main(args)
