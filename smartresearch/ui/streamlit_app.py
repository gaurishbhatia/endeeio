"""
Streamlit web UI for SmartResearch.
Run with:  python -m streamlit run ui/streamlit_app.py
"""
import sys
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartResearch — AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium Aesthetic — Art-Deco meets Cyberpunk ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Source+Code+Pro:wght@300;400;600&family=DM+Sans:wght@300;400;500;700&display=swap');

/* ─── Reset & Root ─────────────────────────────────────── */
:root {
    --bg-primary: #0a0a12;
    --bg-secondary: #111120;
    --bg-glass: rgba(17, 17, 32, 0.7);
    --accent-gold: #d4a853;
    --accent-gold-light: #f0d48a;
    --accent-emerald: #34d399;
    --accent-rose: #fb7185;
    --accent-blue: #60a5fa;
    --text-primary: #e8e6df;
    --text-muted: #7c7a73;
    --border-subtle: rgba(212, 168, 83, 0.15);
    --border-glow: rgba(212, 168, 83, 0.4);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ─── Background ───────────────────────────────────────── */
.stApp {
    background: var(--bg-primary);
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(212, 168, 83, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(52, 211, 153, 0.04) 0%, transparent 50%),
        linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    min-height: 100vh;
}

/* ─── Sidebar ──────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d18 0%, #0a0a14 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Playfair Display', serif;
    color: var(--accent-gold);
    font-weight: 700;
    letter-spacing: 0.5px;
    font-size: 1.25rem;
}
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'DM Sans', sans-serif;
    color: var(--accent-gold-light);
    font-weight: 500;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ─── Hero Header ──────────────────────────────────────── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 180px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    color: var(--accent-gold);
    letter-spacing: 1px;
    margin: 0;
    line-height: 1.1;
    text-shadow: 0 0 60px rgba(212, 168, 83, 0.15);
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 300;
    margin-top: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.hero-subtitle strong {
    color: var(--accent-emerald);
    font-weight: 500;
}

/* ─── Metric Pillars ───────────────────────────────────── */
.metric-pillar {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 1.2rem 1rem;
    text-align: center;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}
.metric-pillar:hover {
    border-color: var(--border-glow);
}
.metric-pillar::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
    opacity: 0.4;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
}
.metric-label {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-muted);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-top: 0.4rem;
}

/* ─── Answer Card ──────────────────────────────────────── */
.answer-card {
    background: linear-gradient(135deg, rgba(212, 168, 83, 0.04), rgba(17, 17, 32, 0.8));
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-gold);
    border-radius: 4px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    backdrop-filter: blur(8px);
}

/* ─── Source Chips ──────────────────────────────────────── */
.source-chip {
    display: inline-block;
    background: rgba(212, 168, 83, 0.08);
    border: 1px solid rgba(212, 168, 83, 0.25);
    color: var(--accent-gold-light);
    border-radius: 3px;
    padding: 4px 14px;
    font-size: 0.78rem;
    margin: 3px;
    font-family: 'Source Code Pro', monospace;
    letter-spacing: 0.5px;
    transition: background 0.2s;
}
.source-chip:hover {
    background: rgba(212, 168, 83, 0.15);
}

/* ─── Chat Messages ────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    backdrop-filter: blur(8px) !important;
}

/* ─── Input ────────────────────────────────────────────── */
.stChatInput textarea,
.stTextArea textarea,
.stTextInput input {
    background: rgba(10, 10, 18, 0.9) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 4px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stChatInput textarea:focus,
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 1px rgba(212, 168, 83, 0.2) !important;
}

/* ─── Buttons ──────────────────────────────────────────── */
.stButton>button {
    background: linear-gradient(135deg, var(--accent-gold) 0%, #c49a3c 100%) !important;
    color: #0a0a12 !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    transition: all 0.25s ease !important;
}
.stButton>button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(212, 168, 83, 0.3) !important;
}

/* ─── Expanders ────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.85rem !important;
    color: var(--accent-gold-light) !important;
}

/* ─── Divider ──────────────────────────────────────────── */
hr {
    border-color: var(--border-subtle) !important;
}

