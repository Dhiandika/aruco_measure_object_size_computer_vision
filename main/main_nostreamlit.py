# ---------------------
# Import Library System
# ---------------------
import json
import os

# -----------------------------------
# Import Library Proses Gambar dan UI
# -----------------------------------
import cv2
import numpy as np


# ----------
# Kode Class
# ----------
# Kelas untuk deteksi background polos
class HomogeneousBgDetector():
    # Inisialisasi Kelas
    def __init__(self):
        pass

    # Method deteksi objek
    def detect_objects(self, frame, namaframe):

        # Window cv2
        window_name = f"{namaframe}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)

        # Convert gambar ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Buat mask dengan adaptive threshold
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
        cv2.imshow(window_name, mask)

        # Temukan contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Tampilkan mask
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                # cnt = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                objects_contours.append(cnt)

        return objects_contours


# -------------
# Kode Function
# -------------
# Fungsi untuk membuka kamera berdasarkan IP atau ID kamera
def jenis_kamera(ip):
    # Jika terdapat IP, gunakan IP kamera
    if ip != "/video":
        cap = cv2.VideoCapture(ip)
    # Jika IP kosong, gunakan kamera utama
    else:
        cap = cv2.VideoCapture(0)
    # Jika kamera tidak berhasil terbuka
    if not cap.isOpened():
        print("Tidak dapat membuka kamera.")
        return None
    # Kembalikan objek kamera
    return cap


# Fungsi untuk mendeteksi aruco marker
def deteksi_aruco(img, aruco_dict, parameters):
    # Deteksi aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    # Jika aruco marker terdeteksi
    if corners:
        # Ubah koordinat pixel ke Integer
        int_corners = np.intp(corners)
        # Bentuk polygon dari kotak Aruco
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
        # Aruco Marker dengan keliling 20 cm (5cm)
        aruco_perimeter = cv2.arcLength(corners[0], True) / 20
        # Kembalikan skala Aruco
        return aruco_perimeter  # Pixel to cm ratio
    # Jika aruco tidak terdeteksi
    return None


