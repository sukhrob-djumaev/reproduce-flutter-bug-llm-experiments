import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Builder(
            builder: (context) => ElevatedButton(
              onPressed: () => showDialog(
                context: context,
                builder: (_) => AlertDialog(
                  title: const Text('Test dialog'),
                  content: const Text('Dialog content'),
                  actions: [
                    TextButton(
                      onPressed: () {},
                      child: const Text('Delete'),
                    ),
                    const Spacer(), // ← causes silent debug / release inconsistency
                    OutlinedButton(
                      onPressed: () {},
                      child: const Text('Cancel'),
                    ),
                    FilledButton(
                      onPressed: () {},
                      child: const Text('Save'),
                    ),
                  ],
                ),
              ),
              child: const Text('Show dialog'),
            ),
          ),
        ),
      ),
    );
  }
}
