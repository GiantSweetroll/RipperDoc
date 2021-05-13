import 'dart:typed_data';

Uint8List convertStringToUint8List(String byteData) {
  List<int> list = List.empty(growable: true);

  //Converts String to Uint8List
  byteData.runes.forEach((rune) {
    if (rune >= 0x10000) {
      rune -= 0x10000;
      int firstWord = (rune >> 10) + 0xD800;
      list.add(firstWord >> 8);
      list.add(firstWord & 0xFF);
      int secondWord = (rune & 0x3FF) + 0xDC00;
      list.add(secondWord >> 8);
      list.add(secondWord & 0xFF);
    }
    else {
      list.add(rune >> 8);
      list.add(rune & 0xFF);
    }
  });

  return Uint8List.fromList(list);
}