import 'package:fluent_ui/fluent_ui.dart';

void main() => runApp(const TestApp());

class TestApp extends StatefulWidget {
  const TestApp({super.key});

  @override
  State<TestApp> createState() => _TestAppState();
}

class _TestAppState extends State<TestApp> {
  int _currentIndex = 0;
  int _unrelated = 0;

  @override
  Widget build(BuildContext context) {
    return FluentApp(
      home: Column(
        children: [
          // Tapping this button only rebuilds this widget; it does not
          // touch currentIndex, the tabs, or anything inside them.
          Button(
            onPressed: () => setState(() => _unrelated++),
            child: Text('rebuild parent: $_unrelated'),
          ),
          Expanded(
            child: TabView(
              currentIndex: _currentIndex,
              onChanged: (value) => setState(() => _currentIndex = value),
              tabs: [
                Tab(text: const Text('tab 1'), body: const CounterPage()),
                Tab(text: const Text('tab 2'), body: const CounterPage()),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Button(
        onPressed: () => setState(() => _counter++),
        child: Text('counter: $_counter'),
      ),
    );
  }
}
