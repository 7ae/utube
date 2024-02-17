import argparse
import os
import subprocess
import sys

# define command-line arguments
parser = argparse.ArgumentParser(description='Download YouTube videos and playlists.')
parser.add_argument('input', help='File path or YouTube link. If a file path is provided, it should contain YouTube links line by line.')
parser.add_argument('--format', choices=['video', 'audio'], default='video', help='Specify the download format (audio or video). Default is video.')
parser.add_argument('--max-downloads', type=int, default=sys.maxsize, help='Maximum number of downloads. Default is unlimited.')
parser.add_argument('--path', help='Output path for downloaded files. Default is "./out".')

# parse the command-line arguments
args = parser.parse_args()

# use the provided output path or default to "./out"
output_path = args.path or './out'

# extract URLs from the input file or use the provided URL
urls = [line.strip() for line in open(args.input)] if os.path.isfile(args.input) else [args.input.strip()]
for u in urls:
    # extract the base video URL without any additional parameters
    base_url = u.split('&')[0]
    print(f"\033[36mSYSTEM:\033[0m [{__file__}] URL: {base_url}")

    # check if url is a video url or a playlist url
    is_playlist = 'list=' in base_url

    # download the best quality video file
    video_format = ['bestvideo+bestaudio/best']

    # download the best quality audio file and convert to flac
    audio_format = ['bestaudio/best', '-x', '--audio-format', 'flac']

    format_option = video_format if args.format == 'video' else audio_format

    # extract channel id or playlist id from url, and use the id as folder name
    channel_id = f'{base_url.split("list=")[1] if is_playlist else subprocess.check_output(["yt-dlp", "--print", "channel_url", "--playlist-items", "1", base_url], stderr=subprocess.DEVNULL, text=True).strip().split("/")[-1]}'
    print(f"\033[36mSYSTEM:\033[0m [{__file__}] ID: {channel_id}")

    try:
        # create subdirectory using id as name (return to the initial directory after completing the download)
        path = os.path.join(output_path, channel_id)
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    except Exception as e:
        # skip loop if id is invalid
        print(f"\033[31mERROR:\033[0m [{__file__}] '{path}' is an invalid ID.")
        continue

    # construct filename with limited 'uploader' and 'title' to 60 bytes each to prevent exceeding maximum filename length (255)
    filename = f'%(upload_date)s.%(uploader).60B.%(title).60B.(%(resolution)s).%(format_id)s.[%(id)s].%(ext)s'

    options = [
        '--write-info-json', '--write-description',  # export metadata and description
        '--write-thumbnail', '--embed-thumbnail',  # download thumbnail image file
        '--embed-metadata',  # embed metadata to the downloaded file
        '--sub-langs', 'all', '--write-subs', '--embed-subs',  # download captions (except auto-generated) and live chat
        '--embed-chapters',  # include segment information
        '--download-archive', 'archive.txt',  # record id of downloaded video to prevent redownloading
        '--geo-bypass',  # bypass geographic restriction due to copyright
        '--yes-playlist' if is_playlist else '--no-playlist',
        '--max-downloads', str(args.max_downloads),  # limit max download count
        # retrieve up to 100 comments, with a maximum of 10 replies total, sorted by the top comments
        '--get-comments', '--extractor-args', 'youtube:comment_sort=top;max_comments=100,all,10'
    ]

    # execute the download command
    subprocess.run(['yt-dlp', '-f'] + format_option + ['-o', filename, base_url] + options)

    # return to the initial directory once the download is complete
    os.chdir('../..')

