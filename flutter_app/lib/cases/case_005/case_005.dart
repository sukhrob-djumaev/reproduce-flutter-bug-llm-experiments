import 'package:flutter/material.dart';

class Case005App extends StatelessWidget {
  const Case005App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: Case005Page());
  }
}

class Case005Page extends StatefulWidget {
  const Case005Page({super.key});

  @override
  State<Case005Page> createState() => _Case005PageState();
}

class _Case005PageState extends State<Case005Page> {
  final String _status = 'Ready';

  Future<void> _refresh() async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    debugPrint('Refresh request failed');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Updates')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Status: $_status',
              key: const ValueKey<String>('status-value'),
            ),
            const SizedBox(height: 16),
            FilledButton(
              key: const ValueKey<String>('refresh-button'),
              onPressed: _refresh,
              child: const Text('Refresh'),
            ),
          ],
        ),
      ),
    );
  }
}
