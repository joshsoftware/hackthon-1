import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';

// class ImageModel {
//   final String _uploadUrl =
//       "https://your-server.com/upload"; // Replace with your server URL

//   // Upload image with progress callback
//   Future<bool> uploadImageWithProgress(
//     File imageFile,
//     Function(double) onProgress,
//   ) async {
//     try {
//       final uri = Uri.parse(_uploadUrl);
//       final request = http.MultipartRequest("POST", uri);
//       request.files
//           .add(await http.MultipartFile.fromPath('file', imageFile.path));

//       final streamedResponse = await request.send();

//       final responseStream = streamedResponse.stream;
//       final contentLength = streamedResponse.contentLength ?? 0;

//       int bytesUploaded = 0;
//       final List<int> bytes = [];

//       await for (var chunk in responseStream) {
//         bytes.addAll(chunk);
//         bytesUploaded += chunk.length;

//         // Update progress
//         final progress = bytesUploaded / contentLength;
//         onProgress(progress);
//       }

//       final response = Response.bytes(
//         bytes,
//         streamedResponse.statusCode,
//         request: streamedResponse.request,
//         headers: streamedResponse.headers,
//       );

//       // Check if the upload was successful
//       return response.statusCode == 200;
//     } catch (e) {
//       print("Error uploading image: $e");
//       return false;
//     }
//   }
// }

class ImageModel {
  // Simulated upload function with progress updates
  Future<bool> uploadImageWithProgress(
    File imageFile,
    Function(double) onProgress,
  ) async {
    try {
      const int totalSteps = 100; // Simulate 100 steps for the upload
      const Duration stepDuration = Duration(milliseconds: 50); // 50ms per step

      for (int step = 0; step <= totalSteps; step++) {
        await Future.delayed(stepDuration);

        // Calculate and report progress
        final progress = step / totalSteps;
        onProgress(progress);
      }

      // Simulate successful upload
      return true;
    } catch (e) {
      if (kDebugMode) {
        print("Error during simulated upload: $e");
      }
      return false;
    }
  }
}
