# Horus Project

## Overview

The Horus Project is a multifaceted application that integrates camera feed processing with voice commands to enable object and text detection functionalities. The project is split into three main Python scripts: `camera.py`, `detect.py`, and `speech2text.py`. The project leverages the power of Google's Vision API for image analysis.

## Scripts

### camera.py

The main script that coordinates the functionalities of the entire project. It sets up video capture using OpenCV, continuously retrieves frames from a camera feed, and listens for voice commands to trigger object or text detection on the frames. 

### detect.py

Contains functions that communicate with the Google Vision API to perform text and object detection on the frames received from the camera feed. It also handles speaking out the detected text or objects using pyttsx3, a text-to-speech conversion library. Additionally, this script contains utility functions for image display and verification of detected words using the nltk library.

### speech2text.py

Contains a function that sets up a speech recognizer to listen for voice commands through a specific microphone (DroidCam) that is streamed through IP. This script leverages the speech_recognition library to convert spoken commands into text, which can then be used to trigger various actions in the `camera.py` script.

## How It Works

1. **Camera Feed Setup**
   
   The `camera.py` script connects to a video feed through an IP webcam app and continuously captures frames from this feed. It also starts a separate thread to listen for voice commands.

2. **Voice Commands**
   
   Users can give voice commands such as "scan", "read", and "quit". The "scan" and "read" commands trigger object and text detection respectively on the current frame from the camera feed, while the "quit" command exits the application.

3. **Text and Object Detection**
   
   The `detect.py` script uses the Google Vision API to analyze the captured frames for text and objects. Detected text and objects are spoken out loud using the pyttsx3 library, and the frames with detection bounding boxes are saved as images.

4. **Speech-to-Text**
   
   The `speech2text.py` script sets up a microphone (preferably DroidCam) to listen for voice commands and convert them into text using the speech_recognition library.

   
