import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(const ReproApp());

const int kRowCount = 4;
const int kCardsPerRow = 8;

const double kCardWidth = 360;
const double kCardHeight = 150;
const double kCardGap = 10;

final ValueNotifier<String> focusedLabel = ValueNotifier<String>('(none)');

class ReproApp extends StatelessWidget {
  const ReproApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(12),
              child: ValueListenableBuilder<String>(
                valueListenable: focusedLabel,
                builder: (context, value, _) => Text(
                  'Focused: $value   —   press Down then Up. Expect back on r0c0, observe r0c1.',
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ),
            Expanded(
              child: CustomScrollView(
                slivers: [
                  SliverList.builder(
                    itemCount: kRowCount,
                    itemBuilder: (context, row) => FocusRow(row: row),
                  ),
                  const SliverToBoxAdapter(child: SizedBox(height: 400)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class FocusRow extends StatefulWidget {
  const FocusRow({required this.row, super.key});

  final int row;

  @override
  State<FocusRow> createState() => _FocusRowState();
}

class _FocusRowState extends State<FocusRow> {
  late final FocusScopeNode _scope = FocusScopeNode(debugLabel: 'rowScope${widget.row}');
  int? _selectedCard;

  @override
  void dispose() {
    _scope.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FocusScope(
      node: _scope,
      onKeyEvent: (node, event) {
        if (event is! KeyDownEvent) {
          return KeyEventResult.ignored;
        }
        if (event.logicalKey == LogicalKeyboardKey.arrowDown) {
          _scope.enclosingScope?.focusInDirection(TraversalDirection.down);
          return KeyEventResult.handled;
        }
        if (event.logicalKey == LogicalKeyboardKey.arrowUp) {
          _scope.enclosingScope?.focusInDirection(TraversalDirection.up);
          return KeyEventResult.handled;
        }
        if (_selectedCard == 0 && event.logicalKey == LogicalKeyboardKey.arrowLeft) {
          _scope.enclosingScope?.focusInDirection(TraversalDirection.left);
          return KeyEventResult.handled;
        }
        return KeyEventResult.ignored;
      },
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(8),
            child: Text('Row ${widget.row}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ),
          SizedBox(
            height: kCardHeight,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: kCardsPerRow,
              itemBuilder: (context, col) {
                return Focus(
                  canRequestFocus: false,
                  onFocusChange: (hasFocus) {
                    if (hasFocus) {
                      _selectedCard = col;
                    }
                  },
                  child: FocusCard(row: widget.row, col: col),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

// A single focusable card. It owns the focusable node and calls [Scrollable.ensureVisible] when focused.
class FocusCard extends StatefulWidget {
  const FocusCard({required this.row, required this.col, super.key});

  final int row;
  final int col;

  @override
  State<FocusCard> createState() => _FocusCardState();
}

class _FocusCardState extends State<FocusCard> {
  late final FocusNode _node = FocusNode(debugLabel: 'r${widget.row}c${widget.col}');
  bool _focused = false;

  @override
  void dispose() {
    _node.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Focus(
      focusNode: _node,
      autofocus: widget.row == 0 && widget.col == 0,
      onFocusChange: (hasFocus) {
        setState(() => _focused = hasFocus);
        if (hasFocus) {
          focusedLabel.value = 'r${widget.row}c${widget.col}';
          Scrollable.ensureVisible(
            context,
            alignment: 0.5,
            duration: const Duration(milliseconds: 300),
          );
        }
      },
      child: Container(
        width: kCardWidth,
        margin: const EdgeInsets.only(right: kCardGap),
        decoration: BoxDecoration(
          color: _focused ? Colors.amber : Colors.blueGrey,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: _focused ? Colors.white : Colors.transparent, width: 3),
        ),
        alignment: Alignment.center,
        child: Text(
          'r${widget.row}c${widget.col}',
          style: TextStyle(
            fontSize: 22,
            color: _focused ? Colors.black : Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
