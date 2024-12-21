import cv2
import numpy as np

def extract_edges_and_separate_background(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    # Create a mask from edges
    edges_dilated = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
    mask = cv2.bitwise_not(edges_dilated)

    # Separate background
    background = cv2.bitwise_and(image, image, mask=mask)

    # Combine edges with transparency for visualization
    edges_colored = cv2.merge((edges, edges, edges))
    edges_with_transparency = np.zeros_like(image)
    edges_with_transparency[edges > 0] = [255, 255, 255]  # White edges

    # Save the results
    cv2.imwrite(f"{output_path}_edges.jpg", edges)
    cv2.imwrite(f"{output_path}_background.jpg", background)

    print(f"Edges saved to {output_path}_edges.jpg")
    print(f"Background saved to {output_path}_background.jpg")

# Usage
image_path = "vinay_front.jpg"  # Replace with your image path
output_path = "output"          # Replace with desired output base name
extract_edges_and_separate_background(image_path, output_path)