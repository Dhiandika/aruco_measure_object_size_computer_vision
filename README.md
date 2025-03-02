# Aruco Measure Object Size Computer Vision
*   [Repository Master [denisikiandani/ComputerVision-3d_Object_Detector]](https://github.com/denisikiandani/ComputerVision-3d_Object_Detector.git): Ini adalah Repository Kelompok Dari Matakuliah Visi Komputer.
*   
---
 
Proyek ini mendemonstrasikan cara mengukur ukuran objek 3D menggunakan marker ArUco dan teknik visi komputer.  Menggunakan kamera, proyek ini mendeteksi marker ArUco, menghitung pose (posisi dan orientasi) marker, dan kemudian memanfaatkan informasi tersebut untuk memperkirakan dimensi objek yang ditempatkan di dekat atau di atas marker.

## Refrensi


https://github.com/user-attachments/assets/44b9caff-ecde-4d76-b0c1-96e0773c5530


## Deskripsi
Proyek ini menyediakan implementasi langkah demi langkah untuk mengukur ukuran objek 3D dengan menggunakan marker ArUco dan visi komputer. Cara kerja:
| Gambaran        | Gambaran        |
| ------------- | ------------- |
| ![Gambar 1](image/Figure%206.png) ![Gambar 2](image/Figure%2010.png) | ![Gambar 3](image/Picture1.png) ![Gambar 3](image/Picture2.jpg)  |
*   **Deteksi Marker ArUco:** Mendeteksi marker ArUco dalam frame kamera.
*   **Estimasi Pose:** Menghitung posisi dan orientasi marker ArUco relatif terhadap kamera.
*   **Perhitungan Ukuran Objek:** Memperkirakan dimensi objek berdasarkan pose marker dan pengetahuan tentang ukuran marker.
*   **Visualisasi:** Menampilkan hasil pengukuran pada frame kamera.

---
## Hasil


## Libary 
*   **opencv-python:** Library OpenCV untuk Python.
*   **numpy:** Library NumPy untuk komputasi numerik.
*   **streamlit:** Library Streamlit untuk membuat aplikasi web interaktif.
*   **bpy:** Library Python untuk Blender. Ini diasumsikan sebagai instalasi Blender yang sesuai dan konfigurasi variabel lingkungan yang benar untuk Python agar dapat mengakses Blender.
