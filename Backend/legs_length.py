import cv2
import numpy as np
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

def get_arm_and_leg_coordinates(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print("No pose landmarks detected!")
        return None, None, None, None, None

    landmarks = results.pose_landmarks.landmark
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
    
    right_wrist_coords = (int(right_wrist.x * image_width), int(right_wrist.y * image_height))
    left_wrist_coords = (int(left_wrist.x * image_width), int(left_wrist.y * image_height))
    right_shoulder_coords = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))
    left_shoulder_coords = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
    left_ankle_coords = (int(left_ankle.x * image_width), int(left_ankle.y * image_height))
    right_ankle_coords = (int(right_ankle.x * image_width), int(right_ankle.y * image_height))

    wrist_to_ankle_right_pixels = math.sqrt((right_wrist_coords[0] - right_ankle_coords[0]) ** 2 + 
                                              (right_wrist_coords[1] - right_ankle_coords[1]) ** 2)
    wrist_to_ankle_left_pixels = math.sqrt((left_wrist_coords[0] - left_ankle_coords[0]) ** 2 + 
                                             (left_wrist_coords[1] - left_ankle_coords[1]) ** 2)

    return right_shoulder_coords, left_shoulder_coords, right_wrist_coords, left_wrist_coords, right_ankle_coords, left_ankle_coords, wrist_to_ankle_right_pixels, wrist_to_ankle_left_pixels

def extract_human_outline_mediapipe(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load the image.")
        return None, None, None, None

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

        print(f"Topmost Pixel: ({topmost_x}, {topmost_y})")
        print(f"Bottommost Pixel: ({bottommost_x}, {bottommost_y})")

        return top_pixel, bottom_pixel, edges, mask
    else:
        print("Segmentation failed.")
        return None, None, None, None

def get_hip_coordinates(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print("No pose landmarks detected!")
        return None, None

    landmarks = results.pose_landmarks.landmark
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    left_hip_coords = (int(left_hip.x * image_width), int(left_hip.y * image_height))
    right_hip_coords = (int(right_hip.x * image_width), int(right_hip.y * image_height))

    return left_hip_coords, right_hip_coords

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

def calculate_legs_length(image_path, height):
    top_pixel, bottom_pixel, edges, mask = extract_human_outline_mediapipe(image_path)
    if top_pixel is None:
        print("Could not detect the highest point.")
        return
    if edges is None:
        print("Outline extraction failed.")
        return

    left_shoulder_coords, right_shoulder_coords, left_wrist_coords, right_wrist_coords, left_ankle_coords, right_ankle_coords, wrist_to_ankle_right_pixels, wrist_to_ankle_left_pixels = get_arm_and_leg_coordinates(image_path)
    
    if left_ankle_coords is None or right_ankle_coords is None:
        print("Could not detect the ankle coordinates.")
        return

    diff_x = bottom_pixel[0] - top_pixel[0]
    diff_y = bottom_pixel[1] - top_pixel[1]
    diff_pixels = math.sqrt(diff_x ** 2 + diff_y ** 2)
    pixels_per_inch = diff_pixels / height

    wrist_to_ankle_right_inches = (wrist_to_ankle_right_pixels / pixels_per_inch) + 8

    return wrist_to_ankle_right_inches 