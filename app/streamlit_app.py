import time
import streamlit as st

from database.csv_loader import load_csv
from database.duckdb_manager import DuckDBManager
from database.schema_reader import SchemaReader
from database.sql_validator import SQLValidator
from database.sql_executor import SQLExecutor

from agent.sql_agent import SQLAgent
from agent.answer_agent import AnswerAgent
from agent.question_suggester import QuestionSuggester


# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Data Ledger — CSV Q&A Agent",
    page_icon="📒",
    layout="wide"
)

# -------------------------------
# Design tokens
# -------------------------------
# ink      #0D0F13  background
# charcoal #16191F  surface / card
# rule     #262A31  dividers, borders
# chalk    #EDEAF0  primary text
# fog      #767B85  secondary / muted text
# accent   #F13CFF  neon magenta — the one bright note against the dark neutrals

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap');

:root{
  --ink:#0D0F13;
  --charcoal:#16191F;
  --rule:#262A31;
  --chalk:#EDEAF0;
  --fog:#767B85;
  --accent:#F13CFF;
  --accent-glow:rgba(241,60,255,0.35);
}

.stApp{
  background:var(--ink);
  color:var(--chalk);
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

html, body, [class*="css"]{
  font-family:'IBM Plex Sans', sans-serif;
}

/* ---------- Masthead ---------- */

.eyebrow{
  font-family:'IBM Plex Mono', monospace;
  font-size:12px;
  letter-spacing:.18em;
  text-transform:uppercase;
  color:var(--accent);
  margin-bottom:6px;
}

.masthead-title{
  font-family:'Fraunces', serif;
  font-weight:500;
  font-size:44px;
  color:var(--chalk);
  line-height:1.1;
  margin:0;
}

.masthead-sub{
  font-family:'IBM Plex Mono', monospace;
  font-size:13px;
  color:var(--fog);
  margin-top:10px;
}

.masthead-rule{
  border:none;
  border-top:1px solid var(--rule);
  margin:22px 0 30px 0;
}

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"]{
  background:var(--charcoal);
  border-right:1px solid var(--rule);
}

[data-testid="stSidebar"] .eyebrow{
  margin-top:4px;
}

/* ---------- Ledger stat row (replaces glowing metric cards) ---------- */

.ledger-stat{
  border-top:1px dashed var(--rule);
  padding-top:10px;
  margin-top:10px;
}

.ledger-stat-label{
  font-family:'IBM Plex Mono', monospace;
  font-size:11px;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:var(--fog);
}

.ledger-stat-value{
  font-family:'Fraunces', serif;
  font-size:32px;
  color:var(--chalk);
  margin-top:2px;
}

.ledger-stat-value.is-accent{
  color:var(--accent);
  text-shadow:0 0 18px var(--accent-glow);
}

/* ---------- Inputs ---------- */

.stTextInput input{
  background:var(--charcoal);
  color:var(--chalk);
  border-radius:2px;
  border:1px solid var(--rule);
  font-family:'IBM Plex Mono', monospace;
}

.stTextInput input:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 1px var(--accent), 0 0 14px var(--accent-glow);
}

.stButton>button{
  background:transparent;
  color:var(--accent);
  font-family:'IBM Plex Mono', monospace;
  font-size:14px;
  letter-spacing:.06em;
  text-transform:uppercase;
  border-radius:2px;
  border:1px solid var(--accent);
  height:46px;
  transition:.15s;
}

.stButton>button:hover{
  background:var(--accent);
  color:var(--ink);
  border-color:var(--accent);
  box-shadow:0 0 20px var(--accent-glow);
}

/* ---------- Ledger entry card (the signature element) ---------- */

.entry-card{
  position:relative;
  background:var(--charcoal);
  border:1px solid var(--rule);
  border-top:2px solid var(--accent);
  box-shadow:0 -6px 24px -12px var(--accent-glow);
  padding:24px 28px;
  margin-top:18px;
}

.entry-tag{
  position:absolute;
  top:-11px;
  right:20px;
  background:var(--ink);
  border:1px solid var(--accent);
  color:var(--accent);
  font-family:'IBM Plex Mono', monospace;
  font-size:11px;
  letter-spacing:.1em;
  padding:2px 10px;
  box-shadow:0 0 12px var(--accent-glow);
}

.entry-label{
  font-family:'IBM Plex Mono', monospace;
  font-size:11px;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:var(--fog);
  margin:16px 0 6px 0;
}

.entry-label:first-child{
  margin-top:0;
}

.entry-answer{
  font-family:'IBM Plex Sans', sans-serif;
  font-size:16px;
  color:var(--chalk);
  background:rgba(108,140,255,0.08);
  border-left:2px solid var(--accent);
  padding:10px 14px;
}

.sql-block{
  font-family:'IBM Plex Mono', monospace;
  font-size:13px;
  color:var(--chalk);
  background:var(--ink);
  border:1px solid var(--rule);
  padding:12px 14px;
  white-space:pre-wrap;
}

.sql-block .prompt{
  color:var(--accent);
}

/* Dataframes */
[data-testid="stDataFrame"]{
  border:1px solid var(--rule);
}

