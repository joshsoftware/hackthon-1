// height_input_dialog.dart
import 'package:flutter/material.dart';

class HeightInputDialog extends StatefulWidget {
  final Function(String)
      onHeightSubmitted; // Callback function to return the height

  HeightInputDialog({required this.onHeightSubmitted});

  @override
  _HeightInputDialogState createState() => _HeightInputDialogState();
}

class _HeightInputDialogState extends State<HeightInputDialog> {
  final TextEditingController _heightController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Enter Your Height'),
      content: TextField(
        controller: _heightController,
        keyboardType: TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(hintText: 'Height in inches'),
      ),
      actions: [
        TextButton(
          onPressed: () {
            String height = _heightController.text;
            if (height.isNotEmpty) {
              widget.onHeightSubmitted(height);
              Navigator.of(context).pop(); // Close the dialog
            } else {
              // You can show an error message if needed
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Please enter a valid height')),
              );
            }
          },
          child: Text('Next'),
        ),
      ],
    );
  }
}
