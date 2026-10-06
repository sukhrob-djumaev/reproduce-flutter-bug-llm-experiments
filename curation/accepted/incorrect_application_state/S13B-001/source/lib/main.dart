import 'package:flutter/material.dart';
import 'package:list_smith/list_smith.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: SafeArea(
          child: ListSmith.async(
            fetchPage: PageFetcher(
              (request) => fetchArticles(
                page: request.pageIndex,
                size: request.pageSize,
              ),
            ),
            refresh: PullToRefresh(),
            itemBuilder: (context, article, index) =>
                ArticleTile(article: article),
          ),
        ),
      ),
    );
  }
}

class ArticleTile extends StatelessWidget {
  const ArticleTile({super.key, required this.article});

  final Article article;
  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}

Future<List<Article>> fetchArticles({
  required int page,
  required int size,
}) async {
  return Future.delayed(const Duration(seconds: 3), () {
    return Future.value([
      Article(body: 'Body1' * 3, title: 'Title 1'),
      Article(body: 'Body2' * 3, title: 'Title 2'),
      Article(body: 'Body3' * 3, title: 'Title 3'),
    ]);
  });
}

class Article {
  final String title;
  final String body;

  Article({required this.title, required this.body});
}

