import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: SliverCenteredExample()));

class SliverCenteredExample extends StatelessWidget {
  const SliverCenteredExample({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Centered SliverConstrainedCrossAxis')),
      body: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 300),
        child: CustomScrollView(
          slivers: <Widget>[
            SliverCrossAxisGroup(
              slivers: <Widget>[
                // Flexible left spacer / column
                SliverCrossAxisExpanded(
                  flex: 1,
                  sliver: SliverToBoxAdapter(
                    child: Container(
                      color: Colors.blue.withValues(alpha: 0.1),
                      height: 400,
                      alignment: Alignment.center,
                      child: const Text('Expanded (Left)'),
                    ),
                  ),
                ),

                // Center content with fixed constrained width (e.g. 300 px)
                SliverConstrainedCrossAxis(
                  maxExtent: 300.0,
                  sliver: SliverList.builder(
                    itemCount: 15,
                    itemBuilder: (BuildContext context, int index) {
                      return Card(
                        color: Colors.amber.shade100,
                        margin: const EdgeInsets.symmetric(
                          vertical: 4.0,
                          horizontal: 8.0,
                        ),
                        child: ListTile(
                          leading: CircleAvatar(child: Text('${index + 1}')),
                          title: Text('Center item ${index + 1}'),
                        ),
                      );
                    },
                  ),
                ),

                // Flexible right spacer / column
                SliverCrossAxisExpanded(
                  flex: 1,
                  sliver: SliverToBoxAdapter(
                    child: Container(
                      color: Colors.blue.withValues(alpha: 0.1),
                      height: 400,
                      alignment: Alignment.center,
                      child: const Text('Expanded (Right)'),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
