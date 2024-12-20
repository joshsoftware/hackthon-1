import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class CaptureImageModel {
  Future<bool> uploadImage(File image) async {
    try {
      var request = http.MultipartRequest(
          'POST', Uri.parse('https://example.com/upload'));
      request.files.add(await http.MultipartFile.fromPath('file', image.path));
      var response = await request.send();

      if (response.statusCode == 200) {
        return true;
      } else {
        return false;
      }
    } catch (e) {
      if (kDebugMode) {
        print('Upload failed: $e');
      }
      return false;
    }
  }
}
