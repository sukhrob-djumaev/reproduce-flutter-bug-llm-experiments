import 'package:flutter/material.dart';
import 'package:flutter_driver/driver_extension.dart';
import 'package:flutter_bug_reproduction/cases/case_003/case_003.dart';

void main() {
  enableFlutterDriverExtension();
  runApp(const Case003App());
}
