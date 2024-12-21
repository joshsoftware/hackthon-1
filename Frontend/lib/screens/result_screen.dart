import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:stitch_perfect/models/measurement_model.dart';
import 'package:stitch_perfect/viewmodels/measurement_view_model.dart';

class MeasurementResultsPage extends StatefulWidget {
  final objId;

  const MeasurementResultsPage(this.objId, {super.key});

  @override
  _MeasurementResultsPageState createState() => _MeasurementResultsPageState();
}

class _MeasurementResultsPageState extends State<MeasurementResultsPage> {
  late String objId;

  @override
  void initState() {
    super.initState();
    objId = widget.objId;
    // Fetch measurements once when the widget is initialized
    final viewModel = Provider.of<MeasurementViewModel>(context, listen: false);
    viewModel.fetchMeasurements(objId);
  }

  @override
  Widget build(BuildContext context) {
    final viewModel = Provider.of<MeasurementViewModel>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Your Measurements',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.teal.shade300,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: "Refresh Measurements",
            onPressed: () {
              viewModel.fetchMeasurements(objId);
            },
          ),
        ],
      ),
      body: viewModel.isLoading
          ? const Center(child: CircularProgressIndicator())
          : viewModel.errorMessage != null
              ? Center(
                  child: Text(
                    viewModel.errorMessage!,
                    style: const TextStyle(color: Colors.red),
                  ),
                )
              : ResultScreenBody(
                  measurements: viewModel.measurements,
                ),
    );
  }
}

class ResultScreenBody extends StatelessWidget {
  ResultScreenBody({
    super.key,
    required this.measurements,
  });

  final MeasurementModel measurements;
  List<String> topMeasurements = [];
  List<String> bottomMeasurements = [];

  @override
  Widget build(BuildContext context) {
    final double deviceHeight = MediaQuery.of(context).size.height;
    final double deviceWidth = MediaQuery.of(context).size.width;
    if (measurements != null) {
      topMeasurements = [
        "Shoulder Width : " + measurements.shoulder.toString(),
        "Sleeve Length : " + measurements.armlength.toString(),
        "Shirt Length : " + measurements.shirt.toString(),
      ];
      bottomMeasurements = [
        "Chest Circumference :" + measurements.chest.toString(),
        "Waist Circumference : " + measurements.waist.toString(),
        "Outseam Length : " + measurements.leg.toString()
      ];
      ;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 16),
        const Center(
          child: Text(
            'All measurements are in inches',
            style: TextStyle(fontSize: 14, color: Colors.grey),
          ),
        ),
        const SizedBox(height: 16),
        // Row containing the custom image on the left and the measurements
        Expanded(
          child: Row(
            children: [
              // Custom Image on the left corner without padding
              ClipRect(
                child: Align(
                  alignment: Alignment.centerRight,
                  widthFactor: 0.5, // Show only half of the image
                  child: Container(
                    width: deviceWidth * 0.45,
                    height: deviceHeight * 0.6,
                    decoration: BoxDecoration(
                      borderRadius: const BorderRadius.only(
                        topRight: Radius.circular(12),
                        bottomRight: Radius.circular(12),
                      ),
                      image: const DecorationImage(
                        image: AssetImage('assets/images/pose_front.png'),
                        fit: BoxFit.fitHeight,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(
                  width: 16), // Spacing between image and measurements
              // Measurements
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Top Measurements (Above the center of the image view)
                    Column(
                      children: topMeasurements
                          .map((entry) => Padding(
                                padding: const EdgeInsets.symmetric(
                                    vertical: 16, horizontal: 16),
                                child: Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      entry.toString(),
                                      style: const TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                    // Text(
                                    //   entry.toString(),
                                    //   style: const TextStyle(
                                    //     fontSize: 16,
                                    //     fontWeight: FontWeight.bold,
                                    //   ),
                                    // ),
                                  ],
                                ),
                              ))
                          .toList(),
                    ),
                    // Bottom Measurements (Below the center of the image view)

                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Container(
                        width: double
                            .infinity, // Makes the line take the full width
                        height: 1, // Height of the separator line
                        color: Colors.grey, // Grey color for the separator
                      ),
                    ),
                    Column(
                      children: bottomMeasurements
                          .map((entry) => Padding(
                                padding: const EdgeInsets.symmetric(
                                    vertical: 16, horizontal: 16),
                                child: Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      entry.toString(),
                                      style: const TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                    // Text(
                                    //   entry.toString(),
                                    //   style: const TextStyle(
                                    //     fontSize: 16,
                                    //     fontWeight: FontWeight.bold,
                                    //   ),
                                    // ),
                                  ],
                                ),
                              ))
                          .toList(),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        // Buttons
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ShareButton(model: measurements),
                SizedBox(
                  height: 16,
                ),
                CaptureImageButton(),
              ],
            ),
          ),
        ),
        const SizedBox(height: 46),
      ],
    );
  }
}

class CaptureImageButton extends StatelessWidget {
  const CaptureImageButton({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 250,
      child: ElevatedButton.icon(
        onPressed: () {
          // Add logic for "Capture Again"
          Navigator.of(context).popUntil((route) => route.isFirst);
        },
        icon: const Icon(
          Icons.camera_alt,
          color: Colors.teal,
        ),
        label: const Text(
          'Capture Again',
          style: TextStyle(
              fontSize: 16, color: Colors.teal, fontWeight: FontWeight.w600),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.white,
          foregroundColor: Colors.teal,
          padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
    );
  }
}

class ShareButton extends StatelessWidget {
  MeasurementModel model;

  ShareButton({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 250,
      child: ElevatedButton.icon(
        onPressed: () {
          // Add logic for "Share"
          // Example measurements
          final measurements = {
            "Shoulder Width": model.shoulder,
            "Chest Circumference": model.chest,
            "Sleeve Length": model.armlength,
            "Outseam Length": model.leg,
            "Waist Circumference": model.waist,
            "Shirt Length": model.shirt,
          };

          // Format the measurements as a string
          String measurementText = "Here are the body measurements:\n\n";
          measurements.forEach((key, value) {
            measurementText += "$key: $value inches\n";
          });

          // Share via WhatsApp (or any platform)
          Share.share(
            measurementText,
            subject: 'Body Measurements',
          );
        },
        icon: const Icon(
          Icons.share,
          color: Colors.white,
        ),
        label: const Text(
          'Share',
          style: TextStyle(
              fontSize: 16, color: Colors.white, fontWeight: FontWeight.w600),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.teal,
          foregroundColor: Colors.white,
          padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
    );
  }
}
