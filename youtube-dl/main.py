import subprocess
from moviepy.editor import *

input_file = "videos.txt"
output_dir = "videos"


def download_video(video_id, start_time, end_time):
    # command to download the video
    command = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={video_id}",
        # "--postprocessor-args",
        # f"ffmpeg: -ss {start_time_fmt} -to {end_time_fmt} -c copy",
        # "--get-filename",
        "-S res,ext:mp4:m4a --recode mp4",
        "-o",
        f"{output_dir}/{video_id}.%(ext)s",
    ]

    # run subprocess and get output and error
    result = subprocess.run(command, capture_output=True, text=True, )
    print(result.stdout + result.stderr)

    # trim the video
    start_time_fmt = f"{start_time[:2]}:{start_time[2:4]}:{start_time[4:]}"
    end_time_fmt = f"{end_time[:2]}:{end_time[2:4]}:{end_time[4:]}"
    clip = VideoFileClip(f"{output_dir}/{video_id}.mp4")
    clip = clip.subclip(start_time_fmt, end_time_fmt)

    # special case: video_id starts with '-'
    if video_id[0] == '-':
        clip.write_videofile(f"{output_dir}/{video_id[1:]}_{start_time}_{end_time}.mp4")
        os.rename(f"{output_dir}/{video_id[1:]}_{start_time}_{end_time}.mp4",
                  f"{output_dir}/{video_id}_{start_time}_{end_time}.mp4")
    else:
        clip.write_videofile(f"{output_dir}/{video_id}_{start_time}_{end_time}.mp4")


def read_video_list(filename):
    """
    Read video details from a file and download each.

    Parameters:
    filename (str): Path to the file containing video details.
    """
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split('_')
            if len(parts) == 3:
                video_id, start_time, end_time = parts
                download_video(video_id, start_time, end_time)


# Example usage
if __name__ == "__main__":
    read_video_list(input_file)
