import subprocess
from moviepy.editor import *

# Parameters  -------------------------------------------------------
input_file = "test_list.txt"
output_dir = "videos"
start_from_line = 1
cnt = 0  # for tracing, do not edit
# -------------------------------------------------------------------


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
    if result.returncode != 0:
        with open(f"log.txt", "a") as f:
            f.write(f"DOWNLOAD PROBLEM:\n{video_id}\n{result.stderr}\n")
        return

    try:
        # trim the video
        clip = VideoFileClip(f"{output_dir}/{video_id}.mp4")
        clip = clip.subclip(start_time, end_time)

        # special case: video_id starts with '-'
        if video_id[0] == '-':
            clip.write_videofile(f"{output_dir}/{video_id[1:]}_{start_time}_{end_time}.mp4")
            os.rename(f"{output_dir}/{video_id[1:]}_{start_time}_{end_time}.mp4",
                      f"{output_dir}/{video_id}_{start_time}_{end_time}.mp4")
        else:
            clip.write_videofile(f"{output_dir}/{video_id}_{start_time}_{end_time}.mp4", )
    except Exception as e:
        with open(f"log.txt", "a") as f:
            f.write(f"TRIM PROBLEM:\n{video_id} {start_time} {end_time}\n{e}\n")
        return

    # remove the original video
    clip.close()
    os.remove(f"{output_dir}/{video_id}.mp4")

    # log
    with open(f"log.txt", "a") as f:
        f.write(f"{cnt}\n")


def read_video_list(filename):
    with open(filename, 'r') as f:
        for line in f:
            global cnt
            cnt += 1
            if cnt < start_from_line:
                continue
            parts = line.strip().split('_')
            if len(parts) == 3:
                video_id, start_time, end_time = parts
                download_video(video_id, start_time, end_time)


# Example usage
if __name__ == "__main__":
    read_video_list(input_file)
