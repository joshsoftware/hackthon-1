import cv2
import numpy as np
import mediapipe as mp
import math

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

# Function to Get Shoulder and Hip Coordinates
def get_shoulder_hip_coordinates(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print("No pose landmarks detected!")
        return None, None

    landmarks = results.pose_landmarks.landmark
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]

    left_shoulder_coords = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
    left_hip_coords = (int(left_hip.x * image_width), int(left_hip.y * image_height))

    return left_shoulder_coords, left_hip_coords

# Function to Extract Human Outline and Find Chest Points
def extract_human_outline_and_chest_points(image_path, left_shoulder, left_hip):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    # Process the image to get segmentation mask
    results = selfie_segmentation.process(rgb_image)

    if results.segmentation_mask is not None:
        mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255
        edges = cv2.Canny(mask, threshold1=50, threshold2=150)

        # Extract coordinates of edge points
        y_coords, x_coords = np.nonzero(edges)

        # Calculate 1/4 distance from shoulder to hip
        one_fourth_x = int(left_shoulder[0] + 0.25 * (left_hip[0] - left_shoulder[0]))
        one_fourth_y = int(left_shoulder[1] + 0.25 * (left_hip[1] - left_shoulder[1]))

        # Find farthest left point from the shoulder
        max_distance_left = 0
        farthest_left_point = None
        for x, y in zip(x_coords, y_coords):
            if abs(y - one_fourth_y) <= 10:  # Restrict points near 1/4 region
                distance = abs(x - left_shoulder[0])
                if distance > max_distance_left:
                    max_distance_left = distance
                    farthest_left_point = (x, y)

        # Find farthest right point on the same y-axis as farthest_left_point
        max_distance_right = 0
        farthest_right_point = None
        if farthest_left_point:
            leftmost_x, leftmost_y = farthest_left_point
            for x, y in zip(x_coords, y_coords):
                if abs(y - leftmost_y) <= 2 and x > leftmost_x:  # Same y-axis with tolerance
                    distance = x - leftmost_x
                    if distance > max_distance_right:
                        max_distance_right = distance
                        farthest_right_point = (x, y)

        return farthest_left_point, farthest_right_point, edges, mask
    else:
        print("Segmentation failed.")
        return None, None, None, None

def extract_outline(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe Selfie Segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    # Process the image to get segmentation mask
    results = selfie_segmentation.process(rgb_image)

    if results.segmentation_mask is not None:
        mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255
        edges = cv2.Canny(mask, threshold1=50, threshold2=150)
        return edges
    else:
        print("Segmentation failed.")
        return None


def get_shoulder_coordinates(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print("No pose landmarks detected!")
        return None, None

    landmarks = results.pose_landmarks.landmark
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    feet = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
    
    left_shoulder_coords = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
    right_shoulder_coords = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))

    feet_x = int(feet.x * image_width)
    feet_y = int(feet.y * image_height)
    shoulder_length_pixels = ((right_shoulder_coords[0] - left_shoulder_coords[0]) ** 2 + 
                              (right_shoulder_coords[1] - left_shoulder_coords[1]) ** 2) ** 0.5


    return left_shoulder_coords, right_shoulder_coords, feet_x, feet_y, shoulder_length_pixels

