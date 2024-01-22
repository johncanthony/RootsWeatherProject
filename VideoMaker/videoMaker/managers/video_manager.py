from dataclasses import dataclass
import ffmpeg
import os
import logging as log


@dataclass
class VideoBase:

    video_name: str = "output"
    video_bitrate: str = "5000k"

    def __post_init__(self):
        self.IMAGE_DIR = os.getenv('IMAGE_DIR') or './images'

    @property
    def image_directory(self):
        return f'{self.IMAGE_DIR}/{self.video_name}'

    @property
    def output_file(self):
        return f'{self.image_directory}/{self.video_name}.mp4'

    @property
    def input_glob(self):
        return f'{self.image_directory}/*.jpg'

    def input_directory_exists(self):
        log.info(f'[FFMPEG] Checking for input directory: {self.image_directory}')
        return False if not os.path.exists(self.image_directory) else True

    def input_directory_not_empty(self):
        log.info(f'[FFMPEG] Checking for images in input directory: {self.image_directory} - file count: {len(os.listdir(self.image_directory))}')
        return False if len(os.listdir(self.image_directory)) == 0 else True


'''
Youtube Shorts video ffmpeg command example:
ffmpeg -framerate 15 -pattern_type glob -i "*_GOES16-*-GEOCOLOR-*.jpg" -i space_walk_short.mp3 -map 0:v -map 1:a -c:v libx264 -c:a aac
  -b:a 192k -r 24 -vf "scale=w=1080:h=1920,setsar=1" -af "afade=t=out:st=280:d=3" output.mp4

'''


@dataclass
class ShortsVideoManager(VideoBase):

    framerate: int = 15

    @property
    def audiofile(self):
        return os.getenv('RWP_AUDIOFILE') or "./audio/clip.mp3"

    vcodec: str = "libx264"
    acodec: str = "aac"
    audio_bitrate: str = "192k"

    def build(self):
        log.info(f'[FFMPEG] Creating shorts video for job: {self.video_name}')

        input_video = ffmpeg.input(self.input_glob, pattern_type='glob', framerate=self.framerate).filter("scale", 1080, 1920).filter("setsar", 1)
        input_audio = ffmpeg.input(self.audiofile)

        (
            ffmpeg
            .output(input_audio,
                    input_video, self.output_file,
                    vcodec=self.vcodec,
                    acodec=self.acodec,
                    audio_bitrate=self.audio_bitrate,
                    video_bitrate=self.video_bitrate,
                    shortest=None)
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

    def build(self):
        log.info(f'[FFMPEG] Creating video for job: {self.video_name}')
        (
            ffmpeg
            .input(self.input_glob, pattern_type='glob', framerate=self.framerate)
            .filter("scale", 1920, 1080)
            .output(self.output_file, vcodec=self.vcodec, video_bitrate=self.video_bitrate)
            .run()
        )
