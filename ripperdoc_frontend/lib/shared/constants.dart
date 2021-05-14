import "package:flutter/material.dart";

final String domainName = "localhost:5000";
final String backendSubdomain = "api-backend";

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