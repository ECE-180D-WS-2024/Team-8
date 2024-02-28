import cv2 as cv

def capture_frame(video_source=0):
    # Initialize the video capture object
    cap = cv.VideoCapture(video_source)
    # Capture a single frame
    _, frame = cap.read()

    return frame