"""
main.py
"""
from __future__ import annotations

from argparse import ArgumentParser
from os.path import expanduser as os_path_expanduser, join as os_path_join
from tempfile import gettempdir

from ytdlp_handler import (download_video, filter_audio_streams, filter_video_streams, get_best_audio_streams,
                           get_best_video_streams,
                           get_video_info, init_downloader)

# todo add longer help message to help users understand what the script does

parser = ArgumentParser(description="Download videos with the best or chosen quality")

parser.add_argument("video_url", help="The url of the video to download", type=str)
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
parser.add_argument("-o", "--output", help="Output file name. Default is the video title", type=str, required=False)
parser.add_argument("-d", "--directory", help="Set output directory. Default is user/Downloads", type=str,
                    required=False)
parser.add_argument("-f", "--output-format", help="The output format of the video", type=str, required=False)
# todo implement the following options
# parser.add_argument("-m", "--manual", help="Choose the video and audio streams manually. "
#                                            "User will be prompted to enter audio and video stream IDs",
#                     action="store_true")
# parser.add_argument("-r", "--resolution", help="The resolution of the video to download. "
#                                                "The highest framerate and bitrate will be preferred by default.",
#                     choices=[144, 240, 360, 480, 720, 1080, 1440, 2160], type=int, required=False)
# parser.add_argument("-fr", "--framerate",
#                     help="Video framerate. User will be prompted to choose from available options",
#                     type=str, required=False)
# parser.add_argument("-b", "--bitrate",
#                     help="Audio bitrate. User will be prompted to choose from available options",
#                     type=str, required=False)
# parser.add_argument("-s", "--samplerate",
#                     help="The samplerate of the audio to download. "
#                          "User will be prompted to choose from available options",
#                     type=str, required=False)

args = parser.parse_args()


def main(arguments):
    """
    main function
    :return:
    """

    # init settings
    downloader_options: dict = {
        "verbose": arguments.verbose,
        "merge_output_format": arguments.output_format or "mp4",
        "paths": {
            "home": arguments.directory or os_path_join(os_path_expanduser("~"), "Downloads"),  # downloads directory
            "temp": gettempdir()  # os temp directory
        },
        "outtmpl": {
            "default": f"{arguments.output}.%(ext)s" if arguments.output else "%(title)s.%(ext)s",
            "chapter": "%(title)s - %(section_number)03d %(section_title)s [%(id)s].%(ext)s"
        }
    }
    print(downloader_options["paths"]["temp"])

    # init downloader
    init_downloader(downloader_options)

    # get available streams
    video_info: dict = get_video_info(arguments.video_url)

    # get available streams
    streams: list[dict] = video_info["streams"]

    # get best video streams
    best_video_streams: list[dict] = get_best_video_streams(streams)

    # get best audio streams
    best_audio_streams = get_best_audio_streams(streams)

    # selected audio and video streams
    video_stream: dict = filter_video_streams(best_video_streams)  # , arguments.resolution, arguments.framerate)
    audio_stream: dict = filter_audio_streams(best_audio_streams)  # , arguments.bitrate, arguments.samplerate)

    # download video
    download_video(arguments.video_url, video_stream["format_id"], audio_stream["format_id"])


if __name__ == "__main__":
    main(args)
