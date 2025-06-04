# titensor_photography
This is the Repo for all projects related to Titensor Photography



Current Projects:

*Check In - complete

*Database Upload - complete

*QR Code/Facial Recognition - in progress

## Kivy Registration App

`RegistrationApp_kivy.py` implements a Kivy version of the original Tkinter registration form. This code can be packaged for iOS using the [Kivy iOS](https://kivy.org/doc/stable/guide/packaging-ios.html) toolchain.

To run the app on desktop:

```bash
pip install kivy pillow pyqrcode pandas phonenumbers
python RegistrationApp_kivy.py
```

Packaging for iPad requires a Mac with Xcode and the Kivy iOS toolchain. Follow Kivy's documentation to build and deploy to an iOS device.

## KivyMD Registration App

`RegistrationApp_kivymd.py` provides the same functionality using [KivyMD](https://kivymd.readthedocs.io/) for a more modern look inspired by the ChatGPT app.

To run:

```bash
pip install kivy kivymd pillow pyqrcode pandas phonenumbers
python RegistrationApp_kivymd.py
```

While Kivy works cross‑platform, for a fully native iOS experience consider porting the interface to SwiftUI.

## SwiftUI Registration App

`RegistrationApp_SwiftUI.swift` contains a SwiftUI implementation of the registration form. Create a new iOS
project in Xcode and replace the default code with this file to run natively on iPad or iPhone. The view model
stores entries in `registration.csv` inside the app's documents directory and also generates a QR code for each
submission using Core Image.
