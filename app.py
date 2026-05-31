import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="IT Master Simulator", page_icon="🛡️")

# --- AI SETUP ---
# Ensure you add GEMINI_API_KEY to your Streamlit Cloud "Secrets"
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- INITIALIZATION ---
if 'career' not in st.session_state:
    st.session_state.career = {
        'level': 'Helpdesk Intern', 'reputation': 100, 
        'competence': 0, 'confidence': 50, 'day': 1
    }
    st.session_state.messages = [
        {"role": "system", "content": """
        You are a blunt, Senior IT Mentor. Student is Alex Vance.
        Your goal: Triage training. 
        Rules:
        1. Always pose IT problems (Printer jams, DNS issues, escalated security threats).
        2. If Alex is wrong, penalize reputation.
        3. If Alex is right, boost competence.
        4. Stay conversational. Use real IT jargon.
        5. Every 5 interactions, evaluate if Alex deserves a promotion.
        """}
    ]

# --- SIDEBAR UI ---
st.sidebar.title(f"🛡️ {st.session_state.career['level']}")
st.sidebar.progress(st.session_state.career['competence'] / 100, text="Competence")
st.sidebar.progress(st.session_state.career['confidence'] / 100, text="Team Confidence")
st.sidebar.metric("Reputation", st.session_state.career['reputation'])

# --- MAIN CHAT UI ---
st.title("IT Master Simulator")

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("Triage response..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.spinner("Analyzing your triage..."):
        response = model.generate_content(str(st.session_state.messages))
        ai_reply = response.text
        
        # Simple Logic to adjust stats based on AI's output
        # In a production app, you'd use structured data (JSON) here
        st.session_state.career['competence'] += 2
        st.session_state.career['day'] += 1
        
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.write(ai_reply)
            st.rerun()
