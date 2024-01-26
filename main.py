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
                         "Possible values: 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p",
                    choices=['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'], type=str, required=False)
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
    streams = video_info["streams"]

    # get best video stream
    video_stream = get_best_video_stream(streams, arguments.resolution)

    # get best audio stream
    audio_stream = get_best_audio_stream(streams, arguments.bitrate, arguments.samplerate)

    # download video
    download_video(arguments.video_url, video_stream, audio_stream, arguments.output, arguments.directory)


if __name__ == "__main__":
    main(args)
