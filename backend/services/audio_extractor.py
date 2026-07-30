from moviepy.editor import VideoFileClip
from pathlib import Path


def extract_audio(video_path):

    output = (
        Path(video_path)
        .with_suffix(".wav")
    )

    clip = VideoFileClip(video_path)

    clip.audio.write_audiofile(
        str(output),
        logger=None,
    )

    clip.close()

    return str(output)