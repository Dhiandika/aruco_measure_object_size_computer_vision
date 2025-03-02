# Import Library yang diperlukan
import cv2
import numpy as np

# Kelas Untuk Deteksi Background Polos
class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert Image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("a", gray)

        # Create a Mask with adaptive threshold
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("mask", mask)
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                #cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)

        print(len(objects_contours))
        return objects_contours

    def get_objects_rect(self):
        box = cv2.boxPoints(rect)  # cv2.boxPoints(rect) for OpenCV 3.x
        box = np.int0(box)

# Load Aruco Detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

# Menload Object Detector
detector = HomogeneousBgDetector()

# Load Image
img = cv2.imread('phone_aruco_marker.jpg')

# Get Aruco marker
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
# print(corners)

# Draw polygon around the marker
int_corners = np.int0(corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

# Aruco Perimeter
aruco_perimiter = cv2.arcLength(corners[0], True)
# print(aruco_perimiter)

# Pixel to CM ratio
pixel_cm_ratio = aruco_perimiter / 20
# print(pixel_cm_ratio)

contours = detector.detect_objects(img)
# print(contours)
# print(f'panjangnya {len(contours)}')

# Draw objects boundaries
for cnt in contours:
    # Draw polygon
    # cv2.polylines(img, [cnt], True, (255,0,0), 2)

    # Get rect
    # (x,y), (w,h), angle = cv2.minAreaRect(cnt)
    rect = cv2.minAreaRect(cnt)
    (x,y), (w,h), angle = rect

    # Get width height of object by apply ratio pixel to cm
    object_width = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio

    # Display rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.circle(img, (int(x),int(y)), 5, (0,0,255), -1)
    cv2.polylines(img, [box], True, (255,0,0), 1)
    cv2.putText(img, f"Width {round(object_width, 1)} cm", (int(x-100), int(y-15)), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
    cv2.putText(img, f"Width {round(object_height, 1)} cm", (int(x-100), int(y+15)), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)

    # print(box)
    # print(x,y)
    # print(w,h)
    # print(angle)

cv2.imshow("Image", img)
cv2.waitKey(0)