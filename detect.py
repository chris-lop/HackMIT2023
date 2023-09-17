import os
from google.cloud import vision
import io
import numpy as np
import cv2
import time
import pyttsx3
from threading import Thread
from nltk.corpus import words
import nltk
from queue import Queue

# Download the words corpus for detection of actual words
nltk.download('words')

# Set up the path to your service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\chris\Documents\GitHub\HackMIT2023\hackmit2023-399222-8744ab18af31.json"

english_words = set(words.words())

# Create a single instance of the pyttsx3 engine
engine = pyttsx3.init()

# Create a queue for thread-safe speaking of text
speak_queue = Queue()

def speak_worker():
    while True:
        text = speak_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speak_queue.task_done()

# Start a separate thread to handle speaking text
speak_thread = Thread(target=speak_worker)
speak_thread.start()

def speak_text(text):
    speak_queue.put(text)

def is_actual_word(text):
    return any(word.lower() in english_words for word in text.split())


def display_image(window_name, frame):
    # Check if the 'img' directory exists, if not, create it
    if not os.path.exists('img'):
        os.makedirs('img')
    
    # Generate a filename using the window_name and current timestamp
    filename = os.path.join('img', f'{window_name}_{int(time.time())}.jpg')
    
    # Save the image
    cv2.imwrite(filename, frame)
    
    print(f"Image saved at: {filename}")


def detect_text(frame):
    client = vision.ImageAnnotatorClient()

    # Convert the OpenCV image (in BGR format) to RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Encode the image as JPEG
    _, buffer = cv2.imencode('.jpg', rgb_frame)
    
    # Convert the image to bytes
    image_bytes = io.BytesIO(buffer).read()

    # Prepare the image data for the Vision API
    image = vision.Image(content=image_bytes)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    # Prepare a copy of the frame to draw bounding boxes
    frame_with_boxes = frame.copy()

    # Get detected texts and their bounding boxes
    for text in texts[1:]:  # Start from 1 to skip the first element which contains all detected text
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        cv2.polylines(frame_with_boxes, [np.array(vertices)], isClosed=True, color=(0, 255, 0), thickness=2)
        
        if is_actual_word(text.description):
            print('\n"{}"'.format(text.description))
            speak_text(text.description)

    # Display the frame with bounding boxes in a new window using a separate thread
    display_thread = Thread(target=display_image, args=('Text Detection', frame_with_boxes))
    display_thread.start()
    

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def detect_objects(frame):
    client = vision.ImageAnnotatorClient()

    # Convert the OpenCV image (in BGR format) to RGB format
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Encode the image as JPEG
    _, buffer = cv2.imencode('.jpg', rgb_frame)

    # Convert the image to bytes
    image_bytes = io.BytesIO(buffer).read()

    # Prepare the image data for the Vision API
    image = vision.Image(content=image_bytes)

    # Perform object detection
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    # Prepare a list to store descriptions of detected objects
    descriptions = []


    # Prepare a copy of the frame to draw bounding boxes
    frame_with_boxes = frame.copy()

    # Get detected objects and their bounding boxes
    for object_ in objects:
        vertices = [(vertex.x * frame_with_boxes.shape[1], vertex.y * frame_with_boxes.shape[0]) for vertex in object_.bounding_poly.normalized_vertices]
        cv2.polylines(frame_with_boxes, [np.array(vertices, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)
        
        print('\n"{}"'.format(object_.name))
        speak_text(object_.name)

    # Display the frame with bounding boxes in a new window using a separate thread
    display_thread = Thread(target=display_image, args=('Object Detection', frame_with_boxes))
    display_thread.start()

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return descriptions
