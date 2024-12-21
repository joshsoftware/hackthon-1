import cv2
import numpy as np

# Load the image (Make sure the image is in a path you specify)
img = cv2.imread('human_outline_mediapipe.png')

# Get the height, width, and channels of the image
height, width, channels = img.shape

# Output the height and width
print(f"Height: {height} pixels")
print(f"Width: {width} pixels")

# Convert the image to grayscale to detect outlines
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold to get binary image (assuming the outline is black and background is white)
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find the coordinates of non-white (colored) pixels
colored_pixels = np.column_stack(np.where(binary == 0))  # 0 means black, outline color

# Get the topmost and bottommost pixels
topmost = colored_pixels[colored_pixels[:, 0].argmin()]
bottommost = colored_pixels[colored_pixels[:, 0].argmax()]

print(f"Lowest Y: {bottommost} and Highest Y: {topmost}")

# Calculate the difference in pixels
pixel_diff = bottommost[0] - topmost[0]

# Mark the topmost and bottommost pixels in the original image
cv2.circle(img, (topmost[1], topmost[0]), 5, (0, 0, 255), -1)  # Red circle for topmost
cv2.circle(img, (bottommost[1], bottommost[0]), 5, (0, 255, 0), -1)  # Green circle for bottommost

# Draw a line connecting the topmost and bottommost pixels
cv2.line(img, (topmost[1], topmost[0]), (bottommost[1], bottommost[0]), (255, 0, 0), 2)

# Display the result
cv2.imshow('Marked Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Optionally save the result to a file
cv2.imwrite('marked_image.png', img)

# Output the pixel difference
print(f"The pixel difference (in pixels) is: {pixel_diff}")
