import cv2
import mediapipe as mp
import numpy as np
import math

# Your pose estimation function to get left heel coordinates
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

def get_feet_coordinates(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print("No pose landmarks detected!")
        return None

    landmarks = results.pose_landmarks.landmark
    feet = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_shoulder_coords = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
    right_shoulder_coords = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))


    shoulder_length_pixels = ((right_shoulder_coords[0] - left_shoulder_coords[0]) ** 2 + 
                              (right_shoulder_coords[1] - left_shoulder_coords[1]) ** 2) ** 0.5

    feet_x = int(feet.x * image_width)
    feet_y = int(feet.y * image_height)

    return feet_x, feet_y, shoulder_length_pixels

# Your human outline extraction function
def extract_human_outline_mediapipe(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load the image.")
        return None, None, None

    # Convert to RGB for MediaPipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    # Process the image to get the segmentation mask
    results = selfie_segmentation.process(rgb_image)

    if results.segmentation_mask is not None:
        # Create a binary mask where the person is highlighted
        mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255

        # Apply Canny Edge Detection
        edges = cv2.Canny(mask, threshold1=50, threshold2=150)

        # Get Non-zero (Edge) Pixel Coordinates
        y_coords, x_coords = np.nonzero(edges)

        # Find Topmost and Bottommost Pixels
        topmost_y = np.min(y_coords)  # Minimum y (topmost)
        bottommost_y = np.max(y_coords)  # Maximum y (bottommost)

        # Get Corresponding x Coordinates
        topmost_x = x_coords[np.argmin(y_coords)]
        bottommost_x = x_coords[np.argmax(y_coords)]

        top_pixel = [int(topmost_x), int(topmost_y)]
        bottom_pixel = [int(bottommost_x), int(bottommost_y)]

        # Print Results
        print(f"Topmost Pixel: ({topmost_x}, {topmost_y})")
        print(f"Bottommost Pixel: ({bottommost_x}, {bottommost_y})")

        # # Find contours in the edge-detected image
        # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # if contours:
        #     # Assume the largest contour is the human outline
        #     largest_contour = max(contours, key=cv2.contourArea)

        #     # Extract all points from the largest contour
        #     all_points = [point[0] for point in largest_contour]

        #     # Find the highest (minimum y-coordinate) point
        #     highest_point = min(all_points, key=lambda p: p[1])  # Minimum y-coordinate
        #     lowest_point = max(all_points, key=lambda p: p[1])   # Maximum y-coordinate

        return top_pixel, bottom_pixel, edges
    else:
        print("No human detected.")
        return None, None

# Calculate the difference in pixels between the highest point and left heel
def calculate_pixel_difference(image_path, outline_image_path):
    highest_point, lowest_point, _ = extract_human_outline_mediapipe(image_path, outline_image_path)
    if highest_point is None:
        print("Could not detect the highest point.")
        return

    feet_x, feet_y, shoulder_length_pixels = get_feet_coordinates(image_path)
    if feet_x is None or feet_y is None:
        print("Could not detect the left heel coordinates.")
        return

    print(f"Highest Point: {highest_point} (x={highest_point[0]}, y={highest_point[1]})")
    print(f"Lowest Point: {lowest_point} (x={lowest_point[0]}, y={lowest_point[1]})")
    print(f"Left Heel Coordinates: x={feet_x}, y={feet_y}")
    print(f"Shoulder diff in pixels: {shoulder_length_pixels}")

    

    # Calculate the pixel difference between the highest point and left heel
    diff_x = feet_x - highest_point[0]
    diff_y = feet_y - highest_point[1]
    diff_pixels = math.sqrt(diff_x ** 2 + diff_y ** 2)

    print(f"Difference in X: {diff_x} pixels")
    print(f"Difference in Y: {diff_y} pixels")
    print(f"Euclidean Pixel Difference: {diff_pixels:.2f} pixels")
    pixels_per_inch = diff_pixels / 66

    shoulder_length_inches = shoulder_length_pixels / pixels_per_inch
    print(f"Shoulder Length: {shoulder_length_inches} inches")

    # Annotate and visualize the points on the image
    image = cv2.imread(image_path)
    cv2.circle(image, tuple(highest_point), 5, (0, 255, 0), -1)  # Green for highest
    cv2.circle(image, tuple(lowest_point), 5, (0, 255, 0), -1)  # Green for highest
    cv2.circle(image, (feet_x, feet_y), 5, (0, 0, 255), -1)  # Red for left heel
    cv2.putText(image, f"Shoulder Length: {shoulder_length_inches:.2f} inches", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) 

    # Save or display the annotated image
    cv2.imshow("Annotated Image", image)
    cv2.imwrite("annotated_image_with_points.png", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return shoulder_length_inches

# Example usage
input_image = "sethu_front.png"
outline_image = "human_outline_mediapipe.png"

shoulder_length = calculate_pixel_difference(input_image, outline_image)
if shoulder_length:
    print(f"Shoulder Length: {shoulder_length:.2f} inches")
