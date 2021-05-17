import 'package:flutter/material.dart';

import 'package:ripperdoc_frontend/widgets/NavDrawer.dart';
import 'package:ripperdoc_frontend/widgets/PhotoScreen.dart';

void main() {
  runApp(MaterialApp(
    title: "RipperDoc",
    theme: ThemeData(
      primarySwatch: Colors.blue,
    ),
    home: PhotoScreen(),    // TODO: change this to a wrapper class for cloud firestore
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