import streamlit as st
import google.generativeai as genai

# --- KONFIGURATION ---
# 1. Hol dir deinen API Key von Google AI Studio
# 2. Füge ihn unten zwischen die Anführungszeichen ein
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Konfiguriere die AI
genai.configure(api_key=API_KEY)

# Hier setzen wir das Modell und (optional) System-Anweisungen
# Wenn du spezielle Anweisungen aus AI Studio hast, füge sie bei system_instruction ein
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="Du bist ein hilfreicher Assistent für die Aegis AI App."
)

# --- DAS DESIGN DER APP ---
st.title("Aegis AI App 🛡️")
st.write("Willkommen! Wie kann ich dir heute helfen?")

# --- CHAT HISTORIE (Gedächtnis) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Zeige alte Nachrichten an
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- EINGABE & ANTWORT ---
if prompt := st.chat_input("Schreib deine Nachricht..."):
    # 1. Zeige User-Nachricht an
    with st.chat_message("user"):
        st.markdown(prompt)
    # Speichere User-Nachricht ins Gedächtnis
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generiere Antwort
    with st.chat_message("assistant"):
        try:
            # Wir senden den Text an Gemini
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
            # Speichere AI-Antwort ins Gedächtnis
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")