# Fungsi untuk deteksi objek
def deteksi_objek(img, pixel_cm_ratio, namaframe):
    # List untuk menyimpan deteksi objek
    objek = []
    # Deteksi objek dalam gambar
    contours = detector.detect_objects(img, namaframe)
    # Mengambar boundaries objek
    for cnt in contours:
        # Mendapatkan bounding box dari objek
        rect = cv2.minAreaRect(cnt)
        # Mendapatkan detail koordinat, ukuran, dan kemiringan dari bounding box
        (x, y), (w, h), angle = rect
        # Convert pixel ke dalam bentuk centimeter
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio
        # Menampilkan bounding box
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # Menambahkan deteksi objek ke list
        objek.append((box, object_width, object_height))
        # Untuk menampilkan titik tengah deteksi
        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        # Untuk menampilkan garis tepi deteksi objek
        cv2.polylines(img, [box], True, (255, 0, 0), 2)
        # Untuk menambahkan teks pada deteksi objek
        cv2.putText(img, f"Width {round(object_width, 2)} cm", (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2,
                    (100, 200, 0), 2)
        cv2.putText(img, f"Height {round(object_height, 2)} cm", (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2,
                    (100, 200, 0), 2)
    # Mengembalikan list deteksi objek
    return objek


# Fungsi untuk menyimpan ukuran deteksi objek
def simpan_ukuran(objek1, objek2, filename="ukuran_benda.json"):
    total_width = 0
    total_height = 0
    total_length = 0
    count = 0

    for (box1, width1, height1), (box2, width2, height2) in zip(objek1, objek2):
        total_width += width1
        total_height += height1
        total_length += width2  # Assuming length is the width of the second camera's object
        count += 1

    if count > 0:
        average_width = round(total_width / count, 2)
        average_height = round(total_height / count, 2)
        average_length = round(total_length / count, 2)

        data = {
            "width": average_width,
            "height": average_height,
            "length": average_length
        }

        with open(filename, "w") as f:
            json.dump(data, f)

        print(f"Ukuran objek berhasil disimpan ke {filename}")

        # Baca dan tampilkan data dari file JSON
        ukuran_baca = baca_ukuran(filename)
        if ukuran_baca:
            print("Hasil Ukuran Objek:")
            print(f"Width: {ukuran_baca['width']} cm")
            print(f"Height: {ukuran_baca['height']} cm")
            print(f"Length: {ukuran_baca['length']} cm")
    else:
        print("Tidak ada objek yang terdeteksi untuk disimpan.")


def baca_ukuran(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None


# -------------------
# Load detektor objek
# -------------------
# Load Aruco detector
parameters = cv2.aruco.DetectorParameters()
# Load Jenis Aruco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
# Load Object Detector
detector = HomogeneousBgDetector()

# Setting Kamera
scan_count = 0
max_scans = 99999999999999999
# List untuk menyimpan ukuran deteksi objek
ukuran_benda = []

# Define IP cameras here
ip_camera1 = "http://192.168.1.102:8080" + "/video"
ip_camera2 = "http://192.168.1.102:8080" + "/video"

# Buka kamera
cap1 = jenis_kamera(ip_camera1)
cap2 = jenis_kamera(ip_camera2)

# Jika kamera 1 dan kamera 2 berhasil dibuka
if cap1 and cap2:

    # Jika scan belum 10 kali
    while scan_count < max_scans:
        # Ambil frame kamera 1 dan 2
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()
        # Jika frmae salah satu kamera gagal diambil
        if not ret1 or not ret2:
            print("Gagal menangkap gambar.")
            break
        # Ambil rasio Aruco
        pixel_cm_ratio1 = deteksi_aruco(img1, aruco_dict, parameters)
        pixel_cm_ratio2 = deteksi_aruco(img2, aruco_dict, parameters)
        # Jika kedua rasio Aruco berhasil diambil
        if pixel_cm_ratio1 and pixel_cm_ratio2:
            # Deteksi Objeknya dengan rasio Aruco terdeteksi
            objek1 = deteksi_objek(img1, pixel_cm_ratio1, 1)
            objek2 = deteksi_objek(img2, pixel_cm_ratio2, 2)
            # Jika kedua objek terdeteksi
            if objek1 and objek2:
                # Tambahkan ukuran deteksi kedua objek ke list
                ukuran_benda.append((objek1, objek2))
                # Tambah hitungan scan
                scan_count += 1

                for (box1, width1, height1), (box2, width2, height2) in zip(objek1, objek2):
                    cv2.putText(img1, f"Combined Width {round(width1, 2)} cm", (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                                (100, 200, 0), 2)
                    cv2.putText(img1, f"Combined Height {round(height2, 2)} cm", (10, 100), cv2.FONT_HERSHEY_PLAIN,
                                2, (100, 200, 0), 2)
                    cv2.putText(img1, f"Length {round(width2, 2)} cm", (10, 150), cv2.FONT_HERSHEY_PLAIN, 2,
                                (100, 200, 0), 2)

        # Window Cv2
        window_name1 = "Kamera 1"
        window_name2 = "Kamera 2"
        cv2.namedWindow(window_name1, cv2.WINDOW_NORMAL)
        cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name1, 640, 480)
        cv2.resizeWindow(window_name2, 640, 480)
        cv2.imshow(window_name1, img1)
        cv2.imshow(window_name2, img2)

        # Tampilkan dengan cv2
        cv2.imshow("Kamera 1", img1)
        cv2.imshow("Kamera 2", img2)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Jika scan sudah 10 kali maka stop
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

    # Simpan ukuran ke file JSON setelah 10 kali scan
    if scan_count >= max_scans:
        # Gabungkan semua objek yang ditemukan menjadi satu daftar
        all_objek1 = [obj for obj1, _ in ukuran_benda for obj in obj1]
        all_objek2 = [obj for _, obj2 in ukuran_benda for obj in obj2]
        simpan_ukuran(all_objek1, all_objek2)
