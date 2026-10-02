import cv2

# Initialize the webcam (0 is usually the default built-in camera)
video_cap = cv2.VideoCapture(0)

def draw_futuristic_square(img, center, size, color, thickness):
    """Draws a sophisticated square with open sides and distinct corners."""
    cx, cy = center
    half_s = size // 2
    
    # Define the 4 corners of our square
    x1, y1 = cx - half_s, cy - half_s
    x2, y2 = cx + half_s, cy + half_s
    
    # Length of the corner ticks
    length = 20 

    # Top-Left Corner
    cv2.line(img, (x1, y1), (x1 + length, y1), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x1, y1), (x1, y1 + length), color, thickness, cv2.LINE_AA)

    # Top-Right Corner
    cv2.line(img, (x2, y1), (x2 - length, y1), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x2, y1), (x2, y1 + length), color, thickness, cv2.LINE_AA)

    # Bottom-Left Corner
    cv2.line(img, (x1, y2), (x1 + length, y2), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x1, y2), (x1, y2 - length), color, thickness, cv2.LINE_AA)

    # Bottom-Right Corner
    cv2.line(img, (x2, y2), (x2 - length, y2), color, thickness, cv2.LINE_AA)
    cv2.line(img, (x2, y2), (x2, y2 - length), color, thickness, cv2.LINE_AA)

while True:
    # Capture frame-by-frame
    ret, video_data = video_cap.read()
    
    # Check if the frame was grabbed successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Get the width and height of the video frame dynamically
    height, width = video_data.shape[:2]
    center_point = (width // 2, height // 2)
    
    # 🎨 UI Customization
    square_size = 240          # Size of the tracking square
    neon_cyan = (255, 255, 0)   # Color in BGR format
    line_thickness = 3          # Thickness of the corners

    # Draw the sophisticated live scanning box
    draw_futuristic_square(video_data, center_point, square_size, neon_cyan, line_thickness)

    # Add a clean text indicator above the square
    cv2.putText(video_data, "SYS_STATUS: ACTIVE SCAN", (center_point[0] - 90, center_point[1] - (square_size // 2) - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, neon_cyan, 1, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Video_live", video_data)
    
    # Stop the loop if the 'a' key is pressed
    if cv2.waitKey(10) == ord("a"):
        break

# Clean up: Release the camera capture and close all OpenCV windows
video_cap.release()
cv2.destroyAllWindows()
