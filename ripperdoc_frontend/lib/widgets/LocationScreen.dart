import "package:flutter/material.dart";
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:ripperdoc_frontend/widgets/NavDrawer.dart';

class LocationScreen extends StatefulWidget {

  // Fields
  final _searchKeyword;

  // Constructor
  LocationScreen(this._searchKeyword);

  // Overridden Methods
  @override
  _LocationScreenState createState() => _LocationScreenState(_searchKeyword);
}

class _LocationScreenState extends State<LocationScreen> {

  //Fields
  String searchKeyword;

  // Constructor
  _LocationScreenState(this.searchKeyword);

  // Methods
  List<Widget> getMainWidgets() {
    return [
      Expanded(
        flex: 2,
        // TODO: replace this with google maps widget
        child: Container(
          decoration: BoxDecoration(
            color: Colors.amber,
          ),
          child: Center(
            child: Text(
              "Google Maps goes here",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 30,
              ),
            ),
          ),
        ),
      ),
      Expanded(
          flex: 1,
          child: ListView.builder(
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
      )
    ];
  }

  // Overridden Methods
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Ripper Doc")),
      body: kIsWeb || MediaQuery.of(context).orientation == Orientation.landscape ? Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: getMainWidgets(),
      ) : Column(
        children: getMainWidgets(),
      ),
    );
  }
}
