from moviepy import ImageClip, AudioFileClip, concatenate_videoclips # temp for now for testing
import numpy as np
from os import makedirs
from utils import GetAudioDuration # change the sr is the sr changes in dev

class VideoGenerator:
    def __init__(self,output_dir="video_output/",video_name = "video_test"):
        video_name = video_name
        
        self.sr = 22050
        
        # output config
        self.output_dir = output_dir
        makedirs(output_dir, exist_ok=True)
        self.output_dest = output_dir.strip() + "/" + video_name.strip() + ".mp4"
        
    def MakeVideo(self, slides_with_transcript):
        clips = []
        for slide_name, slide_data in slides_with_transcript.items():
            frame_path = slide_data["image"]
            audio_path = slide_data["audio"]
            
            audio_clip = AudioFileClip(audio_path)
            img_clip = ImageClip(frame_path).with_duration(audio_clip.duration).with_audio(audio_clip)
            img_clip = img_clip.with_duration(audio_clip.duration).with_audio(audio_clip)
            
            clips.append(img_clip)
            
        final_video = concatenate_videoclips(clips,method="compose")
        final_video.write_videofile(self.output_dest, fps=24, codec="libx264",audio_codec="aac")