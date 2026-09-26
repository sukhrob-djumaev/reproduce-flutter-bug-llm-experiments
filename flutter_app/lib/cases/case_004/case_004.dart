import 'package:flutter/material.dart';

class Case004App extends StatelessWidget {
  const Case004App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: Case004Page());
  }
}

class Case004Page extends StatelessWidget {
  const Case004Page({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tasks')),
      body: ListView(
        children: const [
          ListTile(title: Text('Weekly report')),
          ListTile(title: Text('Weekly report')),
        ],
      ),
    );
  }
}
