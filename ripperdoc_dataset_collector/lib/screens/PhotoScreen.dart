import 'dart:io';

import 'package:dotted_border/dotted_border.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import "package:flutter/material.dart";
import 'package:image_picker/image_picker.dart';
import 'package:ripperdoc_dataset_collector/services/image_picker.dart';
import 'package:ripperdoc_dataset_collector/shared/constants.dart';
import 'package:ripperdoc_dataset_collector/shared/loading.dart';

class PhotoScreen extends StatefulWidget {
  @override
  _PhotoScreenState createState() => _PhotoScreenState();
}

class _PhotoScreenState extends State<PhotoScreen> {
  //Fields
  PickedFile imageFile;
  String instructionText = "Upload an Image", buttonText = "SEND";
  final _formKey = GlobalKey<FormState>();
  String logoText;

  //Private methods
  void _showLoading(BuildContext context) {
    showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) {
          return Loading(
            transparent: true,
          );
        });
  }

  Future<void> _pickImage() async {
    if (kIsWeb) {
      this.imageFile = await ImagePickerService.pickImage();
    } else {
      ImageSource imageSource;

      // Option to select either gallery or camera
      await showModalBottomSheet(
          context: context,
          builder: (BuildContext context) {
            return SafeArea(
              child: Container(
                child: Wrap(
                  children: [
                    ListTile(
                      leading: Icon(Icons.photo_library),
                      title: Text(
                        "Photo Library",
                      ),
                      onTap: () {
                        imageSource = ImageSource.gallery;
                        Navigator.of(context).pop();
                      },
                    ),
                    ListTile(
                      leading: Icon(Icons.photo_camera),
                      title: Text(
                        "Camera",
                      ),
                      onTap: () {
                        imageSource = ImageSource.camera;
                        Navigator.of(context).pop();
                      },
                    ),
                  ],
                ),
              ),
            );
          });

      // Use Image Picker
      if (imageSource != null) {
        this.imageFile = await ImagePickerService.pickImage(source: imageSource);
      }
    }
  }

  Widget _createUploadImageWidget() {
    return DottedBorder(
      color: Colors.black,
      strokeWidth: 2,
      dashPattern: [6, 3, 6, 3],
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          RawMaterialButton(
            // fillColor: Colors.grey[200],
            // shape: RoundedRectangleBorder(),
            onPressed: () async {
              await this._pickImage();
              this.setState(() {});
            },
            child: Icon(
              Icons.file_upload,
              size: 90,
            ),
          ),
        ],
      ),
    );
  }

  Widget _showImageWidget() {
    return GestureDetector(
      onTap: () async {
        await this._pickImage();
        this.setState(() {});
      },
      child: Card(
        // elevation: 2.0,
        color: Color.fromRGBO(255, 255, 255, 0.5),
        shadowColor: Colors.transparent,
        child: Container(
          padding: EdgeInsets.all(5.0),
          child: kIsWeb ? Image.network(
            this.imageFile.path,
            fit: BoxFit.scaleDown,
          ): Image.file(
            File(this.imageFile.path),
            fit: BoxFit.scaleDown,
          ),
        ),
      ),
    );
  }

  //Overridden Methods
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Container(
          // color: colorAppBase,
          decoration: decorationAppBase,
          child: Form(
            key: this._formKey,
            child: Center(
              child: SingleChildScrollView(
                scrollDirection: Axis.vertical,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  mainAxisSize: MainAxisSize.max,
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Align(
                      alignment: Alignment.center,
                      child: Text(
                        this.instructionText,
                        style: TextStyle(
                          fontSize: 30,
                          color: Colors.black,
                        ),
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.all(20.0),
                      child: Container(
                        color: this.imageFile == null
                            ? Color.fromRGBO(255, 255, 255, 0.5)
                            : Colors.transparent,
                        child: this.imageFile == null ?  this._createUploadImageWidget(): this._showImageWidget(),
                      ),
                    ),
                    SizedBox(
                      height: 20.0,
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(50, 0, 50, 30),
                      child: TextFormField(
                        decoration: InputDecoration(
                            hintText: "Enter logo in image"
                        ),
                        validator: (val) => val.trim().isEmpty ? 'Field cannot be empty' : null,
                        onChanged: (val) {
                          this.setState(() {
                            this.logoText = val;
                          });
                        },
                      ),
                    ),
                    SizedBox(
                      height: 10.0,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ElevatedButton(
                          onPressed: () async {
                            //TODO: Upload to firebase stoage
                          },
                          child: Padding(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10.0, vertical: 8.0),
                            child: Text(
                              this.buttonText,
                              style: TextStyle(
                                fontSize: 30,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(
                      height: 10.0,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
