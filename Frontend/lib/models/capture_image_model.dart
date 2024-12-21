import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:http/http.dart';

class ImageModel {
  final String _uploadUrl =
      "https://bluebird-pleased-curiously.ngrok-free.app/upload"; // Replace with your server URL

  // Upload image with progress callback
  Future<bool> uploadImageWithProgress(
    File imageFile,
    String key,
    Function(double) onProgress,
  ) async {
    try {
      final uri = Uri.parse(_uploadUrl);
      final request = http.MultipartRequest("POST", uri);
      request.files.add(await http.MultipartFile.fromPath(key, imageFile.path));
      request.fields['height'] = "5.7";

      final streamedResponse = await request.send();

      final responseStream = streamedResponse.stream;
      final contentLength = streamedResponse.contentLength ?? 0;

      int bytesUploaded = 0;
      final List<int> bytes = [];

      await for (var chunk in responseStream) {
        bytes.addAll(chunk);
        bytesUploaded += chunk.length;

        // Update progress
        final progress = bytesUploaded / contentLength;
        onProgress(progress);
      }

      final response = Response.bytes(
        bytes,
        streamedResponse.statusCode,
        request: streamedResponse.request,
        headers: streamedResponse.headers,
      );

      // Check if the upload was successful
      return response.statusCode == 200;
    } catch (e) {
      print("Error uploading image: $e");
      return false;
    }
  }

  Future<bool> uploadAllImages(
    List<File?> images,
  ) async {
    try {
      final uri = Uri.parse(_uploadUrl);
      final request = http.MultipartRequest("POST", uri);
      for (int i = 0; i < images.length; i++) {
        request.files.add(
            await http.MultipartFile.fromPath(getFileKey(i), images[i]!.path));
      }
      request.fields['height'] = "5.7";

      final streamedResponse = await request.send();
      final List<int> bytes = [];

      final response = Response.bytes(
        bytes,
        streamedResponse.statusCode,
        request: streamedResponse.request,
        headers: streamedResponse.headers,
      );

      // Check if the upload was successful
      return response.statusCode == 201;
    } catch (e) {
      print("Error uploading image: $e");
      return false;
    }
  }
}

String getFileKey(int index) {
  switch (index) {
    case 1:
      return "front-hand-raised";
    case 2:
      return "front-hand-close";
    case 3:
      return "side";
    case 4:
      return "back";
    default:
      return "back";
  }
}

// class ImageModel {
//   // Simulated upload function with progress updates
//   Future<bool> uploadImageWithProgress(
//     File imageFile,
//     Function(double) onProgress,
//   ) async {
//     try {
//       const int totalSteps = 100; // Simulate 100 steps for the upload
//       const Duration stepDuration = Duration(milliseconds: 50); // 50ms per step
//
//       for (int step = 0; step <= totalSteps; step++) {
//         await Future.delayed(stepDuration);
//
//         // Calculate and report progress
//         final progress = step / totalSteps;
//         onProgress(progress);
//       }
//
//       // Simulate successful upload
//       return true;
//     } catch (e) {
//       if (kDebugMode) {
//         print("Error during simulated upload: $e");
//       }
//       return false;
//     }
//   }
// }
