import cv2
import mediapipe as mp
import numpy as np

def extract_human_outline_mediapipe(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load the image.")
        return

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

        # Save the result
        cv2.imwrite(output_path, edges)
        print(f"Human outline saved as '{output_path}'")

        cv2.imshow("Human Outline", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No human detected.")

# Example usage
input_image = "sethu_front.jpg"
output_image = "human_outline_mediapipe.png"
extract_human_outline_mediapipe(input_image, output_image)
