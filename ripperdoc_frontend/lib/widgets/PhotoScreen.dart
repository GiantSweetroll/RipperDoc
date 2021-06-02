import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';


import 'package:ripperdoc_frontend/widgets/NavDrawer.dart';
import 'package:ripperdoc_frontend/widgets/PhotoScreen.dart';
import 'package:dotted_border/dotted_border.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import "package:flutter/material.dart";
import 'package:http/http.dart';
import 'package:image_picker/image_picker.dart';
import 'package:ripperdoc_frontend/services/api_services.dart';
import 'package:ripperdoc_frontend/services/image_picker_service.dart';
import 'package:ripperdoc_frontend/shared/loading.dart';
import 'package:ripperdoc_frontend/widgets/LocationScreen.dart';
import 'package:image/image.dart' as conv ;
import 'package:ripperdoc_frontend/services/convertJpg.dart' as something;

import '../shared/constants.dart';

class PhotoScreen extends StatefulWidget {
  @override
  _PhotoScreenState createState() => _PhotoScreenState();
}

class _PhotoScreenState extends State<PhotoScreen> {
  //Fields
  PickedFile imageFile;
  String instructionText = "Upload an Image", buttonText = "SEARCH";
  final _formKey = GlobalKey<FormState>();
  TextEditingController textEditingController = TextEditingController();
  String _error = "";
  final double uploadAreaSize = 300;
  final Color uploadImageBoxColor = Colors.black45;
  bool isSubmitPicture = true;    // State whether to upload image to backend or to search brand

  //Private methods
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
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.file_upload,
                    color: Colors.white,
                    size: 90,
                  ),
                  Center(
                    child: Text(
                      this.instructionText,
                      style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 32,
                          color: Colors.white
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
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

  /// Create the main widget of the screen
  Widget _createMainWidget() {
    return Form(
      key: this._formKey,
      child: Center(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            Padding(
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
            Row(
              children: [
                Expanded(
                  child: Container(
                      margin: const EdgeInsets.only(left: 10.0, right: 20.0),
                      child: Divider(
                        color: Colors.black,
                        height: 36,
                      )),
                ),
                Text(
                  "or",
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                  ),
                ),
                Expanded(
                  child: Container(
                      margin: const EdgeInsets.only(left: 10.0, right: 20.0),
                      child: Divider(
                        color: Colors.black,
                        height: 36,
                      )),
                ),
              ],
            ),
            SizedBox(height: (20),),
            Padding(
              padding: const EdgeInsets.fromLTRB(50, 0, 50, 30),
              child: TextFormField(
                decoration: InputDecoration(
                  hintText: "Enter brand",
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
                validator: (val) {
                  if (this.isSubmitPicture) {
                    this.isSubmitPicture = false;
                  }

                  if (val.trim().isEmpty && !this.isSubmitPicture) {
                    this.isSubmitPicture = true;
                    return null;
                  } else {
                    return null;
                  }
                },
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
                    if (this.isSubmitPicture && this.imageFile != null) {
                      this.setState(() {
                        this._error = "";
                      });
                      this._showLoading(context);

                      //Convert To JPG
                      var decodeImage = conv.decodeImage(await this.imageFile.readAsBytes());
                      var encodeToJpg = conv.encodeJpg(decodeImage);

                      String base64String = base64.encode(encodeToJpg);

                      // Post request to backend
                      try {
                        Response r = await postImage("1", base64String);    // TODO: change ID according to cloud firestore ID
                        if (r.statusCode != 200) {
                          this.setState(() {
                            this._error = "Unable to process image due to an error (${r.statusCode})";
                          });
                          Navigator.pop(context);
                        } else {
                          final body = json.decode(r.body);
                          String logo = body['result'];
                          print(logo);
                          String query = "$logo repair shop";
                          Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => LocationScreen(query)));
                          // TODO: use this to query for repair service
                        }
                      } catch (e, stacktrace) {
                        print(e);
                        print(stacktrace);
                        Navigator.pop(context);
                      }
                    } else if (!this.isSubmitPicture && this._formKey.currentState.validate()) {
                      // TODO: perform google search based on user input
                      String query = "${this.textEditingController.text} repair shop";    // TODO: change as needed
                    } else{
                      this.setState(() {
                        this._error = this.isSubmitPicture ? "Please upload a photo" : "Please upload a photo or fill in the text field";
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
    );
  }

  //Overridden Methods
  @override
  void dispose() {
    this.textEditingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Ripper Doc")),
      drawer: NavDrawer(),
      body: SafeArea(
        child: Container(
          decoration: decorationAppBase,
          child: Center(
            child: SingleChildScrollView(
              scrollDirection: Axis.vertical,
              child: Center(
                child: kIsWeb ? SizedBox(
                  // color: colorAppBase,
                  width: this.uploadAreaSize,
                  child: this._createMainWidget(),
                ) : MediaQuery.of(context).orientation == Orientation.portrait ? this._createMainWidget() : SizedBox(
                  width: this.uploadAreaSize + 200,
                  child: this._createMainWidget(),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
