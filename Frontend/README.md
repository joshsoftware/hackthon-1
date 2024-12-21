# **Body Measurement App for Tailoring**

A Flutter-based mobile app that allows users to take photos in specific poses, processes the images on a backend server using advanced machine learning models, and provides accurate body measurements for custom tailoring. The app ensures a seamless, secure, and user-friendly experience.

---

## **Features**
- **Photo Capture**: Guides users to capture images in specific poses for accurate measurements.  
- **Server-side Processing**: Images are uploaded to a secure backend for processing using advanced ML models.  
- **Measurement Extraction**: Fetches and calculates key body measurements such as:  
  - Shoulder Width  
  - Chest/Bust Circumference  
  - Waist Circumference  
  - Hip Circumference  
  - Inseam Length (for pants)  
- **Real-Time Feedback**: Displays measurement results in a clean and user-friendly interface.  
  

---

## **Tech Stack**

### **Frontend**
- **Framework**: Flutter (Dart)  
- **Libraries**:  
  - `camera` (for capturing images)  
  - `image_picker` (optional for gallery access)  
  - `http` (for API calls to the backend)  

### **Backend**
- **Framework**: Flask/Django/Python (or your preferred backend framework)  
- **Image Processing**: MediaPipe, OpenCV  
- **Database**: (Optional) PostgreSQL for logging or tailor integration.  

---

## **Project Setup**

### **1. Prerequisites**
- Flutter SDK: [Install Flutter](https://flutter.dev/docs/get-started/install)  
- Backend server setup with the required ML models.  
- Device with a working camera.  

### **2. Installation**
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/body-measurement-app.git
   cd body-measurement-app
   ```
2. Install dependencies:  
   ```bash
   flutter pub get
   ```
3. Run the app:  
   ```bash
   flutter run
   ```

### **3. Backend Setup**
- Ensure your backend is up and running to process the images.  
- Use the provided API endpoint to connect the app with the backend.  

---

## **How It Works**

### **User Flow**
1. **Capture Photos**: Users are guided to take photos in specific poses.  
2. **Upload to Server**: Captured images are securely uploaded to the backend.  
3. **Image Processing**: The backend processes images using ML models to detect keypoints and calculate measurements.  
4. **Retrieve Results**: The app fetches the measurements and displays them in a user-friendly format.  

### **Key Measurements**
- **Shoulder Width**: Distance between shoulder keypoints.  
- **Chest/Bust Circumference**: Estimated from chest and back keypoints.  
- **Waist Circumference**: Calculated from the narrowest torso keypoints.  
- **Hip Circumference**: Measured from the widest hip keypoints.  
- **Inseam Length**: Length between the groin, knee, and ankle keypoints.  

---

## **Folder Structure**

```plaintext
lib/
│
├── main.dart                # Entry point of the Flutter app
├── screens/                 # UI Screens (Home, Results, etc.)
│   ├── home_screen.dart
│   ├── result_screen.dart
│
├── services/                # API services
│   ├── api_service.dart     # Handles backend API calls
│
├── widgets/                 # Reusable UI components
│   ├── custom_button.dart
│   ├── image_preview.dart
│
└── utils/                   # Utility functions
    ├── constants.dart       # API URLs and constants
    ├── helpers.dart         # Helper functions for scaling and validation
```

---

## **To-Do**
- [ ] Add AR-based guidelines for pose correction.  
- [ ] Enhance measurement accuracy with depth data from LiDAR (for supported devices).  
- [ ] Integrate tailor APIs for seamless measurement sharing.  
- [ ] Add multi-language support for global users.  

---

## **Contributing**
We welcome contributions to improve this app!  
1. Fork the repository.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:  
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.  

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**
For any questions or collaboration requests, feel free to reach out:  
- **Email**: amit.rawal@joshsoftware.com  
