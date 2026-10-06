import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("FlChart Test")),
        body: LineChart(
          LineChartData(
            lineBarsData: [
              LineChartBarData(spots: [FlSpot(0, 0), FlSpot(1, 1)]),
              LineChartBarData(spots: [FlSpot.nullSpot]),
            ],
          ),
        ),
      ),
    );
  }
}
