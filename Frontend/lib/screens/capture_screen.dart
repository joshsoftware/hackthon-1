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
      appBar: AppBar(title: Text('Upload Images')),
      body: Column(
        children: [
          Expanded(
            child: GridView.builder(
              padding: EdgeInsets.all(10),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
              ),
              itemCount: 4,
              itemBuilder: (context, index) {
                final selectedImage = viewModel.selectedImages[index];
                final sampleImage = viewModel.sampleImages[index];
                final uploadProgress = viewModel.uploadProgress[index];

                return Stack(
                  children: [
                    GestureDetector(
                      onTap: () {
                        DialogUtils.showImageSourceDialog(
                          context,
                          index,
                        );
                      },
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(10),
                          image: DecorationImage(
                            image: selectedImage != null
                                ? FileImage(selectedImage)
                                : AssetImage(sampleImage) as ImageProvider,
                            fit: BoxFit.cover,
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
                    Positioned(
                      top: 5,
                      right: 5,
                      child: IconButton(
                        icon: Icon(Icons.close, color: Colors.red),
                        onPressed: () {
                          viewModel.removeImage(index);
                        },
                      ),
                    ),
                  ],
                );
              },
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
            child: Text('Upload All Images'),
          ),
        ],
      ),
    );
  }
}
