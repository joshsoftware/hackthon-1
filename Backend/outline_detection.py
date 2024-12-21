import cv2
import mediapipe as mp
import numpy as np

def extract_user_outline(image_path, output_path):
    # Step 1: Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load the image.")
        return
    original = image.copy()

    # Step 2: Convert image to RGB (required by MediaPipe)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 3: Initialize MediaPipe for segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    # Step 4: Process the image to get the segmentation mask
    results = selfie_segmentation.process(rgb_image)

    # Step 5: Create a binary mask where the person is highlighted
    mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255

    # Step 6: Apply Canny Edge Detection to get the outline
    edges = cv2.Canny(mask, threshold1=50, threshold2=150)

    # Step 7: Save and display the result
    cv2.imwrite(output_path, edges)
    print(f"User outline saved as '{output_path}'")

    # Display the images
    cv2.imshow("Original Image", original)
    cv2.imshow("User Outline", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
input_image = "vinay_front.jpg"  # Replace with the path to your input image
output_image = "user_outline.png"
extract_user_outline(input_image, output_image)
