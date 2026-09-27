import 'package:flutter/material.dart';
import 'package:flutter_driver/driver_extension.dart';
import 'package:flutter_bug_reproduction/cases/case_001/case_001.dart';

void main() {
  enableFlutterDriverExtension();
  runApp(const Case001App());
}
