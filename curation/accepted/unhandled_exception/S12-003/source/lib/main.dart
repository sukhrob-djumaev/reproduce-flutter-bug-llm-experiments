import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        body: Center(
          child: UnconstrainedBox(
            child: Overlay(
              initialEntries: [
                OverlayEntry(
                  canSizeOverlay: true,
                  builder: (_) => const _Content(),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}

class _Content extends StatelessWidget {
  const _Content();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 300,
      height: 300,
      color: Colors.lightBlue.shade100,
      alignment: Alignment.bottomCenter,
      child: DropdownMenu<int>(
        label: const Text('Tap to reproduce'),
        dropdownMenuEntries: [
          for (var i = 1; i <= 3; i++)
            DropdownMenuEntry(value: i, label: 'Item $i'),
        ],
      ),
    );
  }
}
