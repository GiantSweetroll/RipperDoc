import 'dart:async';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:image_picker/image_picker.dart';

class ImagePickerService {
  static Future<PickedFile> pickImage({ImageSource source }) async {
    final ImagePicker picker = ImagePicker();
    return kIsWeb ? await picker.getImage() : await picker.getImage(source: source);
  }
}