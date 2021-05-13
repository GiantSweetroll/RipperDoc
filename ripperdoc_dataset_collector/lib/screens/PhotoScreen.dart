import 'dart:io';

import 'package:dotted_border/dotted_border.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import "package:flutter/material.dart";
import 'package:image_picker/image_picker.dart';
import 'package:package_info/package_info.dart';
import 'package:ripperdoc_dataset_collector/services/firebase_storage.dart';
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
  TextEditingController textEditingController = TextEditingController();
  String _error = "";
  final double uploadAreaSize = 300;
  StorageServices storageServices = StorageServices();
  final Color uploadImageBoxColor = Colors.black45;
  PackageInfo packageInfo;

  //Private methods
  void initPackageInfo() async {
    this.packageInfo = await PackageInfo.fromPlatform();
  }

  void resetFields() {
    this.setState(() {
      this._error = "";
      this.textEditingController.text = "";
      this.imageFile = null;
    });
  }

  void _showLoading(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return Loading(
          transparent: true,
        );
      }
    );
  }

  void _showInstructionsPage(BuildContext context) async {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text(
            "App Info",
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          content: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            child: Column(
              children: [
                Text(
                  "RipperDoc Collector is an app used to collect images to be used "
                      "in training the neural network AI for logo recognition,"
                      " particularly logos of tech companies.\n",
                  softWrap: true,
                ),
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                      "How to Use:",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
                Text(
                  "Upload a photo of an item with the logo visible (it can be in "
                      "any orientation). Then enter what logo it is in the text field"
                      " under it. Finish by hitting the SEND button.\n"
                ),
                Text(
                  "By using this app you agree and provide full consent for the RipperDoc team to use your"
                      " submitted images in anyway we see fit. \n\nThank you.\n\n"
                      "Running version: ${this.packageInfo.version}"
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text(
                "OK",
              ),
            ),
          ],
        );
      }
    );
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
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Expanded(
            child: RawMaterialButton(
              // fillColor: Colors.grey[200],
              // shape: RoundedRectangleBorder(),
              onPressed: () async {
                await this._pickImage();
                this.setState(() {});
              },
              child: Icon(
                Icons.file_upload,
                color: Colors.white,
                size: 90,
              ),
            ),
          )
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
        color: this.uploadImageBoxColor,
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
  void initState() {
    super.initState();
    this.initPackageInfo();
  }

  @override
  void dispose() {
    this.textEditingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.grey[900],
        title: Text(
          this.instructionText,
          style: TextStyle(
            // fontSize: 30,
            color: Colors.white,
          ),
        ),
        actions: [
          IconButton(
              icon: Icon(Icons.help_outline),
              onPressed: () {
                this._showInstructionsPage(context);
              },
          ),
        ],
      ),
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
                    Container(
                      padding: EdgeInsets.all(20.0),
                      child: Container(
                        height: this.uploadAreaSize,
                        width: this.uploadAreaSize,
                        color: this.imageFile == null
                            ? this.uploadImageBoxColor
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
                          hintText: "Enter logo",
                          hintStyle: TextStyle(
                            color: Colors.white,
                          ),
                          fillColor: Colors.black45,
                          filled: true,
                        ),
                        style: TextStyle(
                          color: Colors.white,
                        ),
                        controller: this.textEditingController,
                        validator: (val) => val.trim().isEmpty ? 'Field cannot be empty' : null,
                      ),
                    ),
                    Center(
                      child: Text(
                        this._error,
                        style: TextStyle(color: Colors.red),
                      ),
                    ),
                    SizedBox(
                      height: 10.0,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ElevatedButton(
                          onPressed: this.resetFields,
                          style: ButtonStyle(
                            backgroundColor: MaterialStateProperty.resolveWith((states) => Colors.red)
                          ),
                          child: Padding(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10.0, vertical: 8.0),
                            child: Text(
                              "RESET",
                              style: TextStyle(
                                fontSize: 30,
                              ),
                            ),
                          ),
                        ),
                        SizedBox(width: 20,),
                        ElevatedButton(
                          onPressed: () async {
                            // Validate input
                            if (this.imageFile != null && this._formKey.currentState.validate()) {
                              this.setState(() {
                                this._error = "";
                              });
                              this._showLoading(context);
                              // Upload to firebase storage
                              File f = File(this.imageFile.path);
                              // File f = File.fromRawPath(await this.imageFile.readAsBytes());
                              String url = await storageServices.uploadFile(f, this.textEditingController.text);
                              if (url.isEmpty) {
                                // Show error
                                this.setState(() {
                                  this._error = "Unable to send image due to an error";
                                });
                              } else {
                                // Reset fields
                                this.resetFields();
                              }
                              Navigator.pop(context);
                            } else {
                              this.setState(() {
                                this._error = "Please upload a photo and fill in the text field";
                              });
                            }
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
