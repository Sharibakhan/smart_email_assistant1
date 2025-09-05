import os
import pandas as pd
import speech_recognition as sr
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
from dotenv import load_dotenv
import pyttsx3
from rapidfuzz import process

# Load .env variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load recipients
recipients = pd.read_csv("recipients.csv")

# Text-to-Speech setup
engine = pyttsx3.init()
def speak(text):
    print("🔊", text)
    engine.say(text)
    engine.runAndWait()

# Voice Input (to get recipient name) 
def get_voice_input(prompt_text="Speak now, please say the full name."):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt_text)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-IN")
        print("📝 You said:", text)
        return text
    except Exception as e:
        speak("Sorry, I could not understand. Please try again.")
        print("❌ Could not recognize speech:", e)
        return None

# Fuzzy Match Email by Name 
def get_email_by_name(spoken_name):
    names = recipients["Name"].tolist()
    best_match, score, idx = process.extractOne(spoken_name, names)
    if score > 70:  # similarity threshold
        matched_row = recipients.iloc[idx]
        return matched_row["Email"], matched_row["Name"]
    else:
        return None, None

# Gemini: Formalize any casual text 
def formalize_email(casual_text, receiver_name, sender_name):
    prompt = f"""
    You are an AI assistant that converts spoken casual text into a clear and professional email. 
    Do not assume the intent — instead, carefully rewrite the message as the sender intended. 

    - Receiver: {receiver_name}
    - Sender: {sender_name}
    - Casual Message: {casual_text}

    Requirements:
    1. Preserve whether the message is an instruction ("ask them to do something") or an information/update ("I will do something").
    2. Keep the tone polite and professional.
    3. Always include:
       - A suitable subject line
       - Greeting with receiver's name
       - The main message
       - Closing with sender's name
    """
    model = genai.GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content(prompt)
    formal_email = response.text.strip()
    print("📝 Formal Email:", formal_email)
    return formal_email



# Send Email 
def send_email(receiver_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        speak(f"Email sent successfully to {receiver_email}")
        print(f"✅ Email sent successfully to {receiver_email}")
    except Exception as e:
        speak("Email failed to send.")
        print("❌ Email failed:", e)

# MAIN 
def main():
    # Step 1: Get recipient name
    spoken_name = get_voice_input("Speak the recipient's full name.")
    if not spoken_name:
        return

    # Step 2: Match email from CSV
    email, matched_name = get_email_by_name(spoken_name)
    if not email:
        speak("No match found in recipients list.")
        print("❌ No match found in recipients list.")
        return

    speak(f"Matched with {matched_name}")

    # Step 3: Get casual text (what you want to send)
    casual_text = get_voice_input("Speak the message you want to send.")
    if not casual_text:
        return

    # Step 4: Formalize with Gemini (Receiver + Sender)
    sender_name = os.getenv("MY_NAME", "Your Name")
    formal_text = formalize_email(casual_text, matched_name, sender_name)

    # Step 5: Send Email
    send_email(email, f"Message for {matched_name}", formal_text)


if __name__ == "__main__":
    main()

