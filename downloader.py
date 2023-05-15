import os
import argparse
import nest_asyncio
from bs4 import BeautifulSoup
from pathlib import Path
from pytube import YouTube
from requests_html import HTMLSession

class YoutubeDownloader:
    def __init__(self):
        self.content = ""
        self.links = []
        self.location = "Downloads/"
        self.url = ""

        #get the required data from the initiator function
        self.initiator()
        
        # #if the link is the link of playlist then we have to get all the links from playlist
        if "list" in self.url:
            self.get_page()
            self.extract_link()
        else:
            self.links.append(self.url)
        self.download_it()
            
    def initiator(self):
        try:
            #it will parse the arguments from command line
            parser = argparse.ArgumentParser(description="Heyy, Download videos from Youtube.")
            parser.add_argument("-u", "--url", required=True, type=str, help="url of playlist or single video",metavar='')
            parser.add_argument("-l", "--location", required=False, type=str, help="location for saving video/audio",metavar='')
            parser.add_argument("-a","--audio",required=False,action=argparse.BooleanOptionalAction,default=False)
            parser.add_argument("-r","--resolution",required=False,type=str, help="resolution i.e. 720",metavar='')
            args = parser.parse_args()

            self.url = args.url
            self.audio = args.audio
            self.resolution = str(args.resolution) + "p"
            if args.location:
                self.location = args.location + "/"
        except Exception as e:
            print(e)
            exit(0)

    def get_page(self):
        print("Getting Youtube Videos....")

        #stop loop for async. call
        nest_asyncio.apply()
        session = HTMLSession()

        #getting response from web and parsing it
        response = session.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.content = str(soup.find_all('script')).split("\n")
        print("Youtube Video Collected.")

    def extract_link(self):
        for line in self.content:
            if "/watch?" in line:
                pointer = 0
                while True:
                    if "/watch?" not in line[pointer:]:
                        break
                    start = line[pointer:].find("/watch?")
                    stop = line[pointer+start:].find("\"")
                    if stop==-1:
                        break
                    finalLink = line[pointer+start:pointer+start+stop].replace("\\u0026","&")
                    if 'index' in finalLink:
                        self.links.append("https://www.youtube.com"+finalLink.split("&")[0])
                    pointer = pointer + start + stop
        self.links = list(set(self.links))

    def get_resolution(self,stream):
        stream = stream.filter(progressive=True,file_extension='mp4').order_by('resolution').desc()
        availableRes = [int(i.resolution[:-1]) for i in stream.filter()]

        #user havn't passed the value for resolution
        if self.resolution[:-1]=="None":
            print("Selecting Best Resolution Available...")
            return str(availableRes[0]) +'p'
        
        #user inputted resolution is not available
        if int(self.resolution[:-1]) not in availableRes:
            print("Switching Down Resolution...")
            return str(availableRes[0]) +'p'
        
        return self.resolution
        
    """
    #Futute Development(solve ffmpeg bug or find some merger)

    def merger(self,audio,video,target):
        video_stream = ffmpeg.input(video)
        audio_stream = ffmpeg.input(audio)

        #audio and video are merged and after that it would be removed
        ffmpeg.concat(audio_stream, video_stream,a=1,v=1).output(target).run()
        os.remove(audio)
        os.remove(video)

    def high_resolution(stream,fullpath,yt):
        audioclip = stream.filter(only_audio=True).first().download(fullpath)
        os.rename(audioclip,fullpath+'/temp.mp3')
        videoclip = stream.filter(res=self.get_resolution(stream),file_extension='mp4').order_by('resolution').desc().first().download(fullpath)
        os.rename(videoclip,fullpath+"/temp.mp4")
        self.merger(fullpath+"/temp.mp3",fullpath+"/temp.mp4",yt.title+".mp4")
    """

    def download_helper(self,link,fullpath):
        #calling the YouTube module with require link to generate streams
        yt = YouTube(link)
        stream = yt.streams
        print("Downloading...")

        #download audio if user inputted for it otherwise video
        if self.audio:
            audioclip = stream.filter(only_audio=True).first().download(fullpath)
            os.rename(audioclip, fullpath+"/"+yt.title+ '.mp3')
        else:
            videoclip = stream.filter(progressive=True,res=self.get_resolution(stream),file_extension='mp4').first().download(fullpath)
        print(yt.title + " has been successfully downloaded.")
        
    def download_it(self): 
        cwd = Path.cwd()
        fullpath = cwd.joinpath(self.location)
        
        #check for the path exists or not.
        if fullpath.exists():
            print("Folder Already Exists at that path....Please Change")
            return False

        #download all the videos
        for link in self.links:
            try:
                self.download_helper(link,str(fullpath))
            except Exception as e:
                print(e)
                pass

if __name__ == '__main__':
    YoutubeDownloader()