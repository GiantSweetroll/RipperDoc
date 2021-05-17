import "package:flutter/material.dart";

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

  // Overridden Methods
  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Expanded(
          flex: 1,
          // TODO: replace this with google maps widget
          child: Container(
            decoration: BoxDecoration(
              color: Colors.amber,
            ),
          ),
        ),
        Expanded(
          flex: 1,
          child: ListView.builder(
            itemBuilder: (context, index) {
              // TODO: Replace this with the actual location
              return ListTile(
                title: Text("Location $index"),
              );
            },
          )
        )
      ],
    );
  }
}
