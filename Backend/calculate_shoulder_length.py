import cv2
import numpy as np
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

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

        return top_pixel, bottom_pixel, edges, mask
    else:
        print("Segmentation failed.")
        return None, None

def find_farthest_edges(edges, left_shoulder, right_shoulder):
    height, width = edges.shape
    
    left_x = left_shoulder[0]
    left_y = left_shoulder[1]
    for x in range(left_x, -1, -1):
        if edges[left_y, x] > 0:
            leftmost = {"leftmost_x": x, "leftmost_y": left_y}
            break
    else:
        leftmost = {"leftmost_x": left_x, "leftmost_y": left_y}

    right_x = right_shoulder[0]
    right_y = right_shoulder[1]
    for x in range(right_x, width):
        if edges[right_y, x] > 0:
            rightmost = {"rightmost_x": x, "rightmost_y": right_y}
            break
    else:
        rightmost = {"rightmost_x": right_x, "rightmost_y": right_y}

    return leftmost, rightmost

def calculate_shoulder_length(image_path, user_height):
    top_pixel, bottom_pixel, edges, mask = extract_human_outline_mediapipe(image_path)
    if top_pixel is None:
        print("Could not detect the highest point.")
        return
    if edges is None:
        print("Outline extraction failed.")
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


    left_edge, right_edge = find_farthest_edges(edges, left_shoulder_coords, right_shoulder_coords)
    
    farthest_length_pixels = ((right_edge['rightmost_x'] - left_edge['leftmost_x'])**2 + 
                    (right_edge['rightmost_y'] - left_edge['leftmost_y'])**2) ** 0.5
    
    farthest_length_media_inches = farthest_length_pixels / pixels_per_inch

    return farthest_length_media_inches