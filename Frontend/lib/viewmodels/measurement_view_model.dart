import 'package:flutter/material.dart';
import 'package:stitch_perfect/models/measurement_model.dart';
import 'package:stitch_perfect/services/measurement_service.dart';

class MeasurementViewModel extends ChangeNotifier {
  final MeasurementService _service = MeasurementService();

  List<MeasurementModel> _measurements = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<MeasurementModel> get measurements => _measurements;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  Future<void> fetchMeasurements() async {
    _isLoading = true;
    _errorMessage = null;
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      notifyListeners();
      try {
        _measurements = await _service.fetchMeasurements();
      } catch (error) {
        _errorMessage = error.toString();
      } finally {
        _isLoading = false;
        notifyListeners();
      }
    });
  }
}
