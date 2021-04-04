import 'dart:io';

import 'package:firebase_storage/firebase_storage.dart';
import 'package:path/path.dart';

class StorageServices {
  FirebaseStorage storage = FirebaseStorage(
      storageBucket: 'gs://ripperdoc-53af5.appspot.com/'
  );

  ///Uploads a file to the firebase storage
  Future<String> uploadFile(File file, String label) async {

    try {
      //Upload to firebase storage

      String fName = DateTime.now().toString() + "-" + basename(file.path);
      StorageReference storageRef = this.storage.ref().child('user_collected/$label/$fName');
      StorageUploadTask uploadTask = storageRef.putFile(file);
      StorageTaskSnapshot completedTask = await uploadTask.onComplete;

      //Get the download link url
      String downloadUrl = await completedTask.ref.getDownloadURL();

      return downloadUrl;
    } catch(e) {
      print(e.toString());
      return "";
    }
  }
}