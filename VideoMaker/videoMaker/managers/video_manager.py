from dataclasses import dataclass
import ffmpeg
import os
import logging as log


@dataclass
class VideoBase:

    video_name: str = "output"
    image_directory: str = f'/images/{video_name}'
    input_glob: str = f'{image_directory}/*.jpg'
    output_file: str = f'{image_directory}/{video_name}.mp4'
    video_bitrate: str = "5000k"

    def input_directory_exists(self):
        return False if not os.path.exists(self.image_directory) else True

    def input_directory_not_empty(self):
        return False if len(os.listdir(self.image_directory)) == 0 else True


'''
Youtube Shorts video ffmpeg command example:
ffmpeg -framerate 15 -pattern_type glob -i "*_GOES16-*-GEOCOLOR-*.jpg" -i space_walk_short.mp3 -map 0:v -map 1:a -c:v libx264 -c:a aac
  -b:a 192k -r 24 -vf "scale=w=1080:h=1920,setsar=1" -af "afade=t=out:st=280:d=3" output.mp4

'''


@dataclass
class ShortsVideoManager(VideoBase):

    framerate: int = 15
    audiofile: str = ""
    vcodec: str = "libx264"
    acodec: str = "aac"
    audio_bitrate: str = "192k"
    filters: str = "scale=w=1080:h=1920,setsar=1"

    def build(self):
        log.info(f'[FFMPEG] Creating shorts video for job: {self.video_name}')
        (
            ffmpeg
            .input(self.input_glob, pattern_type='glob', framerate=self.framerate)
            .input(self.audiofile)
            .filter(self.filters)
            .output(self.output_file, vcodec=self.vcodec, acodec=self.acodec, audio_bitrate=self.audio_bitrate, video_bitrate=self.video_bitrate)
            .run()
        )


'''
Youtube video ffmpeg command example:
ffmpeg -framerate 15 -pattern_type glob -i *_GOES16-*-GEOCOLOR-*.jpg -c:v libx264 -r 24 -vf scale=1920x1080 ./output.mp4
'''


@dataclass
class VideoManager(VideoBase):

    framerate: int = 15
    vcodec: str = "libx264"
    filters: str = "scale=w=1920:h=1080"

    def build(self):
        log.info(f'[FFMPEG] Creating video for job: {self.video_name}')
        (
            ffmpeg
            .input(self.input_glob, pattern_type='glob', framerate=self.framerate)
            .filter(self.filters)
            .output(self.output_file, vcodec=self.vcodec, video_bitrate=self.video_bitrate)
            .run()
        )
