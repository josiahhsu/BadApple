import numpy as np
from PIL import Image, ImageChops
from moviepy.editor import VideoFileClip, ImageSequenceClip

# frame customization functions
def rotation(img):
    return img[0].rotate(img[1] % 360)

def invert(img):
    return ImageChops.invert(img[0])

def recolor(img):
    return Image.eval(img[0], lambda x: x + 100)

def downscaled(img):
    return img[0].convert('1').resize((128,128)).convert('RGB')

# video processing
def process_frames(video, processor):
    frames = []
    num = 0
    for f in video.iter_frames():
        img = [Image.fromarray(f), num]
        new_image = processor(img)
        result = np.asarray(new_image)
        frames.append(result)
        num += 1
    return ImageSequenceClip(frames, fps=30)

def make_video(processor, source, output):
    # Modifies visuals of original video based on function used
    video = VideoFileClip(source)
    video_clip = process_frames(video, processor)

    # Add audio from original
    audio_clip = VideoFileClip(source)
    final_clip = video_clip.set_audio(audio_clip.audio)
    final_clip.write_videofile(output)

if __name__ == '__main__':
    make_video(downscaled, "BadApple.mp4", "final.mp4")
