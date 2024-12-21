import cv2
import numpy as np

def detect_human_outline(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Load the Mask R-CNN pre-trained model from OpenCV
    net = cv2.dnn.readNetFromTensorflow("frozen_inference_graph.pb", "mask_rcnn.pbtxt")

    # Create blob and set input to the network
    blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
    net.setInput(blob)

    # Forward pass to get results
    boxes, masks = net.forward(["detection_out_final", "detection_masks"])

    # Loop through detections and find human class (typically class 1)
    num_detections = boxes.shape[2]
    for i in range(num_detections):
        box = boxes[0, 0, i]
        class_id = int(box[1])
        score = box[2]

        # Ensure detection is for a human and score is above a threshold
        if class_id == 1 and score > 0.5:
            # Extract box coordinates
            x1, y1, x2, y2 = (box[3:] * [width, height, width, height]).astype(int)
            
            # Extract mask and apply threshold
            mask = masks[i, class_id]
            mask_resized = cv2.resize(mask, (x2 - x1, y2 - y1))
            mask_binary = (mask_resized > 0.5).astype(np.uint8) * 255
            
            # Create full-size mask and overlay it on the original image
            full_mask = np.zeros((height, width), dtype=np.uint8)
            full_mask[y1:y2, x1:x2] = mask_binary

            # Detect edges using Canny
            edges = cv2.Canny(full_mask, 100, 200)

            # Save the result and display
            cv2.imwrite(output_path, edges)
            cv2.imshow("Human Outline", edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return

# Example usage
input_image = "sethu_front.jpg"  # Path to your input image
output_image = "human_outline.png"
detect_human_outline(input_image, output_image)
