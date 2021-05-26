

import 'package:flutter/material.dart';
import 'package:ripperdoc_frontend/widgets/HistoryScreen.dart';
import 'package:ripperdoc_frontend/widgets/LocationScreen.dart';

import 'package:ripperdoc_frontend/widgets/NavDrawer.dart';
import 'package:ripperdoc_frontend/widgets/PhotoScreen.dart';

void main() {
  runApp(MaterialApp(
    title: "RipperDoc",
    theme: ThemeData(
      primarySwatch: Colors.blue,
    ),
    initialRoute: '/home', // TODO: change this to a wrapper class for cloud firestore
    routes: {
      '/home': (context) => PhotoScreen(),
      '/history': (context) => HistoryScreen(),
    },
  ));
}
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: NavDrawer(),
      appBar: AppBar(
        title: Text('RipperDoc'),
      ),
      body: Center(
        child: Text("Home"),
      ),
    );
  }
}