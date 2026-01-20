import pyttsx3
import pandas as pd
import webbrowser
import wikipedia
import speech_recognition as sr

# Load Q&A dataset
df = pd.read_csv("Question&Answer.csv")

# Initialize engines
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Website dictionary
websites = {
    "whatsapp": "https://web.whatsapp.com/",
    "youtube": "https://www.youtube.com/",
    "google": "https://www.google.com/",
    "gmail": "https://mail.google.com/",
    "facebook": "https://www.facebook.com/",
    "instagram": "https://www.instagram.com/",
    "chatgpt": "https://chat.openai.com/"
}

print(" Chatbot is ready! Type or speak your question.")
print("Say or type 'exit' to stop.\n")

# Ask user input mode once
mode = input("Choose input method (speak/type): ").strip().lower()

while True:
    if mode == "speak":
        print(" Speak your question...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            ques = recognizer.recognize_google(audio)
            print("You said:", ques)
        except:
            print("Sorry, I couldn't understand. Please type instead.")
            ques = input("Enter your question: ")
    else:
        ques = input("Enter your question: ")

    # Exit condition
    if ques.lower() in ["exit", "quit", "bye", "stop"]:
        print("Goodbye! ")
        engine.say("Goodbye! Have a great day.")
        engine.runAndWait()
        break

    try:
        # If user wants to open a website
        if ques.lower().startswith("open"):
            site = ques.lower().replace("open", "").strip()
            if site in websites:
                webbrowser.open(websites[site])
                print(f"Opening {site}...")
                engine.say(f"Opening {site}")
            else:
                print("Sorry, I don't know that website.")
                engine.say("Sorry, I don't know that website.")

        else:
            # Search in CSV dataset
            df1 = df[df['Question'].str.lower() == ques.lower()]
            
            if df1.empty:
                try:
                    # If not found, fetch from Wikipedia
                    answer = wikipedia.summary(ques, sentences=2)
                    print("From Wikipedia:", answer)
                    engine.say(answer)
                except Exception:
                    print("Sorry, I couldn't find anything on Wikipedia.")
                    engine.say("Sorry, I couldn't find anything on Wikipedia.")
            else:
                # Found in dataset
                answer = df1['Answer'].iloc[0]
                print("From CSV:", answer)
                engine.say(answer)

        engine.runAndWait()

    except Exception as e:
        print("Error:", e)