/* ─── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(212, 168, 83, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(212, 168, 83, 0.5); }

/* ─── Animations ───────────────────────────────────────── */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero-wrap, .metric-pillar {
    animation: fadeSlideIn 0.6s ease-out both;
}
.metric-pillar:nth-child(2) { animation-delay: 0.1s; }
.metric-pillar:nth-child(3) { animation-delay: 0.2s; }
</style>
""", unsafe_allow_html=True)


# ── Lazy load pipeline ────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading SmartResearch engine...")
def load_pipeline():
    from app.rag_pipeline import RAGPipeline
    return RAGPipeline()


# ── Session state defaults ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ingested_sources" not in st.session_state:
    st.session_state.ingested_sources = []


# ── Sidebar — Document Ingestion ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ◈ Document Vault")
    st.markdown(
        '<p style="color:#7c7a73; font-size:0.85rem; margin-top:-0.5rem;">'
        'Feed documents into the knowledge base.</p>',
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    url_input = st.text_input(
        "Or enter a web URL",
        placeholder="https://arxiv.org/abs/...",
    )

    ingest_btn = st.button("⚡ INGEST", use_container_width=True)

    if ingest_btn:
        pipeline = load_pipeline()
        sources_to_ingest = []

        for uf in (uploaded_files or []):
            suffix = Path(uf.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uf.read())
                sources_to_ingest.append((tmp.name, uf.name))

        if url_input.strip():
            sources_to_ingest.append((url_input.strip(), url_input.strip()))

        if not sources_to_ingest:
            st.warning("Upload a file or enter a URL first.")
        else:
            for src_path, display_name in sources_to_ingest:
                with st.spinner(f"Ingesting {display_name}..."):
                    try:
                        count = pipeline.ingest(src_path)
                        st.success(f"✓ {display_name} → {count} chunks")
                        if display_name not in st.session_state.ingested_sources:
                            st.session_state.ingested_sources.append(display_name)
                    except Exception as e:
                        st.error(f"Failed: {e}")

    st.divider()
    st.markdown("### Indexed Sources")
    if st.session_state.ingested_sources:
        for src in st.session_state.ingested_sources:
            label = Path(src).name if "/" not in src and "\\" not in src else src
            st.markdown(
                f'<span class="source-chip">▸ {label}</span>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No documents ingested yet.")

    st.divider()
    st.markdown("### Retrieval")
    top_k = st.slider("Chunks to retrieve (top-k)", 1, 10, 5)

    st.divider()
    st.markdown(
        '<p style="color:#3d3d4a; font-size:0.7rem; text-align:center; letter-spacing:2px;">'
        'POWERED BY ENDEE × GEMINI</p>',
        unsafe_allow_html=True,
    )


# ── Main area — Hero ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">SmartResearch</div>
    <div class="hero-subtitle">Semantic retrieval powered by <strong>Endee</strong> · Answers by Gemini</div>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ───────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-pillar">
        <div class="metric-value" style="color: var(--accent-gold);">{len(st.session_state.ingested_sources)}</div>
        <div class="metric-label">Sources Indexed</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-pillar">
        <div class="metric-value" style="color: var(--accent-emerald);">{len(st.session_state.messages) // 2}</div>
        <div class="metric-label">Questions Asked</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-pillar">
        <div class="metric-value" style="color: var(--accent-rose);">Endee</div>
        <div class="metric-label">Vector Database</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("⊞  Sources from Endee"):
                for i, chunk in enumerate(msg["sources"], 1):
                    sim = chunk['similarity']
                    st.markdown(
                        f"**Chunk {i}** · "
                        f"`{chunk['source']}` · Page {chunk['page']} · "
                        f"Similarity: `{sim:.4f}`\n\n"
                        f"> {chunk['text'][:300]}..."
                    )

# ── Chat input ────────────────────────────────────────────────────────────────
question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Searching Endee & generating answer..."):
            pipeline = load_pipeline()
            try:
                answer, chunks = pipeline.ask(question, top_k=top_k)
            except EnvironmentError as e:
                answer = f"⚠️ **Configuration Error:** {e}"
                chunks = []
            except Exception as e:
                answer = f"⚠️ **Error:** {e}"
                chunks = []

        st.markdown(answer)

        if chunks:
            with st.expander("⊞  Sources from Endee"):
                for i, chunk in enumerate(chunks, 1):
                    sim = chunk['similarity']
                    st.markdown(
                        f"**Chunk {i}** · "
                        f"`{chunk['source']}` · Page {chunk['page']} · "
                        f"Similarity: `{sim:.4f}`\n\n"
                        f"> {chunk['text'][:300]}..."
                    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": chunks,
    })
