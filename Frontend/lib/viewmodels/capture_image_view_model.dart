// viewmodels/image_view_model.dart
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:stitch_perfect/models/capture_image_model.dart';

class ImageViewModel extends ChangeNotifier {
  final ImageModel _imageModel = ImageModel();

  // Store file paths for four images
  final List<File?> _selectedImages = [null, null, null, null];

  // Upload progress for each image
  final List<double> _uploadProgress = [0.0, 0.0, 0.0, 0.0];

  // Sample images for placeholders
  final List<String> _sampleImages = [
    'assets/images/pose_hands_up.png',
    'assets/images/pose_hands_open.png',
    'assets/images/pose_hands_close.png',
    'assets/images/pose_side.png',
  ];

  List<File?> get selectedImages => _selectedImages;

  List<double> get uploadProgress => _uploadProgress;

  List<String> get sampleImages => _sampleImages;

  // Pick an image for a specific index
  Future<void> pickImage(int index, ImageSource source) async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: source);

    if (pickedFile != null) {
      _selectedImages[index] = File(pickedFile.path);
      notifyListeners();
    }
  }

  // Remove an image and reset to the sample
  void removeImage(int index) {
    _selectedImages[index] = null;
    _uploadProgress[index] = 0.0;
    notifyListeners();
  }

  // Remove an image and reset to the sample
  bool hasImage(int index) {
    return _selectedImages[index] != null;
  }

  // Upload an image for a specific index
  Future<void> uploadImage(int index) async {
    if (_selectedImages[index] == null) return;

    _uploadProgress[index] = 0.1;
    notifyListeners();

    bool success = await _imageModel.uploadImageWithProgress(
      _selectedImages[index]!,
      getFileKey(index),
      (progress) {
        _uploadProgress[index] = progress;
        notifyListeners();
      },
    );

    if (!success) {
      _uploadProgress[index] = 0.0; // Reset on failure
    }
    notifyListeners();
  }

  // Upload all images
  Future<bool> uploadAllImages() async {
    // for (int i = 0; i < _selectedImages.length; i++) {
    //   await uploadImage(i);
    // }
    return await _imageModel.uploadAllImages(_selectedImages);
  }
}
