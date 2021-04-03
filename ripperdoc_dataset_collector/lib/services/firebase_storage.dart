import 'dart:io';

import 'package:firebase_storage/firebase_storage.dart';

class StorageServices {
  FirebaseStorage storage = FirebaseStorage(
      storageBucket: 'gs://ripperdoc-53af5.appspot.com/'
  );

  ///Uploads a file to the firebase storage
  Future<String> uploadFile(File file) async {

    //Upload to firebase storage
    StorageReference storageRef = this.storage.ref().child('user_collected/');
    StorageUploadTask uploadTask = storageRef.putFile(file);
    StorageTaskSnapshot completedTask = await uploadTask.onComplete;

    //Get the download link url
    String downloadUrl = await completedTask.ref.getDownloadURL();

    return downloadUrl;
  }
}