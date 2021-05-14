import "package:flutter/material.dart";
import 'package:flutter/foundation.dart' show kIsWeb;

const String domainName = kIsWeb ? "localhost" : "10.0.2.2";
const String backendSubdomain = "api-backend";
const int backendPort = 5000;

const Color colorAppBase = Color.fromRGBO(203, 222, 192, 1.0);
const Color colorAppSecondary = Color.fromRGBO(203, 250, 192, 1.0);

const BoxDecoration decorationAppBase = BoxDecoration(
  gradient: LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      stops: [0.1, 0.9],
      colors: [
        colorAppBase,
        colorAppBase,
      ]
  ),
);

const InputDecoration inputTextDecoration = InputDecoration(
  hintText: "",
  labelText: "",
);