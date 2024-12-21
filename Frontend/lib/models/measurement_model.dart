class MeasurementModel {
  final double armlength;
  final double chest;
  final double height;
  final String id;
  final double shoulder;
  final double waist;
  final double leg;
  final double shirt;

  // Constructor
  MeasurementModel({
    required this.armlength,
    required this.chest,
    required this.height,
    required this.id,
    required this.shoulder,
    required this.waist,
    required this.leg,
    required this.shirt,
  });

  // Factory method to create an instance from JSON
  factory MeasurementModel.fromJson(Map<String, dynamic> json) {
    return MeasurementModel(
      armlength: json['armlength'] != null ? json['armlength'].toDouble() : 0,
      chest: json['chest'] != null ? json['chest'].toDouble() : 0,
      height: json['height'] != null ? json['height'].toDouble() : 0,
      id: json['id'],
      shoulder: json['shoulder'] != null ? json['shoulder'].toDouble() : 0,
      waist: json['waist'] != null ? json['waist'].toDouble() : 0,
      leg: json['leg'] != null ? json['leg'].toDouble() : 0,
      shirt: json['shirt'] != null ? json['shirt'].toDouble() : 0,
    );
  }

  // Method to convert an instance to JSON
  Map<String, dynamic> toJson() {
    return {
      'armlength': armlength,
      'chest': chest,
      'height': height,
      'id': id,
      'shoulder': shoulder,
      'waist': waist,
      'leg': leg,
      'shirt': shirt,
    };
  }
}
