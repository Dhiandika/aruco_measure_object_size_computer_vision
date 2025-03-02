import cv2
import numpy as np

# Global variables for mouse callback
points = []
click_count = 0
aruco_corners = []
object_corners = []

def select_points(event, x, y, flags, param):
    global points, click_count, aruco_corners, object_corners

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        click_count += 1
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Image", img)

        if click_count == 4:
            aruco_corners = np.array(points, dtype=np.int32)
            cv2.polylines(img, [aruco_corners], True, (0, 255, 0), 2)
            cv2.imshow("Image", img)
        elif click_count == 8:
            object_corners = np.array(points[4:], dtype=np.int32)
            cv2.polylines(img, [object_corners], True, (255, 0, 0), 2)
            cv2.imshow("Image", img)

# Load Image
img = cv2.imread('phone_aruco_marker.jpg')
cv2.imshow("Image", img)
cv2.setMouseCallback("Image", select_points)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ensure we have exactly eight points selected
if click_count != 8:
    raise ValueError("Please select exactly eight points: four for the ArUco marker and four for the object.")

# Calculate ArUco perimeter
aruco_perimeter = cv2.arcLength(aruco_corners, True)
pixel_cm_ratio = aruco_perimeter / 20

# Calculate width and height of the object in cm
rect = cv2.minAreaRect(object_corners)
(x, y), (w, h), angle = rect
object_width = w / pixel_cm_ratio
object_height = h / pixel_cm_ratio

# Display dimensions on the image
cv2.putText(img, f"Width: {round(object_width, 1)} cm", (int(x), int(y - 10)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
cv2.putText(img, f"Height: {round(object_height, 1)} cm", (int(x), int(y + 10)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

# Show the final image
cv2.imshow("Final Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
