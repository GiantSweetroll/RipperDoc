import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:ripperdoc_frontend/widgets/NavDrawer.dart';



class HistoryScreen extends StatelessWidget {

  @override
  Widget build(BuildContext context) {

    final title = 'History';
    return Scaffold(
        appBar: AppBar(
          title: Text(title),
        ),
        body:  ListView.builder(
          itemBuilder: (context, index) {
            // TODO: Replace this with the actual location
            return ListTile(
              title: Text(
                "Location $index",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
            );
          },
        )
    );
  }
}