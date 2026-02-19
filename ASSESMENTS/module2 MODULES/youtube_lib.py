from pytubefix import YouTube

URL = "https://www.youtube.com/watch?v=cevGjmYyI3w"

YouTube(URL).streams.first().download()