import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:ripperdoc_frontend/shared/constants.dart';

/// POST image into backend server
///
/// userID: the user id from firebase
/// base64String: the image bytes string encoded in Base64 format
Future<http.Response> postImage(String userID, String base64String) {
  return http.post(
    Uri.https(domainName, "$backendSubdomain/$userID"),
    headers: <String, String> {
      'Content-Type' : 'application/json; charset=UTF-8'
    },
    body: jsonEncode(<String, String> {
      "image" : base64String,
    }),
  );
}

/// GET the identified logo served from backend server.
///
/// userID; the user id from firebase
Future<http.Response> getLogoLabel(String userID) {
  return http.get(Uri.https(domainName, "$backendSubdomain/$userID"));
}