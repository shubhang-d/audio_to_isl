from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import speech_recognition as sr
import string
from easygui import buttonbox
import string
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/process', methods=['POST'])
def process():
    # text = request.form.get('text', '')
    audio = request.files.get('audio')  # Handle audio input
    audio = 1
    file_path = "recording.wav"
    # audio.save(file_path)
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(0) as source:
            audio = recognizer.record(source)
            transcription = recognizer.recognize_google(audio)
            print(transcription)
            os.remove(file_path)  # Clean up
            if audio:
                return handle_audio_input(transcription)
            else:
                return jsonify({"message": "No input provided"})
            #return jsonify({'transcription': transcription})
    except sr.UnknownValueError:
        os.remove(file_path)
        return jsonify({'error': 'Google Speech Recognition could not understand audio'}), 500
    except sr.RequestError as e:
        os.remove(file_path)
        return jsonify({'error': f'Could not request results from Google Speech Recognition service; {e}'}), 500


def handle_text_input(text):
    result = "Processing complete!"
    # Process text to video/gif here
    video_url = f"static/ISL_Gifs/{text}.mp4"  # Example video path
    return jsonify({"message": result, "video_url": video_url})

def handle_audio_input(transcription):
    # Process audio here using speech_recognition or similar
    recognized_text = transcription
    return handle_text_input(recognized_text)

def play_video(mp4_path, desired_width=640, desired_height=480):
    cap = cv2.VideoCapture(mp4_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame
        frame = cv2.resize(frame, (desired_width, desired_height))
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def display_image_for_text(text, arr):
    """Display images corresponding to each character in the provided text."""
    for char in text:
        if char in arr:
            ImageAddress = f'static/letters/{char}.jpg'
            if os.path.exists(ImageAddress):
                ImageItself = Image.open(ImageAddress)
                ImageNumpyFormat = np.asarray(ImageItself)
                plt.imshow(ImageNumpyFormat)
                plt.draw()
                plt.pause(0.8)
            else:
                print(f"Image for {char} not found.")
        else:
            continue
    plt.close()

def func():
    try:
        import speech_recognition as sr
    except ImportError:
        print("Please install the 'speech_recognition' library using 'pip install SpeechRecognition'")
        return

    r = sr.Recognizer()
    isl_gif = [
        'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
        'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
        'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
        'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
        'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
        'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
        'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
        'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
        'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
        'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
        'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
        'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
        'where is the bathroom','Seventy','sixteen','ten', 'Hundred','nineteen','xylophone', 'xylem', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
        'bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile','dasara',
        'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
        'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
        'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
        'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
        'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
        'voice', 'wednesday', 'xbox','xray' ,'3','100','16', '12' 'weight','please wait for sometime','what is your mobile number','what are you doing','are you busy'
    ]  # Add the full list here
    arr = list(string.ascii_lowercase)

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("I am Listening")
            audio = r.listen(source)
            try:
                a = r.recognize_google(audio).lower()
                print('You Said: ' + a)
                
                for c in string.punctuation:
                    a = a.replace(c, "")
                
                if a in ['goodbye', 'good bye', 'bye']:
                    print("Oops! Time to say goodbye")
                    break
                
                elif a in isl_gif:
                    gif_path = f'static/ISL_Gifs/{a}.gif'
                    mp4_path = f'static/ISL_Gifs/{a}.mp4'
                    
                    if os.path.exists(gif_path):
                        from PIL import ImageTk, Image
                        import tkinter as tk
                        from itertools import count

                        class ImageLabel(tk.Label):
                            """A label that displays images, and plays them if they are gifs"""
                            def load(self, im):
                                if isinstance(im, str):
                                    im = Image.open(im)
                                self.loc = 0
                                self.frames = []

                                try:
                                    for i in count(1):
                                        self.frames.append(ImageTk.PhotoImage(im.copy()))
                                        im.seek(i)
                                except EOFError:
                                    pass

                                try:
                                    self.delay = im.info['duration']
                                except:
                                    self.delay = 100

                                if len(self.frames) == 1:
                                    self.config(image=self.frames[0])
                                else:
                                    self.next_frame()

                            def unload(self):
                                self.config(image=None)
                                self.frames = None

                            def next_frame(self):
                                if self.frames:
                                    self.loc += 1
                                    self.loc %= len(self.frames)
                                    self.config(image=self.frames[self.loc])
                                    self.after(self.delay, self.next_frame)
                        
                        root = tk.Tk()
                        lbl = ImageLabel(root)
                        lbl.pack()
                        lbl.load(gif_path)
                        root.mainloop()
                    
                    elif os.path.exists(mp4_path):
                        play_video(mp4_path)
                    
                else:
                    display_image_for_text(a, arr)
            
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

# while True:
#     image = "static/signlang.png"
#     msg = "HEARING IMPAIRMENT ASSISTANT"
#     choices = ["Live Voice", "All Done!"]
#     reply = buttonbox(msg, image=image, choices=choices)
#     if reply == choices[0]:
#         func()
#     elif reply == choices[1]:
#         break

if __name__ == '__main__':
    app.run()