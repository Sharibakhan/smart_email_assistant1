Perfect bro 😎 tum chahti ho ke **requirements.txt** + **README style setup guide** dono ek jagah ready ho jaye, taaki easily kisi ko bhi share kar sako. Main tumhare given text ko improve karke requirements bhi add kar deta hoon 👇

---

# Smart Email Assistant

A voice-based Python app to record your speech, convert it into text, formalize it using Gemini API, and send an email via Gmail.

---

## ✨ Features

* 🎤 Record voice input
* 📝 Convert speech to text
* 🤖 Formalize casual text into a professional email (using Gemini API)
* 📧 Send email automatically via Gmail
* 🔍 Smart fuzzy matching of recipient names from CSV

---

## ⚙️ Setup Instructions

### 1. Clone or download the project

```bash
git clone <repo-link>
cd smart-email-assistant
```

### 2. Create a `.env` file in the project root and add your credentials:

```
GEMINI_API_KEY=<Your Gemini API Key>
SENDER_EMAIL=<Your Gmail>
GMAIL_APP_PASSWORD=<Your Gmail App Password>
MY_NAME=<Your Name>
```

⚠️ Note:

* Gmail ke liye **App Password** banana hoga (normal Gmail password work nahi karega).
* Agar multiple recipients handle karne hain, to `recipients.csv` file maintain karo:

Example `recipients.csv`:

```
Name,Position,Email
Shariba Khan,Employee,khanshariba667@gmail.com
Sakshi,Team Lead,sakshikhare112002@gmail.com
Afza,Employee,afzamukaddam@gmail.com
Shariba Shaikh,Employee,khansharib598@gmail.com
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt

## ▶️ Run the app

```bash
python app.py
```

Then just **speak the recipient’s name and your message** – the system will formalize it and send the email automatically.
