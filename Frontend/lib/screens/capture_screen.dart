import 'package:flutter/material.dart';

class CaptureScreen extends StatelessWidget {
  const CaptureScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Capture Your Photos'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
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
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
                children: [
                  buildCaptureFrame('assets/pose_front.png', context),
                  buildCaptureFrame('assets/pose_side.png', context),
                  buildCaptureFrame('assets/pose_back.png', context),
                  buildCaptureFrame('assets/pose_background.png', context),
                ],
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
                  onPressed: () {},
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

  Widget buildCaptureFrame(String imagePath, BuildContext context) {
    return SizedBox(
      height: 200,
      child: Stack(
        alignment: Alignment.bottomCenter,
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.asset(
              imagePath,
              fit: BoxFit.contain,
              height: double.infinity,
              width: double.infinity,
            ),
          ),
          Positioned(
            bottom: 0,
            right: 0,
            child: IconButton(
              onPressed: () {
                // Logic for capturing image
              },
              icon: Icon(Icons.camera_alt, color: Colors.blue),
            ),
          ),
        ],
      ),
    );
  }
}
