import 'package:flutter/material.dart';
import 'package:stitch_perfect/screens/capture_screen.dart';
import 'package:stitch_perfect/widgets/HeightInputDialogWidget.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.symmetric(vertical: 50.0, horizontal: 30),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      height: 250,
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(16),
                        child: Image.asset(
                          'assets/images/home_logo.png',
                          fit: BoxFit.fill,
                        ),
                      ),
                    ),
                    SizedBox(height: 16),
                    Text(
                      'One stop solution to measure body\ndimensions for custom tailoring',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.grey[900],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                // Show the height input dialog and wait for the result
                String? height = await showDialog<String>(
                  context: context,
                  builder: (BuildContext context) {
                    return HeightInputDialog(
                      onHeightSubmitted: (height) {
                        // Handle the height submission and pass it back to the caller
                        Navigator.of(context).pop(height);
                      },
                    );
                  },
                );

                if (height != null && height.isNotEmpty) {
                  FocusScope.of(context).unfocus();
                  // Navigate to the next screen with the entered height
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => CaptureScreen(height: height),
                    ),
                  );
                }
                //Navigator.pushNamed(context, '/captureScreen');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.teal,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: Text(
                'Start by Capturing Images',
                style: TextStyle(
                    fontSize: 16,
                    color: Colors.white,
                    fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
