import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

void main() => runApp(App());

class App extends StatelessWidget {
  App({super.key});

  late final GoRouter router = GoRouter(
    initialLocation: '/protected',
    onEnter: (_, __, next, ___) =>
        next.matchedLocation == '/protected' ? const Block.stop() : const Allow(),
    onException: (context, state, router) => router.go('/fallback'),
    routes: [
      GoRoute(path: '/protected', builder: (_, __) => const SizedBox()),
      GoRoute(path: '/fallback', builder: (_, __) => const SizedBox()),
    ],
  );

  @override
  Widget build(BuildContext context) => MaterialApp.router(routerConfig: router);
}
