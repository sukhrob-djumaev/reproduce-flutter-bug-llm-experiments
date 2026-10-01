import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:two_dimensional_scrollables/two_dimensional_scrollables.dart';

void main() {
  runApp(const MaterialApp(home: Scaffold(body: ReproTable())));
}

class ReproTable extends StatefulWidget {
  const ReproTable({super.key});

  @override
  State<ReproTable> createState() => _ReproTableState();
}

class _ReproTableState extends State<ReproTable> {
  final ScrollController horizontalController = ScrollController();

  @override
  Widget build(BuildContext context) {
    return Scrollbar(
      controller: horizontalController,
      thumbVisibility: true,
      scrollbarOrientation: ScrollbarOrientation.bottom,
      child: TableView.builder(
        horizontalDetails: ScrollableDetails.horizontal(
          controller: horizontalController,
        ),
        cacheExtent: 0,
        columnCount: 20,
        rowCount: 20,
        trailingPinnedColumnCount: 1,
        columnBuilder: (int column) =>
            TableSpan(extent: FixedTableSpanExtent(column == 19 ? 64 : 200)),
        rowBuilder: (int row) => TableSpan(
          extent: const FixedTableSpanExtent(48),
          recognizerFactories: row == 0
              ? const <Type, GestureRecognizerFactory>{}
              : <Type, GestureRecognizerFactory>{
                  TapGestureRecognizer:
                      GestureRecognizerFactoryWithHandlers<
                        TapGestureRecognizer
                      >(() => TapGestureRecognizer(), (
                        TapGestureRecognizer recognizer,
                      ) {
                        recognizer.onTap = () => debugPrint('row tapped: $row');
                      }),
                },
        ),
        cellBuilder: (BuildContext context, TableVicinity vicinity) {
          if (vicinity.column == 19 && vicinity.row > 0) {
            return TableViewCell(
              child: PopupMenuButton<int>(
                icon: const Icon(Icons.more_vert),
                itemBuilder: (_) => [
                  PopupMenuItem<int>(
                    value: vicinity.row,
                    child: Text('Action ${vicinity.row}'),
                  ),
                ],
                onOpened: () => debugPrint('popup opened: ${vicinity.row}'),
              ),
            );
          }

          return TableViewCell(
            child: Text('row ${vicinity.row}, column ${vicinity.column}'),
          );
        },
      ),
    );
  }
}
