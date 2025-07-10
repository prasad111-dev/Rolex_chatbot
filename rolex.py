import streamlit as st
import requests
import pyttsx3

# ✅ OpenRouter API key
OPENROUTER_API_KEY = "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"

# 🚀 Ask AI from OpenRouter
def ask_openrouter(question):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are Rolex, a confident, helpful AI assistant built by Prasad."},
            {"role": "user", "content": question}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        result = res.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"API Error: {result['error']['message']}"
        else:
            return "Unexpected API response."
    except Exception as e:
        return f"Error: {str(e)}"

# 🔊 Speak (works only locally)
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    for voice in engine.getProperty('voices'):
        if "male" in voice.name.lower() or "david" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

# 🌐 Streamlit Page Setup
st.set_page_config(page_title="Rolex AI", page_icon="🤖", layout="centered")

# 💄 CSS Styling
st.markdown("""
<style>
    body {
        background: linear-gradient(to bottom right, #0f172a, #1e293b);
        color: #e2e8f0;
    }
    .stApp {
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        color: #38bdf8;
        text-align: center;
        text-shadow: 0 0 10px #0ea5e9;
    }
</style>
""", unsafe_allow_html=True)

# 🧠 Title
st.markdown("<h1>🤖 Rolex - AI Voice Assistant</h1>", unsafe_allow_html=True)

# 📝 Text Input
question = st.text_input("Ask anything:")

if st.button("💬 Get Answer"):
    if question.strip():
        with st.spinner("Rolex is thinking..."):
            answer = ask_openrouter(question)
        st.success(answer)
        try:
            speak(answer)  # NOTE: This only works locally, not on Streamlit Cloud
        except:
            pass

# 📎 Footer
st.markdown("""
<hr>
<p style='text-align:center;color:#64748b;'>⚙️ Built by <strong>Prasad Ghavghave</strong> with ❤️</p>
""", unsafe_allow_html=True)
