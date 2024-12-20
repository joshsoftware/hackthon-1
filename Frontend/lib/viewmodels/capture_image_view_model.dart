// viewmodels/image_view_model.dart
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:stitch_perfect/models/capture_image_model.dart';
import 'package:flutter/material.dart';

class CaptureImageViewModel extends ChangeNotifier {
  final CaptureImageModel _imageModel = CaptureImageModel();
  File? _selectedImage;
  bool _isUploading = false;

  File? get selectedImage => _selectedImage;
  bool get isUploading => _isUploading;

  Future<void> pickImage(ImageSource source) async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: source);

    if (pickedFile != null) {
      _selectedImage = File(pickedFile.path);
      notifyListeners();
    }
  }

  Future<bool> uploadImage() async {
    if (_selectedImage == null) return false;

    _isUploading = true;
    notifyListeners();

    bool success = await _imageModel.uploadImage(_selectedImage!);

    _isUploading = false;
    notifyListeners();

    return success;
  }
}
