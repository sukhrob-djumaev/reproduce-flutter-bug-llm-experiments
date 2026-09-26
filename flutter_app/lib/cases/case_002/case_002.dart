import 'package:flutter/material.dart';

class Case002App extends StatelessWidget {
  const Case002App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: Case002Page());
  }
}

class Case002Page extends StatefulWidget {
  const Case002Page({super.key});

  @override
  State<Case002Page> createState() => _Case002PageState();
}

class _Case002PageState extends State<Case002Page> {
  String _name = '';

  void _submit() {
    if (_name.isEmpty) {
      throw StateError('A name is required.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              key: const ValueKey<String>('name-field'),
              decoration: const InputDecoration(labelText: 'Name'),
              onChanged: (value) => _name = value,
            ),
            const SizedBox(height: 16),
            FilledButton(
              key: const ValueKey<String>('submit-button'),
              onPressed: _submit,
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}