/* Muted default streamlit alert boxes, kept but restyled to fit the palette */
.stAlert{
  background:var(--charcoal);
  border:1px solid var(--rule);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------

st.markdown("""
<div class='eyebrow'>CSV LEDGER · QUERY AGENT</div>
<p class='masthead-title'>Ask your data a question.</p>
<div class='masthead-sub'>Every query is planned as SQL, run against the actual rows, and logged as an entry below — nothing here is guessed.</div>
<hr class='masthead-rule'>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.markdown("<div class='eyebrow'>Intake</div>", unsafe_allow_html=True)
st.sidebar.markdown("**Upload dataset**")

uploaded_file = st.sidebar.file_uploader(
    "Choose CSV",
    type=["csv"],
    label_visibility="collapsed"
)

if "entry_count" not in st.session_state:
    st.session_state.entry_count = 0

if uploaded_file is not None:

    df = load_csv(uploaded_file)

    st.sidebar.markdown(f"""
    <div class="ledger-stat">
      <div class="ledger-stat-label">Rows</div>
      <div class="ledger-stat-value is-accent">{len(df):,}</div>
    </div>
    <div class="ledger-stat">
      <div class="ledger-stat-label">Columns</div>
      <div class="ledger-stat-value">{len(df.columns)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<div class='eyebrow' style='margin-top:22px;'>Fields</div>", unsafe_allow_html=True)
    for col in df.columns:
        st.sidebar.markdown(
            f"<div style='font-family:IBM Plex Mono, monospace; font-size:13px; color:var(--fog); padding:3px 0;'>· {col}</div>",
            unsafe_allow_html=True
        )

    # -------------------------------
    # DuckDB
    # -------------------------------

    db = DuckDBManager()
    db.load_dataframe(df)

    connection = db.get_connection()

    schema = SchemaReader(connection).get_schema()

    # -------------------------------
    # Suggested Questions
    # -------------------------------

    try:
        suggester = QuestionSuggester()
        suggestions = suggester.suggest_questions(schema)

        st.sidebar.markdown("<div class='eyebrow' style='margin-top:22px;'>Try asking</div>", unsafe_allow_html=True)
        st.sidebar.markdown(
            f"<div style='font-family:IBM Plex Mono, monospace; font-size:12px; color:var(--fog); line-height:1.6;'>{suggestions}</div>",
            unsafe_allow_html=True
        )
    except Exception:
        pass

    # -------------------------------
    # Dataset preview
    # -------------------------------

    st.markdown("<div class='eyebrow'>Dataset preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    st.markdown("<hr class='masthead-rule'>", unsafe_allow_html=True)

    # -------------------------------
    # Question
    # -------------------------------

    st.markdown("<div class='eyebrow'>New entry</div>", unsafe_allow_html=True)

    col_input, col_btn = st.columns([5, 1])

    with col_input:
        question = st.text_input(
            "Ask a question",
            placeholder="e.g. What is the average order value by region?",
            label_visibility="collapsed"
        )

    with col_btn:
        ask_clicked = st.button("Log query", use_container_width=True)

    if ask_clicked:

        if question.strip() == "":
            st.warning("Enter a question before logging it.")
            st.stop()

        with st.spinner("Planning SQL and running it against the dataset..."):

            start = time.time()

            sql_agent = SQLAgent()
            answer_agent = AnswerAgent()
            executor = SQLExecutor(connection)

            try:
                sql = sql_agent.generate_sql(schema=schema, question=question)

                if sql.strip().upper() == "NOT_POSSIBLE":
                    st.error(
                        "This question can't be answered from the columns in this "
                        "dataset. Try rephrasing it around the fields listed on the left."
                    )
                    st.stop()

                sql = SQLValidator.validate(sql)
                result = executor.execute(sql)
                answer = answer_agent.generate_answer(question=question, sql=sql, result=result)

                elapsed = round((time.time() - start) * 1000, 2)
                st.session_state.entry_count += 1
                entry_no = str(st.session_state.entry_count).zfill(3)

                st.markdown(f"""
                <div class="entry-card">
                  <div class="entry-tag">ENTRY №{entry_no} · {elapsed} ms</div>
                  <div class="entry-label">Question</div>
                  <div>{question}</div>
                  <div class="entry-label">Generated SQL</div>
                  <div class="sql-block"><span class="prompt">&gt;</span> {sql}</div>
                  <div class="entry-label">Answer</div>
                  <div class="entry-answer">{answer}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='entry-label'>Result</div>", unsafe_allow_html=True)
                st.dataframe(result, use_container_width=True)

                csv = result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download result as CSV",
                    csv,
                    "query_result.csv",
                    "text/csv"
                )

            except Exception as e:
                st.error(f"Query failed: {e}")

    db.close()

else:
    st.markdown("""
    <div style='font-family:IBM Plex Mono, monospace; color:var(--fog); font-size:14px; padding:40px 0; border-top:1px dashed var(--rule);'>
    No dataset loaded. Upload a CSV from the sidebar to open a new ledger.
    </div>
    """, unsafe_allow_html=True)