def extract_human_outline_mediapipe(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load the image.")
        return None, None

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    results = selfie_segmentation.process(rgb_image)

    if results.segmentation_mask is not None:
        mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255
        edges = cv2.Canny(mask, threshold1=50, threshold2=150)

        y_coords, x_coords = np.nonzero(edges)

        topmost_y = np.min(y_coords)
        bottommost_y = np.max(y_coords)

        topmost_x = x_coords[np.argmin(y_coords)]
        bottommost_x = x_coords[np.argmax(y_coords)]

        top_pixel = [int(topmost_x), int(topmost_y)]
        bottom_pixel = [int(bottommost_x), int(bottommost_y)]

        return top_pixel, bottom_pixel
    else:
        print("Segmentation failed.")
        return None, None
def find_intersection_on_second_image(outline_image_path, chest_y, pixel_per_inch):
    # Extract outline for second image
    edges = extract_outline(outline_image_path)
    if edges is None:
        print("Failed to extract outline from second image.")
        return None, None
    
    # Extract edge coordinates
    y_coords, x_coords = np.nonzero(edges)

    # Read the second image for visualization
    image = cv2.imread(outline_image_path)

    # Initialize variables for intersection points
    farthest_left = None
    farthest_right = None

    # Find the farthest left and right points along the chest_y axis
    for x, y in zip(x_coords, y_coords):
        if abs(y - chest_y) <= 2:  # Tolerance around chest y-coordinate
            if farthest_left is None or x < farthest_left[0]:
                farthest_left = (x, y)
            if farthest_right is None or x > farthest_right[0]:
                farthest_right = (x, y)

    # Highlight intersection points
    if farthest_left:
        cv2.circle(image, farthest_left, 5, (0, 0, 255), -1)  # Red dot for leftmost intersection
    if farthest_right:
        cv2.circle(image, farthest_right, 5, (0, 0, 255), -1)  # Red dot for rightmost intersection

    # Draw line along the intersection points
    if farthest_left and farthest_right:
        cv2.line(image, farthest_left, farthest_right, (0, 255, 0), 2)  # Green line
        
        # Calculate distance between the farthest points
        distance_pixels = math.sqrt((farthest_right[0] - farthest_left[0])**2 +
                                    (farthest_right[1] - farthest_left[1])**2)
        distance_inches = distance_pixels / pixel_per_inch
        print(f"Distance between intersection points: {distance_inches:.2f} inches")

        # Display the result
        cv2.imshow("Intersection Result", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return distance_inches, image
    return None, None
# Main Function
def calculate_chest_length(image_path, outline_image_path, user_height):
    # Get Shoulder and Hip Coordinates
    left_shoulder_coords, left_hip_coords = get_shoulder_hip_coordinates(image_path)
    if not left_shoulder_coords or not left_hip_coords:
        print("Could not detect shoulder or hip coordinates.")
        return

    top_pixel, bottom_pixel = extract_human_outline_mediapipe(image_path)
    if top_pixel is None:
        print("Could not detect the highest point.")
        return

    left_shoulder_coords, right_shoulder_coords, feet_x, feet_y, shoulder_length_pixels = get_shoulder_coordinates(image_path)
    if feet_x is None or feet_y is None:
        print("Could not detect the left heel coordinates.")
        return
    if left_shoulder_coords is None or right_shoulder_coords is None:
        print("Shoulder detection failed.")
        return

    diff_x = feet_x - top_pixel[0]
    diff_y = feet_y - top_pixel[1]
    diff_pixels = math.sqrt(diff_x ** 2 + diff_y ** 2)
    pixels_per_inch = diff_pixels / user_height
    # Extract Human Outline and Find Chest Points
    farthest_left_point, farthest_right_point, edges, mask = extract_human_outline_and_chest_points(
        image_path, left_shoulder_coords, left_hip_coords
    )
    if farthest_left_point is None or farthest_right_point is None:
        print("Could not find chest points.")
        return
    chest_y = farthest_left_point[1]
    
    chest_distance_pixels = math.sqrt(
        (farthest_right_point[0] - farthest_left_point[0])**2 +
        (farthest_right_point[1] - farthest_left_point[1])**2
    )
    chest_distance_inches = ( chest_distance_pixels / pixel_per_inch ) - 5
    print(f"Distance between chest points: {chest_distance_inches:.2f} inches")
    
    # Process second image for intersection
    intersection_distance_inches, _ = find_intersection_on_second_image(outline_image_path, chest_y, pixel_per_inch)
    
    if intersection_distance_inches:
        # Calculate circumference using average width formula
        circumference = math.pi * (chest_distance_inches + intersection_distance_inches)
        print(f"Estimated Circumference: {circumference/2:.2f} inches")
        return circumference/2
    return 0


    # Visualize the Results
    # image = cv2.imread(image_path)
    # cv2.circle(image, left_shoulder_coords, 5, (255, 0, 0), -1)  # Blue for left shoulder
    # cv2.circle(image, left_hip_coords, 5, (0, 255, 0), -1)  # Green for left hip
    # cv2.circle(image, farthest_left_point, 5, (0, 0, 255), -1)  # Red for farthest left chest point
    # cv2.circle(image, farthest_right_point, 5, (255, 255, 0), -1)  # Yellow for farthest right chest point

    # # Draw a line along the X-axis of chest points
    # cv2.line(image, farthest_left_point, farthest_right_point, (255, 255, 0), 3)  # Yellow line

    # # Show the image with markings
    # cv2.imshow("Result", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
