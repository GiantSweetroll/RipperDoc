import 'package:flutter/material.dart';

const Color colorAppBase = Color.fromRGBO(203, 222, 192, 1.0);
const Color colorAppSecondary = Color.fromRGBO(203, 250, 192, 1.0);

const double defaultFontSize = 30;

const BoxDecoration decorationAppBase = BoxDecoration(
  // image: DecorationImage(
  //   image: AssetImage("assets/mainmenubg_whiteonly.png"),
  //   fit: BoxFit.cover,
  // ),
  gradient: LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    stops: [0.1, 0.9],
    colors: [
      colorAppBase,
      colorAppBase,
    ]
  ),
  image: DecorationImage(
    image: AssetImage("assets/bg1.jpg"),
    fit: BoxFit.fill,
  ),
);

const InputDecoration inputTextDecoration = InputDecoration(
  hintText: "",
  labelText: "",
);