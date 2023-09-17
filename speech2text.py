import speech_recognition as sr

def get_voice_command():
    recognizer = sr.Recognizer()
    
    # List all microphones and select the DroidCam microphone by its index
    mic_list = sr.Microphone.list_microphone_names()

    droidcam_mic_index = None
    for index, name in enumerate(mic_list):
        if 'DroidCam' in name:  # replace 'DroidCam' with the actual name or part of the name of your DroidCam microphone
            droidcam_mic_index = index
            break
    
    if droidcam_mic_index is None:
        print("DroidCam microphone not found!")
        return None

    print(f"Using microphone: {mic_list[droidcam_mic_index]}")  # This line will print the name of the selected microphone

    microphone = sr.Microphone(device_index=droidcam_mic_index)

    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for a command...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
    except Exception as e:
        print(f"Error: {e}")
        return None
