import cv2
# import numpy as np
import matplotlib.pyplot as plt


def extract_color_histogram(video_path):

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

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histogram = cv2.calcHist([frame], [i], None, [256], [0, 256])
            # Output ---------------------------------------------------------------------------------------------------
            plt.plot(histogram, color=col)
            plt.xlim([0, 256])
            plt.title(f"Frame {frame_ind}")
        plt.pause(0.01)
        plt.clf()

        frame_ind += 1

    cap.release()
    print("Finished processing.")


if __name__ == "__main__":
    extract_color_histogram(r"H:\SRTP\Datasets\ve8\VideoEmotion\VideoEmotionDataset1-Anger\youtube\ANGRYGARBAGEMANRAGES_.mp4")
