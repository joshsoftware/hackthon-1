class MeasurementModel {
  final String key;
  final double value;

  MeasurementModel({required this.key, required this.value});

  factory MeasurementModel.fromJson(Map<String, dynamic> json) {
    return MeasurementModel(
      key: json['key'],
      value: json['value'].toDouble(),
    );
  }
}
