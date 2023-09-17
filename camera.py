import cv2
import pytesseract

from threading import Thread
from detect import detect_text, detect_objects, speak_queue
from speech2text import get_voice_command 

keep_running = True

def voice_command_listener():
    global keep_running  # Declare keep_running as global
    while keep_running:  # Loop while keep_running is True
        command = get_voice_command()
        if command in ["scan", "read"]:
            global trigger_detection
            trigger_detection = command
        elif command == "quit":
            keep_running = False

def main():
    global trigger_detection
    global keep_running  # Declare keep_running as global
    trigger_detection = False
    
    # Configure the path to the tesseract executable (adjust path as necessary)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
    
    # Use the IP address and port from the IP webcam app to capture video
    # Replace '192.168.X.X:XXXX' with the IP address and port displayed in your IP webcam app
    cap = cv2.VideoCapture('http://10.189.83.213:4747/video')
    
    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    while keep_running:  # Check the value of keep_running in the loop condition
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If frame is read correctly, ret is True
        if not ret:
            print("Error: Could not read frame")
            break

        # Trim the top portion of the frame
        height, _, _ = frame.shape
        trim_ratio = 0.1  # Adjust the ratio as needed to trim the appropriate amount
        trimmed_frame = frame[int(height*trim_ratio):, :, :]

        # Display the frame
        cv2.imshow('Horus Video Feed', trimmed_frame)
        
        # If 's' key is pressed, take a screenshot and perform OCR on it
        if trigger_detection or cv2.waitKey(1) & 0xFF == ord('s'):
            
            if trigger_detection == "scan":
                scan_thread = Thread(target=detect_objects, args=(trimmed_frame,))
                scan_thread.start()
            elif trigger_detection == "read":
                read_thread = Thread(target=detect_text, args=(trimmed_frame,))
                read_thread.start()

            trigger_detection = None
        
        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            keep_running = False
            break

    # When everything is done, release the capture and close any open windows
    cap.release()
    cv2.destroyAllWindows()

    # Add this line to signal the speak_thread to exit
    speak_queue.put(None)


if __name__ == "__main__":
    # Start the voice command listener in a separate thread
    voice_command_thread = Thread(target=voice_command_listener)
    voice_command_thread.start()

    main()

    # Join the thread to wait for its completion before exiting the program
    voice_command_thread.join()
