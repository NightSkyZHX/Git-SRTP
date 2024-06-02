import cv2
import numpy as np


def calculate_rgb_difference(video_path, interval=5):

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Video Properties\nFrame Count: {frame_count}, Width: {width}, Height: {height}, FPS: {fps}")

    frame_ind = 0
    prev_frame = None

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_ind % interval == 0:
            if prev_frame is not None:
                abs_diff = cv2.absdiff(prev_frame, frame)
                mean_diff = np.mean(abs_diff, axis=(0, 1))
                # Output -----------------------------------------------------------------------------------------------
                print(f"Frame {frame_ind - interval} to {frame_ind} RGB Difference: R={mean_diff[2]:.2f}, G={mean_diff[1]:.2f}, B={mean_diff[0]:.2f}")

        prev_frame = frame.copy()
        frame_ind += 1

    cap.release()
    print("Finished processing.")


if __name__ == "__main__":
    calculate_rgb_difference(r"H:\SRTP\Datasets\ve8\VideoEmotion\VideoEmotionDataset1-Anger\youtube\ANGRYGARBAGEMANRAGES_.mp4")
