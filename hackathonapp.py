import streamlit as st
import random
import time

st.set_page_config(
    page_title="LearnMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Demo data ----------
BANK = {
    "Demand": {
        "Easy": [
            ("As price increases, demand usually:",
             ["Increases", "Decreases", "Stays the same", "Doubles"], 1),
            ("The demand curve generally slopes:",
             ["Upward", "Downward", "Vertically only", "Horizontally only"], 1),
        ],
        "Medium": [
            ("The Law of Demand assumes which factor is constant?",
             ["Income", "Ceteris paribus (other things equal)", "Supply", "Inflation"], 1),
            ("A movement along a demand curve is mainly caused by a change in:",
             ["The good's own price", "Population", "Technology", "Taste"], 0),
        ],
        "Hard": [
            ("A leftward shift of the demand curve is most likely caused by:",
             ["A fall in the price of the good",
              "A decrease in consumer income (normal good)",
              "An increase in advertising",
              "A fall in production cost"], 1),
            ("For a normal good, an increase in consumer income usually:",
             ["Decreases demand", "Increases demand", "Has no effect", "Makes supply zero"], 1),
        ],
    },
    "Supply": {
        "Easy": [
            ("As price increases, supply usually:",
             ["Decreases", "Increases", "Stays the same", "Becomes zero"], 1),
            ("The supply curve generally slopes:",
             ["Downward", "Upward", "Both always", "Not at all"], 1),
        ],
        "Medium": [
            ("Which of these shifts the supply curve to the right?",
             ["Higher input costs", "New technology lowering production cost",
              "Higher taxes on producers", "Fewer sellers"], 1),
            ("A rise in production costs usually causes supply to:",
             ["Increase", "Decrease", "Stay fixed", "Double"], 1),
        ],
        "Hard": [
            ("Supply is perfectly inelastic when:",
             ["Any price change causes infinite quantity change",
              "Quantity supplied doesn't change regardless of price",
              "Price and quantity move proportionally", "Supply curve is horizontal"], 1),
            ("A technological improvement that lowers production costs generally:",
             ["Shifts supply left", "Shifts supply right",
              "Reduces demand", "Makes price irrelevant"], 1),
        ],
    },
    "Elasticity": {
        "Easy": [
            ("Price elasticity of demand measures responsiveness of:",
             ["Supply to price", "Quantity demanded to price change",
              "Income to price", "Cost to output"], 1),
            ("Elasticity measures how responsive one variable is to:",
             ["Another variable", "Nothing", "Only income", "Only supply"], 0),
        ],
        "Medium": [
            ("If elasticity > 1, demand is called:",
             ["Inelastic", "Elastic", "Unitary elastic", "Perfectly inelastic"], 1),
            ("If elasticity is less than 1, demand is generally:",
             ["Elastic", "Inelastic", "Unitary", "Infinite"], 1),
        ],
        "Hard": [
            ("A good with very few substitutes typically has:",
             ["High elasticity of demand", "Low (inelastic) demand",
              "Zero elasticity", "Undefined elasticity"], 1),
            ("Demand tends to be more elastic when consumers have:",
             ["Fewer substitutes", "More substitutes", "No choices", "Fixed income only"], 1),
        ],
    },
    "Break-even Analysis": {
        "Easy": [
            ("Break-even point is where:",
             ["Profit is maximum", "Total revenue equals total cost",
              "Fixed cost is zero", "Variable cost is zero"], 1),
            ("At break-even, the business makes:",
             ["A maximum profit", "No profit and no loss",
              "Only fixed costs", "Only variable costs"], 1),
        ],
        "Medium": [
            ("Break-even quantity = Fixed Cost ÷ ?",
             ["Total Cost", "Contribution margin per unit",
              "Variable Cost", "Selling Price"], 1),
            ("Contribution per unit is selling price minus:",
             ["Fixed cost", "Variable cost", "Total revenue", "Profit"], 1),
        ],
        "Hard": [
            ("If fixed costs rise while contribution margin stays the same, break-even point:",
             ["Falls", "Rises", "Stays the same", "Becomes negative"], 1),
            ("If contribution margin increases while fixed costs remain unchanged, break-even quantity:",
             ["Rises", "Falls", "Always doubles", "Cannot change"], 1),
        ],
    },
}

TOPICS = list(BANK)
LEVELS = ["Easy", "Medium", "Hard"]

# ---------- Styling ----------
st.markdown("""
<style>
.main {background:#f8fafc;}
.block-container {padding-top:1.8rem; max-width:1250px;}
.hero {
  padding:34px; border-radius:28px; margin-bottom:24px;
  background:linear-gradient(135deg,#eef2ff 0%,#f5f3ff 55%,#ecfeff 100%);
  border:1px solid #e5e7eb;
}
.hero h1 {font-size:42px; margin:5px 0 8px; font-weight:800;}
.hero p {font-size:18px; color:#475569; margin:0;}
.card {
  padding:22px; border:1px solid #e5e7eb; border-radius:20px;
  background:white; min-height:150px; box-shadow:0 4px 16px rgba(15,23,42,.04);
}
.small {color:#64748b; font-size:14px;}
.pill {display:inline-block;padding:6px 12px;border-radius:999px;
       background:#e0e7ff;color:#3730a3;font-size:12px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
defaults = {
    "page": "Dashboard",
    "logged_in": False,
    "student": "",
    "scores": {t: [] for t in TOPICS},
    "difficulty": {t: "Medium" for t in TOPICS},
    "questions": [],
    "q_index": 0,
    "correct": 0,
    "selected": None,
    "feedback": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- Login ----------
if not st.session_state.logged_in:
    left, center, right = st.columns([1, 1.4, 1])
    with center:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center">
          <div style="font-size:58px">🎓</div>
          <h1>LearnMate AI</h1>
          <p style="color:#64748b">Personalized learning for smarter studying.</p>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Student name", placeholder="Enter your name")
        if st.button("Enter LearnMate →", type="primary", use_container_width=True):
            if name.strip():
                st.session_state.student = name.strip()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please enter your name.")
    st.stop()

# ---------- Helpers ----------
def start_quiz(topic, level):
    pool = BANK[topic][level]
    questions = random.sample(pool, k=min(5, len(pool)))
    if len(questions) < 5:
        questions = (questions * 3)[:5]
    random.shuffle(questions)
    st.session_state.questions = questions
    st.session_state.q_index = 0
    st.session_state.correct = 0
    st.session_state.selected = None
    st.session_state.feedback = None
    st.session_state.quiz_topic = topic
    st.session_state.quiz_level = level
    st.session_state.page = "Quiz"

def next_level(level, ratio):
    i = LEVELS.index(level)
    if ratio >= .8:
        return LEVELS[min(i + 1, 2)]
    if ratio < .5:
        return LEVELS[max(i - 1, 0)]
    return level

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🎓 LearnMate AI")
    st.caption(f"Welcome, **{st.session_state.student}**")
    st.divider()

    for p, icon in [
        ("Dashboard", "🏠"), ("Study Material", "📚"),
        ("Quiz", "📝"), ("Performance", "📊")
    ]:
        if st.button(f"{icon}  {p}", use_container_width=True):
            st.session_state.page = p
            st.rerun()

    st.divider()
    st.markdown("### Your learning mode")
    st.success("Adaptive learning ON")
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ---------- Dashboard ----------
if st.session_state.page == "Dashboard":
    st.markdown("""
    <div class="hero">
      <span class="pill">AI-ENABLED PERSONALIZED LEARNING</span>
      <h1>Learn at your pace. 🚀</h1>
      <p>Study, test your knowledge, and improve smarter with personalized practice.</p>
    </div>
    """, unsafe_allow_html=True)

    attempts = sum(len(x) for x in st.session_state.scores.values())
    vals = [v for scores in st.session_state.scores.values() for v in scores]
    avg = sum(vals) / len(vals) * 100 if vals else 0
    weak = [t for t, scores in st.session_state.scores.items()
            if scores and sum(scores)/len(scores) < .6]

    a, b, c, d = st.columns(4)
    a.metric("Quiz Attempts", attempts)
    b.metric("Average Score", f"{avg:.0f}%")
    c.metric("Topics", len(TOPICS))
    d.metric("Weak Areas", len(weak))

    st.markdown("### ⚡ Quick Start")
    cols = st.columns(4)
    for col, topic in zip(cols, TOPICS):
        with col:
            st.markdown(
                f'<div class="card"><h3>{topic}</h3>'
                f'<p class="small">Recommended: <b>{st.session_state.difficulty[topic]}</b></p></div>',
                unsafe_allow_html=True)
            if st.button(f"Practice {topic}", key=f"start_{topic}", use_container_width=True):
                start_quiz(topic, st.session_state.difficulty[topic])
                st.rerun()

    st.markdown("### 💡 Personalized Recommendation")
    if weak:
        st.warning("Focus your revision on: " + ", ".join(weak))
    else:
        st.info("Take your first quiz and LearnMate will identify where you should focus.")

# ---------- Study Material ----------
elif st.session_state.page == "Study Material":
    st.title("📚 Study Material")
    st.write("Upload a text-based PDF to extract its content and create a quick study summary.")

    uploaded = st.file_uploader("Drop your PDF here", type=["pdf"])
    if uploaded:
        st.success(f"Ready: {uploaded.name}")
        if st.button("✨ Generate Study Summary", type="primary"):
            try:
                from pypdf import PdfReader
                reader = PdfReader(uploaded)
                text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
                if not text:
                    st.warning("No text was extracted. A scanned/image-only PDF may need OCR.")
                else:
                    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
                    summary = ". ".join(sentences[:7]) + ("." if sentences else "")
                    st.subheader("🤖 LearnMate Summary")
                    st.write(summary)
                    st.info("Demo mode: the current summary is extractive. A live LLM can replace this step later.")
            except Exception as e:
                st.error(f"Could not read the PDF: {e}")

# ---------- Quiz ----------
elif st.session_state.page == "Quiz":
    st.title("📝 Personalized Quiz")

    if not st.session_state.questions:
        topic = st.selectbox("Choose topic", TOPICS)
        level = st.selectbox(
            "Difficulty",
            LEVELS,
            index=LEVELS.index(st.session_state.difficulty[topic])
        )
        st.caption("LearnMate recommends difficulty from your previous performance.")
        if st.button("🚀 Start Quiz", type="primary"):
            start_quiz(topic, level)
            st.rerun()
    else:
        qs = st.session_state.questions
        i = st.session_state.q_index
        topic = st.session_state.quiz_topic
        level = st.session_state.quiz_level

        st.progress((i) / len(qs), text=f"Question {i+1} of {len(qs)} • {topic} • {level}")
        question, options, correct = qs[i]

        st.markdown(f"### {question}")
        answer = st.radio(
            "Select one answer:",
            options,
            key=f"answer_{i}",
            disabled=st.session_state.feedback is not None
        )

        if st.session_state.feedback is None:
            if st.button("Check Answer", type="primary"):
                st.session_state.selected = options.index(answer)
                if st.session_state.selected == correct:
                    st.session_state.correct += 1
                    st.session_state.feedback = ("correct", options[correct])
                else:
                    st.session_state.feedback = ("wrong", options[correct])
                st.rerun()
        else:
            kind, correct_answer = st.session_state.feedback
            if kind == "correct":
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Not quite. Correct answer: **{correct_answer}**")

            if i + 1 < len(qs):
                if st.button("Next Question →", type="primary"):
                    st.session_state.q_index += 1
                    st.session_state.feedback = None
                    st.session_state.selected = None
                    st.rerun()
            else:
                ratio = st.session_state.correct / len(qs)
                old = level
                new = next_level(old, ratio)
                st.session_state.scores[topic].append(ratio)
                st.session_state.difficulty[topic] = new
                st.session_state.questions = []
                st.session_state.feedback = None

                st.balloons()
                st.markdown("---")
                st.subheader("🎉 Quiz Complete!")
                st.metric("Your Score", f"{st.session_state.correct}/{len(qs)}")
                st.write(f"Percentage: **{ratio*100:.0f}%**")
                if new != old:
                    st.info(f"Adaptive Engine: **{old} → {new}**")
                else:
                    st.caption(f"Next recommended level: {new}")

                if st.button("📊 View Performance", type="primary"):
                    st.session_state.page = "Performance"
                    st.rerun()

# ---------- Performance ----------
elif st.session_state.page == "Performance":
    st.title("📊 Performance Dashboard")

    any_score = False
    for topic in TOPICS:
        scores = st.session_state.scores[topic]
        if scores:
            any_score = True
            avg = sum(scores)/len(scores)*100
            st.markdown(f"### {topic}")
            st.progress(min(avg/100, 1), text=f"{avg:.0f}% average • {len(scores)} attempt(s)")
            st.caption(f"Recommended difficulty: {st.session_state.difficulty[topic]}")

    if not any_score:
        st.info("No quiz attempts yet. Complete a quiz to build your dashboard.")
    else:
        weak = [
            t for t, scores in st.session_state.scores.items()
            if scores and sum(scores)/len(scores) < .6
        ]
        if weak:
            st.warning("💡 AI Recommendation: revise " + ", ".join(weak))
        else:
            st.success("🌟 Strong performance across all attempted topics!")

st.divider()
st.caption("LearnMate AI • Hackathon MVP • Python + Streamlit")
