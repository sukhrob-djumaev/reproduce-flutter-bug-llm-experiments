import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// Harness only: GoRouter definition below is copied verbatim from the issue's widget test.
final router = GoRouter(
  initialLocation: '/home',
  routes: [
    StatefulShellRoute.indexedStack(
      builder: (_, __, shell) => Scaffold(
        body: shell,
        bottomNavigationBar: Row(children: [
          TextButton(
            key: const Key('toHome'),
            onPressed: () => shell.goBranch(0),
            child: const Text('home'),
          ),
          TextButton(
            key: const Key('toSettings'),
            onPressed: () => shell.goBranch(1),
            child: const Text('settings'),
          ),
        ]),
      ),
      branches: [
        StatefulShellBranch(routes: [
          GoRoute(path: '/home', builder: (_, __) => const Text('HOME')),
        ]),
        StatefulShellBranch(routes: [
          GoRoute(
            path: '/settings',
            builder: (c, __) => TextButton(
              key: const Key('toGeneral'),
              onPressed: () => c.go('/settings/general'),
              child: const Text('SETTINGS'),
            ),
            routes: [
              GoRoute(path: 'general', builder: (_, __) => const Text('GENERAL')),
            ],
          ),
        ]),
      ],
    ),
  ],
);

void main() => runApp(MaterialApp.router(routerConfig: router));
