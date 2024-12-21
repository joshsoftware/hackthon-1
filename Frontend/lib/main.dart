import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stitch_perfect/screens/capture_screen.dart';
import 'package:stitch_perfect/screens/home_screen.dart';
import 'package:stitch_perfect/screens/result_screen.dart';
import 'package:stitch_perfect/viewmodels/capture_image_view_model.dart';
import 'package:stitch_perfect/viewmodels/measurement_view_model.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ImageViewModel()),
        ChangeNotifierProvider(
          create: (context) => MeasurementViewModel(),
        ),
      ],
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'StitchPerfect',
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      routes: {
        '/': (context) => HomeScreen(),
        '/captureScreen': (context) => CaptureScreen(),
        '/resultScreen': (context) => MeasurementResultsPage(""),
      },
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
    );
  }
}
