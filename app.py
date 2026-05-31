import streamlit as st

# --- INITIALIZATION ---
if 'career' not in st.session_state:
    st.session_state.update({
        'day': 1,
        'name': 'Alex Vance',
        'level': 'Helpdesk Intern',
        'reputation': 100,
        'competence': 0,
        'confidence': 50,
        'terminated': False
    })

# --- SIDEBAR METRICS ---
st.sidebar.subheader(f"Profile: {st.session_state.name}")
st.sidebar.write(f"Role: {st.session_state.level}")
st.sidebar.progress(st.session_state.competence / 100, text="Competence")
st.sidebar.progress(st.session_state.confidence / 100, text="Team Confidence")
st.sidebar.write(f"Reputation: {st.session_state.reputation}")

# --- GAME LOGIC ---
st.title("🛡️ IT Master Simulator")

if st.session_state.terminated:
    st.error("Career Over: You were terminated for poor performance.")
    if st.button("Restart Career"):
        st.session_state.clear()
        st.rerun()
else:
    st.subheader(f"Day {st.session_state.day}: The Helpdesk")
    st.write("A user reports: 'My screen is black and I have a deadline!'")
    
    response = st.text_input("What do you do?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Response"):
            # Mock logic: checking for 'power' or 'cable'
            if "power" in response.lower() or "cable" in response.lower():
                st.success("Correct! User is back online.")
                st.session_state.competence += 10
                st.session_state.day += 1
                st.rerun()
            else:
                st.session_state.reputation -= 20
                st.warning("Incorrect. Reputation lost!")
    
    with col2:
        if st.button("Call Supervisor (Cost: 20 Rep)"):
            if st.session_state.reputation >= 20:
                st.session_state.reputation -= 20
                st.info("Supervisor: 'Check the power cable first.'")
            else:
                st.error("Too risky to call!")

    if st.session_state.reputation <= 0:
        st.session_state.terminated = True
        st.rerun()
