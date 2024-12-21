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
    final viewModel = Provider.of<ImageViewModel>(context);
    return Scaffold(
      appBar: AppBar(title: Text('Capture Your Photos')),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Prerequisites',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 10),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8.0),
              child: Text(
                '1. Please stand where you have White/light background.\n'
                '2. Please wear Tight clothes or you can capture with Undergarments only - Capture images will not be saved on server.\n'
                '3. Please wear Dark Coloured clothes.\n'
                '4. Please capture all photos from same distance & angle.\n'
                '5. Please capture photos in poses shown in each frame below.',
                style: TextStyle(fontSize: 12, color: Colors.grey[800]),
              ),
            ),
            SizedBox(height: 20),
            Expanded(
              child: GridView.builder(
                padding: EdgeInsets.all(10),
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 5,
                  mainAxisSpacing: 5,
                ),
                itemCount: 4,
                itemBuilder: (context, index) {
                  final selectedImage = viewModel.selectedImages[index];
                  final sampleImage = viewModel.sampleImages[index];
                  final uploadProgress = viewModel.uploadProgress[index];

                  return Stack(
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(10),
                            image: DecorationImage(
                              image: selectedImage != null
                                  ? FileImage(selectedImage)
                                  : AssetImage(sampleImage) as ImageProvider,
                              fit: BoxFit.contain,
                            ),
                          ),
                        ),
                      ),
                      if (uploadProgress > 0.0 && uploadProgress < 1.0)
                        Positioned.fill(
                          child: Center(
                            child: CircularProgressIndicator(
                              value: uploadProgress,
                            ),
                          ),
                        ),
                      if(viewModel.hasImage(index)) Positioned(
                        top: 0,
                        right: 0,
                        child: Container(
                          decoration: BoxDecoration(
                            color: Colors.red, // Background color
                            shape: BoxShape.circle, // Circular shape
                          ),
                          child: IconButton(
                            icon: Icon(Icons.close, color: Colors.white),
                            onPressed: () {
                              viewModel.removeImage(index);
                            },
                          ),
                        ),
                      ),
                      if(!viewModel.hasImage(index)) Positioned(
                        bottom: 0,
                        right: 0,
                        child: SizedBox(
                          width: 40,
                          height: 40,
                          child: IconButton(
                            iconSize: 40,
                            icon:
                                Icon(Icons.camera_alt, color: Colors.lightBlue),
                            onPressed: () {
                              DialogUtils.showImageSourceDialog(
                                context,
                                index,
                              );
                            },
                          ),
                        ),
                      ),
                    ],
                  );
                },
              ),
            ),
            SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: Text(
                    'Cancel',
                    style: TextStyle(fontSize: 16, color: Colors.red),
                  ),
                ),
                ElevatedButton(
                  onPressed: () async {
                    await viewModel.uploadAllImages();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('All images uploaded successfully!'),
                      ),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                  ),
                  child: Text(
                    'Upload Images',
                    style: TextStyle(fontSize: 16, color: Colors.white),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
