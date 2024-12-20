import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stitch_perfect/utils/dialog_utils.dart';
import 'package:stitch_perfect/viewmodels/capture_image_view_model.dart';

class CaptureScreen extends StatefulWidget {
  const CaptureScreen({super.key});
  @override
  State<CaptureScreen> createState() => _CaptureScreenState();
}

class _CaptureScreenState extends State<CaptureScreen> {
  @override
  Widget build(BuildContext context) {
    final viewModel = Provider.of<CaptureImageViewModel>(context);

    return Scaffold(
      appBar: AppBar(title: Text('Capture & Upload')),
      body: Center(
        child: viewModel.isUploading
            ? CircularProgressIndicator()
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  viewModel.selectedImage != null
                      ? Image.file(
                          viewModel.selectedImage!,
                          width: 200,
                          height: 200,
                          fit: BoxFit.cover,
                        )
                      : Icon(Icons.image, size: 100, color: Colors.grey),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      DialogUtils.showImageSourceDialog(context);
                    },
                    child: Text('Capture Image'),
                  ),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () async {
                      bool success = await viewModel.uploadImage();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(success
                              ? 'Upload successful!'
                              : 'Upload failed.'),
                        ),
                      );
                    },
                    child: Text('Upload Image'),
                  ),
                ],
              ),
      ),
    );
  }
}
