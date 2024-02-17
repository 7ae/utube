# Utube

Utube is a Python script that automates downloading YouTube videos and playlists using yt-dlp.

## Features

- Metadata and descriptions are exported.
- Thumbnail images are downloaded and embedded in the file.
- Metadata is embedded within the downloaded file.
- Subtitles (excluding auto-generated ones) and live chat are downloaded, with subtitles embedded.
- Segment information is included in the downloaded file.
- Video IDs are logged in `archive.txt` to prevent re-downloading.
- Geographic restrictions due to copyright are bypassed.
- Playlist downloads are handled, with an option to set a maximum number of downloads.
- The top 100 comments, with a maximum of 10 replies for each comment, are saved in `info.json`.

## Installation

```
virtualenv -p python ./tmp/venv
source tmp/venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python utube.py [-h] [--format {video,audio}] [--max-downloads NUMBER] [--path PATH] input
```

### Folder Structure

Utube creates folders for playlists or channels based on their IDs. Downloaded videos are stored inside these folders. Each video is named to include details such as its title and upload date.

-&nbsp;`./out/`
<br>&nbsp;&nbsp;&nbsp;&nbsp;- `{Playlist or Channel ID}/`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `{Upload Date}.{Uploader}.{Video Title}.({Resolution}).{Format ID}.[{Video ID}].{File Extension}`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `.info.json`: This file contains metadata and information about video.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `.description`: This file contains description section of YouTube page. It is provided by uploader.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `.{Thumbnail Extension}`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `.{Subtitle Language}.vtt`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `.live_chat.json`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `archive.txt`: This file logs downloaded video IDs to prevent re-downloading.

### Options

- `input`: Accepts a file path or YouTube link. If a file path is provided, it should contain YouTube links separated by line breaks.
- `--format`: Specifies the download format (audio or video). Default is video.
- `--max-downloads`: Stops downloading once the maximum limit is reached. Default is unlimited.
- `--path`: Sets the output path for downloaded files. Default is "./out".

### Example

Download videos from a file:

`python utube.py queue.txt --max-downloads 5`

- queue.txt:

  ```txt
  https://www.youtube.com/watch?v=xxxx&t=60s
  https://www.youtube.com/shorts/xxxx
  https://www.youtube.com/playlist?list=xxxx
  ```

Download audio from a playlist:

`python utube.py "https://www.youtube.com/playlist?list=xxxx" --format audio`
