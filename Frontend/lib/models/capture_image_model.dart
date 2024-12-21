import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:http/http.dart';

class ImageModel {
  final String _uploadUrl =
      "https://probable-uniquely-scorpion.ngrok-free.app/upload"; // Replace with your server URL

  String responseObjId = "";

  Future<bool> uploadAllImages(List<File?> images, String height) async {
    try {
      final uri = Uri.parse(_uploadUrl);
      final request = http.MultipartRequest("POST", uri);
      for (int i = 0; i < images.length; i++) {
        request.files.add(
            await http.MultipartFile.fromPath(getFileKey(i), images[i]!.path));
      }
      request.fields['height'] = height;

      final response = await request.send();

      // Check if the upload was successful
      if (response.statusCode == 201) {
        var responseData = await response.stream.bytesToString();
        Map<String, dynamic> parsedResponse = json.decode(responseData);

        // Access specific fields
        responseObjId = parsedResponse["id"];
      } else {
        print("Something went wrong.");
        return false;
      }
      return true;
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
      return "front-hand-open";
    case 3:
      return "front-hand-closed";
    case 4:
      return "side";
    default:
      return "side";
  }
}
