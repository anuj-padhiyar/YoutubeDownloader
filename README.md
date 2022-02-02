# YoutubeDownloader
Downloads videos/playlist from youtube url.

install all the required modules using below command
` pip install -r requirement.txt`


## Clone the repo
```
$ git clone https://github.com/RaviPabari/podbean_downloader
$ cd podbean_downloader/
```
## Usage
```
usage: playlistDownload.py [-h] -u  [-l] [-a | --audio | --no-audio] [-r]

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
$ python3 youtubeDownloader.py -u https://www.youtube.com/watch?v=GYeDTTb4jYI
```
