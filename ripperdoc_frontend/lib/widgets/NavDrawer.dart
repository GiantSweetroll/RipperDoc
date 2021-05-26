import 'package:flutter/material.dart';
import 'package:ripperdoc_frontend/widgets/PhotoScreen.dart';
import 'package:ripperdoc_frontend/widgets/HistoryScreen.dart';
import 'package:ripperdoc_frontend/main.dart';


class NavDrawer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          DrawerHeader(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'My RipperDoc',
                  style: TextStyle(color: Colors.grey[100], fontSize: 25),
                ),
                SizedBox(height: 5.0,),
                Text(
                  'Find the suitable repair shop for you',
                  style: TextStyle(color: Colors.grey[300], fontSize: 15),
                ),
              ],
            ),

            decoration: BoxDecoration(
              color: Colors.blueAccent[400],
            ),
          ),
          ListTile(
            leading: Icon(Icons.history),
            title: Text('History'),
            onTap: () => {
              Navigator.of(context).pop(),
              Navigator.pushNamed(context, '/history')
            },
          ),
          ListTile(
            leading: Icon(Icons.logout),
            title: Text('Sign Out'),
            onTap: () => {Navigator.of(context).pop()},
          ),
        ],
      ),
    );
  }
}