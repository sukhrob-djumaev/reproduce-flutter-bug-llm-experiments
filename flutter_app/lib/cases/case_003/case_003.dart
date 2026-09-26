import 'package:flutter/material.dart';

class Case003App extends StatelessWidget {
  const Case003App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: Case003StartPage());
  }
}

class Case003StartPage extends StatelessWidget {
  const Case003StartPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Welcome')),
      body: Center(
        child: FilledButton(
          key: const ValueKey<String>('continue-button'),
          onPressed: () {
            Navigator.of(context).push<void>(
              MaterialPageRoute<void>(
                builder: (context) => const Case003DetailsPage(),
              ),
            );
          },
          child: const Text('Continue'),
        ),
      ),
    );
  }
}

class Case003DetailsPage extends StatelessWidget {
  const Case003DetailsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Preferences')),
      body: Center(
        child: FilledButton(
          key: const ValueKey<String>('finish-button'),
          onPressed: () {
            Navigator.of(context).push<void>(
              MaterialPageRoute<void>(
                builder: (context) => const Case003ReviewPage(),
              ),
            );
          },
          child: const Text('Finish'),
        ),
      ),
    );
  }
}

class Case003ReviewPage extends StatelessWidget {
  const Case003ReviewPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Review')),
      body: const Center(child: Text('Review your preferences')),
    );
  }
}
