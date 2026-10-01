import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

void main() {
  runApp(const MyApp());
}

final GoRouter _router = GoRouter(
  initialLocation: '/A1',
  routes: [
    StatefulShellRoute.indexedStack(
      builder:
          (
            BuildContext context,
            GoRouterState state,
            StatefulNavigationShell navigationShell,
          ) {
            return BottomNavWrapper(navigationShell: navigationShell);
          },
      branches: <StatefulShellBranch>[
        StatefulShellBranch(
          initialLocation: '/A1',
          observers: [LoggingObserver('/A')],
          routes: <RouteBase>[
            GoRoute(
              path: '/A1',
              builder: (BuildContext context, GoRouterState state) =>
                  MyTestPage(
                    title: 'Stack A - 1',
                    nextRoutePath: '/A1/A2',
                    canPop: false,
                  ),
              routes: [
                GoRoute(
                  path: '/A2',
                  builder: (BuildContext context, GoRouterState state) =>
                      MyTestPage(
                        title: 'Stack A - 2',
                        nextRoutePath: '/A1/A2/A3',
                      ),
                  routes: [
                    GoRoute(
                      path: '/A3',
                      builder: (BuildContext context, GoRouterState state) =>
                          MyTestPage(title: 'Stack A - 3'),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),

        StatefulShellBranch(
          initialLocation: '/B1',
          observers: [LoggingObserver('/B')],
          routes: <RouteBase>[
            GoRoute(
              path: '/B1',
              builder: (BuildContext context, GoRouterState state) =>
                  MyTestPage(title: 'Stack B - 1', canPop: false),
            ),
          ],
        ),

        StatefulShellBranch(
          initialLocation: '/C1',
          observers: [LoggingObserver('/C')],
          routes: <RouteBase>[
            GoRoute(
              path: '/C1',
              builder: (BuildContext context, GoRouterState state) =>
                  MyTestPage(
                    title: 'Stack C - 1',
                    nextRoutePath: '/C1/C2',
                    canPop: false,
                  ),
              routes: [
                GoRoute(
                  path: '/C2',
                  builder: (BuildContext context, GoRouterState state) =>
                      MyTestPage(title: 'Stack C - 2'),
                ),
              ],
            ),
          ],
        ),
      ],
    ),
  ],
);

class BottomNavWrapper extends StatelessWidget {
  final StatefulNavigationShell navigationShell;

  const BottomNavWrapper({super.key, required this.navigationShell});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        onDestinationSelected: (int index) {
          navigationShell.goBranch(index, initialLocation: false);
        },
        selectedIndex: navigationShell.currentIndex,
        destinations: <Widget>[
          NavigationDestination(
            icon: Icon(Icons.navigation_outlined),
            selectedIcon: Icon(Icons.navigation),
            label: 'A',
          ),
          NavigationDestination(
            icon: Icon(Icons.navigation_outlined),
            selectedIcon: Icon(Icons.navigation),
            label: 'B',
          ),
          NavigationDestination(
            icon: Icon(Icons.navigation_outlined),
            selectedIcon: Icon(Icons.navigation),
            label: 'C',
          ),
        ],
      ),
    );
  }
}

class LoggingObserver extends NavigatorObserver {
  final String name;

  LoggingObserver(this.name);

  @override
  void didPop(Route route, Route? previousRoute) {
    debugPrint(
      '$name didPop ${route.settings.name} -> ${previousRoute?.settings.name}',
    );
  }

  @override
  void didPush(Route route, Route? previousRoute) {
    debugPrint('$name didPush ${route.settings.name}');
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    super.initState();
    _router.routerDelegate.addListener(() {
      debugPrint(
        'Location: '
        '${_router.routerDelegate.currentConfiguration.last.matchedLocation}',
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(title: 'Go Router Bug', routerConfig: _router);
  }
}

class MyTestPage extends StatefulWidget {
  const MyTestPage({
    super.key,
    required this.title,
    this.nextRoutePath,
    this.canPop = true,
  });

  final String title;
  final String? nextRoutePath;
  final bool canPop;

  @override
  State<MyTestPage> createState() => _MyTestPageState();
}

class _MyTestPageState extends State<MyTestPage> {
  @override
  void dispose() {
    debugPrint('${widget.title} dispose');
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: widget.canPop,
      onPopInvokedWithResult: (bool didPop, Object? result) {
        debugPrint('${widget.title} onPopInvokedWithResult didPop=$didPop');
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text(widget.title),
          leading: widget.canPop
              ? IconButton(
                  icon: const Icon(Icons.chevron_left),
                  onPressed: () => Navigator.of(context).maybePop(),
                )
              : null,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: .center,
            children: [
              Text(
                widget.title,
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              if (widget.nextRoutePath != null)
                Padding(
                  padding: const EdgeInsets.only(top: 16.0),
                  child: ElevatedButton(
                    onPressed: () => context.push(widget.nextRoutePath!),
                    child: Text('Push one screen'),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
