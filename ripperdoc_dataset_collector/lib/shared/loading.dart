import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:ripperdoc_dataset_collector/shared/constants.dart';

class Loading extends StatelessWidget {

  final bool transparent;

  Loading({ this.transparent = false });

  Widget _createSpinKitWidget() {
    return Center(
      child: SpinKitFadingCircle(
        color: Colors.blue[400],
        size: 50.0,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return this.transparent ? Container(
      color: Colors.transparent,
      child: this._createSpinKitWidget(),
    ) : Container(
      decoration: decorationAppBase,
      child: this._createSpinKitWidget(),
    );
  }
}
