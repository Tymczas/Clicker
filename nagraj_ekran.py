import cv2
import numpy as np
import pyautogui

# Video capture settings
frame_rate = 10
frame_size = (1920, 1080)

# Output video settings
output_file = "screen_recording.mp4"
codec = cv2.VideoWriter_fourcc(*"MP4V")

# Create video writer object
video = cv2.VideoWriter(output_file, codec, frame_rate, frame_size)

while True:
    # Capture screen
    img = pyautogui.screenshot()

    # Convert to numpy array
    frame = np.array(img)

    # Convert to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Write frame to video
    video.write(frame)

    # Exit loop if q key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources
video.release()
cv2.destroyAllWindows()
