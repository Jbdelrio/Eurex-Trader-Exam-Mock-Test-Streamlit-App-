
#################################################################################################################

import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Eurex Mock Exam", layout="wide")

@st.cache_data
def load_questions():
    df = pd.read_csv("eurex_questions_auto.csv")
    df['id'] = df['id'].astype(int)
    df['is_multiple'] = df['is_multiple'].astype(str).str.lower() == 'true'

    # Classification: MC = multiple, TF = true/false, otherwise SC
    def classify(row):
        if row['is_multiple']:
            return 'MC'
        options = [str(row[c]).strip().lower() for c in ['option_a', 'option_b', 'option_c', 'option_d']]
        if "true" in options and "false" in options:
            return 'TF'
        return 'SC'

    df['type'] = df.apply(classify, axis=1)
    return df.to_dict(orient="records")


# SESSION STATE
if "started" not in st.session_state:
    st.session_state.started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("📘 Eurex Trader Exam – Mock Test")

st.markdown("""
### Scoring Rules:
- ✅ **True/False or Single Choice (TF/SC)** → +2 if correct  
- ✅ **Multiple Choice (MC)**:
     - ⭐ **+4 points if perfect** (all correct selected & none wrong)
     - Otherwise:
         - +1 correct selected  
         - +1 wrong NOT selected  
         - −1 wrong selected  
         - −1 correct NOT selected  
         - Minimum = 0, Maximum = 4  
- 📌 35 questions total (15 Rules & Regs + 20 Functionality)  
- ⏱️ Time limit: **20 minutes**
""")

# START TEST
if not st.session_state.started:
    if st.button("🚀 Start New Test"):
        all_q = load_questions()

        def filt(section, qtype):
            return [q for q in all_q if section[0] <= q['id'] <= section[1] and q['type'] == qtype]

        rules = (1, 45)
        func = (46, 105)

        selected = \
            random.sample(filt(rules, "TF"), 5) + \
            random.sample(filt(rules, "MC"), 4) + \
            random.sample(filt(rules, "SC"), 6) + \
            random.sample(filt(func, "TF"), 4) + \
            random.sample(filt(func, "MC"), 8) + \
            random.sample(filt(func, "SC"), 8)

        random.shuffle(selected)

        st.session_state.questions = selected
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.submitted = False
        st.session_state.answers = {}

        st.rerun()

    st.stop()


# TIMER
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, 20 * 60 - elapsed)
mins, secs = divmod(remaining, 60)

st.markdown(
    f"<h3 style='color:red;'>⏳ Time Remaining: {mins:02}:{secs:02}</h3>",
    unsafe_allow_html=True
)

if remaining == 0 and not st.session_state.submitted:
    st.warning("⏰ Time's up! Submitting answers automatically...")
    st.session_state.submitted = True


# DISPLAY QUESTIONS
user_answers = st.session_state.answers

with st.form("exam_form"):
    for idx, q in enumerate(st.session_state.questions):
        qid = q["id"]
        qtext = q["question"]
        qtype = q["type"]
        correct = q["correct"].split(';') if pd.notna(q["correct"]) else []

        key = f"q_{qid}_{idx}"

        st.markdown(f"**Q{qid}.** {qtext}")

        # Build options A/B/C/D
        options = []
        for letter, col in zip(["A", "B", "C", "D"],
                               ['option_a', 'option_b', 'option_c', 'option_d']):
            val = q[col]
            if pd.notna(val) and str(val).strip():
                options.append(f"{letter}. {val}")

        # MC → checkboxes
        if qtype == "MC":
            selected_opts = []
            for opt in options:
                if st.checkbox(opt, key=f"{key}_{opt}", disabled=st.session_state.submitted):
                    selected_opts.append(opt)
            if not st.session_state.submitted:
                user_answers[key] = selected_opts

        # SC/TF → radio
        else:
            ans = st.radio("Choose one:", options, key=key,
                           index=None if not st.session_state.submitted else 0,
                           disabled=st.session_state.submitted,
                           label_visibility="collapsed")
            if not st.session_state.submitted:
                user_answers[key] = ans

        # AFTER SUBMISSION — correct/incorrect + correct answers
        if st.session_state.submitted:

            # --- scoring correctness indicator ---
            if qtype == "MC":
                selected = user_answers.get(key, [])
                selected_keys = [s[0] for s in selected]

                perfect = (set(selected_keys) == set(correct))
                wrong_selected = any(s not in correct for s in selected_keys)

                if perfect and not wrong_selected:
                    st.success("🟢 Correct")
                else:
                    st.error("🔴 Incorrect")

            else:  # SC / TF
                selected = user_answers.get(key, '')
                selected_letter = selected[0] if selected else ''
                if selected_letter in correct:
                    st.success("🟢 Correct")
                else:
                    st.error("🔴 Incorrect")

            # --- show correct answers ---
            correct_labels = [
                f"{c}. {q[f'option_{c.lower()}']}"
                for c in correct if pd.notna(q.get(f'option_{c.lower()}'))
            ]
            st.info("✅ Correct Answer(s): " + " | ".join(correct_labels))

        st.markdown("---")

    if not st.session_state.submitted:
        if st.form_submit_button("📤 Submit Answers"):
            st.session_state.submitted = True
            st.rerun()


# FINAL SCORING
if st.session_state.submitted:

    score = 0
    total = 0

    st.subheader("🧮 Final Results")

    for idx, q in enumerate(st.session_state.questions):
        qid = q["id"]
        qtype = q["type"]
        correct = q["correct"].split(';') if pd.notna(q["correct"]) else []
        key = f"q_{qid}_{idx}"

        if qtype == "MC":
            selected = user_answers.get(key, [])
            selected_keys = [s[0] for s in selected]

            perfect = (set(selected_keys) == set(correct))
            wrong_selected = any(s not in correct for s in selected_keys)

            if perfect and not wrong_selected:
                question_score = 4
            else:
                good = sum(1 for s in selected_keys if s in correct)
                not_selected = [k for k in ["A", "B", "C", "D"] if k not in selected_keys]
                good += sum(1 for s in not_selected if s not in correct)

                bad = sum(1 for s in selected_keys if s not in correct)
                bad += sum(1 for s in not_selected if s in correct)

                question_score = max(good - bad, 0)

            max_score = 4

        else:  # SC / TF
            selected = user_answers.get(key, '')
            selected_key = selected[0] if selected else ''
            question_score = 2 if selected_key in correct else 0
            max_score = 2

        score += question_score
        total += max_score

        st.markdown(f"**Q{qid}: {question_score} / {max_score} points**")

    st.success(f"🏆 **Final Score: {score} / {total} points**")

    if st.button("🔁 Take Another Test"):
        st.session_state.started = False
        st.rerun()

    st.balloons()
