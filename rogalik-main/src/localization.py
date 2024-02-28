import cv2 as cv

def capture_frame(cap):
    # Initialize the video capture object
    # Capture a single frame
    _, frame = cap.read()

    return frame