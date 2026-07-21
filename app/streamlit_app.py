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
    page_title="AI CSV Data Q&A Agent",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Custom CSS
# -------------------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(-45deg,#020617,#081F4D,#001F54,#0F172A);
background-size:400% 400%;
animation:gradient 12s ease infinite;
color:white;
}

@keyframes gradient{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.big-title{
font-size:52px;
font-weight:800;
text-align:center;
color:#38BDF8;
text-shadow:0px 0px 18px #00E5FF;
animation:glow 2s infinite alternate;
}

@keyframes glow{
from{text-shadow:0px 0px 10px #00E5FF;}
to{text-shadow:0px 0px 35px #38BDF8;}
}

.subtitle{
text-align:center;
font-size:18px;
color:#CBD5E1;
margin-bottom:25px;
}

.card{
background:rgba(15,23,42,.88);
padding:18px;
border-radius:16px;
border:1px solid #2563EB;
box-shadow:0px 0px 18px rgba(0,229,255,.18);
}

.card:hover{
transform:translateY(-5px);
transition:.3s;
box-shadow:0px 0px 25px #00E5FF;
}

[data-testid="stSidebar"]{
background:#020617;
}

.stButton>button{
background:linear-gradient(90deg,#2563EB,#00E5FF);
color:white;
font-size:18px;
font-weight:bold;
border-radius:12px;
height:55px;
border:none;
transition:.3s;
}

.stButton>button:hover{
transform:scale(1.03);
box-shadow:0px 0px 20px #00E5FF;
}

.stTextInput input{
background:#0F172A;
color:white;
border-radius:10px;
border:1px solid #38BDF8;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------

st.markdown("""
<div class='big-title'>
🤖 AI CSV Data Q&A Agent
</div>

<div class='subtitle'>
⚡ Ask questions about any CSV using <b>Groq LLM</b> + <b>DuckDB</b>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.title("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = load_csv(uploaded_file)

    st.sidebar.success("Dataset Loaded")

    st.sidebar.metric("Rows", len(df))
    st.sidebar.metric("Columns", len(df.columns))

    st.sidebar.markdown("---")
    st.sidebar.subheader("📑 Columns")

    for col in df.columns:
        st.sidebar.write("•", col)

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

        st.sidebar.markdown("---")
        st.sidebar.subheader("💡 Suggested Questions")
        st.sidebar.markdown(suggestions)

    except:
        pass

    # -------------------------------
    # Dashboard
    # -------------------------------

    st.subheader("📊 Dataset Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="card">
        <h3>📄 Rows</h3>
        <h1>{len(df):,}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
        <h3>📑 Columns</h3>
        <h1>{len(df.columns)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h3>🧠 AI Status</h3>
        <h1>READY</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📋 Dataset Preview")

    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")

    question = st.text_input(
        "📝 Ask a Question"
    )

    if st.button("🚀 Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("🤖 Thinking... Generating SQL..."):

            start = time.time()

            sql_agent = SQLAgent()
            answer_agent = AnswerAgent()
            executor = SQLExecutor(connection)

            try:

                sql = sql_agent.generate_sql(
                    schema=schema,
                    question=question
                )

                sql = SQLValidator.validate(sql)

                result = executor.execute(sql)

                answer = answer_agent.generate_answer(
                    question=question,
                    sql=sql,
                    result=result
                )

                elapsed = round(
                    (time.time() - start) * 1000,
                    2
                )

                st.success("✅ Answer Generated Successfully")

                st.balloons()

                st.markdown("## 💻 Generated SQL")

                st.code(sql, language="sql")

                st.markdown("## 📊 Query Result")

                st.dataframe(result, use_container_width=True)

                st.markdown("## 💡 Final Answer")

                st.success(answer)

                st.info(f"⚡ Execution Time : {elapsed} ms")

                csv = result.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "⬇ Download Result",
                    csv,
                    "query_result.csv",
                    "text/csv"
                )

            except Exception as e:
                st.error(f"❌ {e}")

    db.close()

else:

    st.info("⬅ Upload a CSV file from the sidebar to begin.")