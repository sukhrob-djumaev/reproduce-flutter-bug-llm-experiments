import 'package:flutter/material.dart';

class Case001App extends StatelessWidget {
  const Case001App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: Case001Page());
  }
}

class Case001Page extends StatefulWidget {
  const Case001Page({super.key});

  @override
  State<Case001Page> createState() => _Case001PageState();
}

class _Case001PageState extends State<Case001Page> {
  final int _count = 0;

  void _increment() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Count: $_count',
              key: const ValueKey<String>('counter-value'),
            ),
            const SizedBox(height: 16),
            FilledButton(
              key: const ValueKey<String>('increment-button'),
              onPressed: _increment,
              child: const Text('+'),
            ),
          ],
        ),
      ),
    );
  }
}
