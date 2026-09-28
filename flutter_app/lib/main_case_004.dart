import 'package:flutter/material.dart';
import 'package:flutter_driver/driver_extension.dart';
import 'package:flutter_bug_reproduction/cases/case_004/case_004.dart';

void main() {
  enableFlutterDriverExtension();
  runApp(const Case004App());
}
