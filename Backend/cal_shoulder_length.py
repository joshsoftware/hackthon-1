import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False)

def calculate_shoulder_length(image_path, person_height_feet):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        print("No pose landmarks detected!")
        return None

    landmarks = results.pose_landmarks.landmark
    head = landmarks[mp_pose.PoseLandmark.NOSE.value]
    feet = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    head_y = int(head.y * image_height)
    feet_y = int(feet.y * image_height)
    left_shoulder_coords = (int(left_shoulder.x * image_width), int(left_shoulder.y * image_height))
    right_shoulder_coords = (int(right_shoulder.x * image_width), int(right_shoulder.y * image_height))

    person_height_pixels = abs(feet_y - head_y)

    person_height_inches = person_height_feet * 12

    pixels_per_inch = person_height_pixels / person_height_inches


    shoulder_length_pixels = ((right_shoulder_coords[0] - left_shoulder_coords[0]) ** 2 + 
                              (right_shoulder_coords[1] - left_shoulder_coords[1]) ** 2) ** 0.5

    shoulder_length_inches = shoulder_length_pixels / pixels_per_inch

    annotated_image = image.copy()
    cv2.circle(annotated_image, left_shoulder_coords, 5, (0, 255, 0), -1)
    cv2.circle(annotated_image, right_shoulder_coords, 5, (0, 255, 0), -1)
    cv2.line(annotated_image, left_shoulder_coords, right_shoulder_coords, (255, 0, 0), 2)
    cv2.putText(annotated_image, f"Shoulder Length: {shoulder_length_inches:.2f} inches", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imwrite('annotated_image.jpg', annotated_image)
    cv2.imshow('Annotated Image', annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return shoulder_length_inches

image_path = 'images/vinay-front-cropped.jpg'
person_height_feet = 5.6
shoulder_length = calculate_shoulder_length(image_path, person_height_feet)

if shoulder_length:
    print(f"Shoulder Length: {shoulder_length:.2f} inches")
