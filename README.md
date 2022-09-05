# YoutubeDownloader
Downloads video/playlist/audio from youtube url.

install all the required modules using below command
```
$ pip install -r requirements.txt
```

## Usage
```
usage: downloader.py [-h] -u  [-l] [-a | --audio | --no-audio] [-r]

Heyy, Download videos from Youtube.

options:
  -h, --help            show this help message and exit
  -u , --url            url of playlist or single video
  -l , --location       location for saving video/audio
  -a, --audio, --no-audio
  -r , --resolution     resolution i.e. 720

```

## Example
```
$ python3 downloader.py -u https://www.youtube.com/watch?v=GYeDTTb4jYI
```
