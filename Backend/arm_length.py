import cv2
import numpy as np
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

def get_arm_coordinates(image_path):
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
    
    # Convert the coordinates to pixel values
    left_shoulder_coords = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
    left_wrist_coords = (int(left_wrist.x * image_width), int(left_wrist.y * image_height))
    right_shoulder_coords = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))
    right_wrist_coords = (int(right_wrist.x * image_width), int(right_wrist.y * image_height))

    # Calculate the arm length in pixels (distance from shoulder to wrist)
    arm_length_right_pixels = math.sqrt((right_shoulder_coords[0] - right_wrist_coords[0]) ** 2 + 
                                         (right_shoulder_coords[1] - right_wrist_coords[1]) ** 2)
    arm_length_left_pixels = math.sqrt((left_shoulder_coords[0] - left_wrist_coords[0]) ** 2 + 
                                        (left_shoulder_coords[1] - left_wrist_coords[1]) ** 2)

    return left_shoulder_coords, left_wrist_coords, right_shoulder_coords, right_wrist_coords, arm_length_right_pixels, arm_length_left_pixels

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

def main(image_path):
    top_pixel, bottom_pixel, edges, mask = extract_human_outline_mediapipe(image_path)
    if top_pixel is None:
        print("Could not detect the highest point.")
        return
    if edges is None:
        print("Outline extraction failed.")
        return

    left_shoulder_coords, left_wrist_coords, right_shoulder_coords, right_wrist_coords, arm_length_right_pixels, arm_length_left_pixels = get_arm_coordinates(image_path)
    
    if left_shoulder_coords is None or right_shoulder_coords is None:
        print("Shoulder detection failed.")
        return

    diff_x = bottom_pixel[0] - top_pixel[0]
    diff_y = bottom_pixel[1] - top_pixel[1]
    diff_pixels = math.sqrt(diff_x ** 2 + diff_y ** 2)
    pixels_per_inch = diff_pixels / 66

    # Convert arm length to inches
    arm_length_right_inches = (arm_length_right_pixels / pixels_per_inch) + 4
    arm_length_left_inches = (arm_length_left_pixels / pixels_per_inch) + 4

    print(f"Right Arm Length: {arm_length_right_inches} inches")
    print(f"Left Arm Length: {arm_length_left_inches} inches")

    # Display the image with arm length text
    image = cv2.imread(image_path)
    cv2.putText(image, f"Right Arm Length: {arm_length_right_inches:.2f} inches", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, f"Left Arm Length: {arm_length_left_inches:.2f} inches", 
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main("nikhil_front.jpg")
