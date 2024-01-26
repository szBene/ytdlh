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

from ytdlp_handler import *

parser = argparse.ArgumentParser(description="Download videos with the best or chosen quality")

parser.add_argument("video_url", help="The url of the video to download", type=str)
parser.add_argument("-m", "--manual",
                    help="Choose the video and audio streams manually. User will be prompted to enter audio and video stream IDs",
                    action="store_true")
parser.add_argument("-o", "--output", help="Output file name", type=str, required=False)
parser.add_argument("-d", "--directory", help="Output directory", type=str, required=False)
parser.add_argument("-r", "--resolution",
                    help="The resolution of the video to download. The highest framerate will be preferred."
                         "Possible values: 144, 240, 360, 480, 720, 1080, 1440, 2160 (no *p at the end)",
                    choices=[144, 240, 360, 480, 720, 1080, 1440, 2160], type=int, required=False)
parser.add_argument("-f", "--framerate",
                    help="Video framerate.\nUser will be prompted to choose from available options",
                    type=str, required=False)
parser.add_argument("-b", "--bitrate",
                    help="The bitrate of the audio to download.\nUser will be prompted to choose from available options",
                    type=str, required=False)
parser.add_argument("-s", "--samplerate",
                    help="The samplerate of the audio to download.\nUser will be prompted to choose from available options",
                    type=str, required=False)

args = parser.parse_args()


def main(arguments):
    """
    main function
    :return:
    """

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
    download_video(arguments.video_url, best_video_streams, best_audio_streams, arguments.output, arguments.directory)


if __name__ == "__main__":
    main(args)
