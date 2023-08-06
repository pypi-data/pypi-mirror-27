import time

import pafy

from .filemanager import get_workingdir, get_tmpfile

class YouTube(object):
    def __init__(self, url):
        self.url = url
        self._metadata(url)

    def create_audiostream_dict(self, audiostreams):
        """
        Creates audiostream dictionary using bitrate as key
        """
        audiostream_dict = dict()
        highest_webm = None
        highest_rate = 0
        for i, audiostream in enumerate(audiostreams):
            _key = '-'.join([audiostream.bitrate, audiostream.extension])
            if audiostream.extension == 'webm':
                bitrate = int(audiostream.bitrate.replace('k', ''))
                if bitrate > highest_rate:
                    highest_rate = bitrate
                    highest_webm = _key
            audiostream_dict[_key] = i
        audiostream_dict['high'] = highest_webm
        return audiostream_dict

    def _metadata(self, url):
        """
        Gets the video metadata from url
        """
        video = pafy.new(url)
        self.video = video
        self.title = video.title
        self.duration = video.duration
        self.audio_available = self.create_audiostream_dict(video.audiostreams)
        self.audiostreams = video.audiostreams

    def download_audio(self, audiostream_key):
        """
        Downloads audio file from youtube in the specified audiostream, if
        the audiostream size/format is not specified, downloads default audio
        """
        audio_index = lambda : self.audio_available.get(audiostream_key)
        audio = self.audiostreams[audio_index()]
        tmp_file = '/'.join([get_workingdir(), get_tmpfile(audio.extension)])
        self.audiostreams[audio_index()].download(filepath=tmp_file)
        return tmp_file

if __name__ == '__main__':
    yt = YouTube("https://www.youtube.com/watch?v=Z4SvMdNPUcc")
    yt.download_audio(audiostream_key='160k-webm')
