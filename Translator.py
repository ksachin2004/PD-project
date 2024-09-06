from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import speech_recognition as sr


language_codes = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de'
}


root = Tk()
root.geometry('1100x620')
root.resizable(0, 0)
root['bg'] = 'skyblue'
root.title('Language translator by GS')

Label(root, text="Language Translator", font="Arial 20 bold").pack()

Label(root, text="Enter Text", font='arial 13 bold', bg='white smoke').place(x=165, y=90)


Input_text = Text(root, width=40, height=20, wrap=WORD , font=('Arial', 12))
Input_text.place(x=60, y=130)


Label(root, text="Output", font='arial 13 bold', bg='white smoke').place(x=780, y=90)

Output_text = Text(root, height=20, wrap=WORD, width=40, font=('Arial', 12))
Output_text.place(x=650, y=130)


language = list(LANGUAGES.values())

dest_lang = ttk.Combobox(root, values=language, width=25, height=10)
dest_lang.place(x=450, y=270)
dest_lang.set('choose language')


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        Input_text.delete(1.0, END)
        Input_text.insert(END, text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


def speak(text):
    try:
        tts = gTTS(text=text, lang=language_codes.get(dest_lang.get().lower(), 'en'), slow=False)


        tts.save("translation.mp3")
        os.system("start translation.mp3")
    except Exception as e:
        Output_text.delete(1.0, END)
        Output_text.insert(END, f"Error in speaking: {str(e)}")


def translate():
    try:
        translator = Translator()
        translated = translator.translate(text=Input_text.get("1.0", "end-1c"), dest=dest_lang.get())
        Output_text.delete(1.0, END)
        Output_text.insert(END, translated.text)
        speak(translated.text)
    except Exception as e:
        Output_text.delete(1.0, END)
        Output_text.insert(END, f"Error: {str(e)}")


trans_btn = Button(root, text='Translate', font='arial 12 bold', pady=5, command=translate, bg='orange', activebackground='white')
trans_btn.place(x=495, y=320)

voice_btn = Button(root, text='Voice Input', font='arial 12 bold', pady=5, command=recognize_speech, bg='yellow', activebackground='grey')
voice_btn.place(x=325, y=455)

root.mainloop()