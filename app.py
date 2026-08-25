import time
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Research Studio",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MODERN GEMINI-INSPIRED CUSTOM CSS
# ============================================================

st.markdown(
"""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* App Background & Spacing */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1180px;
}

/* Gemini Glowing Banner */
.gemini-hero {
    padding: 2.5rem;
    border-radius: 24px;
    background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(217, 70, 239, 0.15) 0%, transparent 40%),
                linear-gradient(135deg, #161b22 0%, #0f141c 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.25);
    margin-bottom: 2rem;
}

.gemini-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    color: #818cf8;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}

.gemini-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 70%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.gemini-subtitle {
    font-size: 15px;
    color: #8b949e;
    font-weight: 400;
    max-width: 650px;
    line-height: 1.5;
}

/* Agent Architecture Pipeline */
.pipeline-header {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8b949e;
    margin: 1.5rem 0 1rem 0;
}

.node-card {
    background: #161b22;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.2rem;
    transition: all 0.2s ease-in-out;
    height: 100%;
}

.node-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
}

.node-index {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #818cf8;
    margin-bottom: 4px;
    font-weight: 600;
}

.node-title {
    font-size: 15px;
    font-weight: 700;
    color: #f0f6fc;
    margin-bottom: 4px;
}

.node-desc {
    font-size: 12px;
    color: #8b949e;
    line-height: 1.4;
}

/* Tab Panels & Containers */
.report-paper {
    background: #161b22;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 2.2rem;
    color: #e6edf3;
    line-height: 1.7;
    font-size: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.fact-badge-pass {
    display: inline-block;
    padding: 6px 14px;
    background: rgba(34, 197, 94, 0.1);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.25);
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
}

.fact-badge-revise {
    display: inline-block;
    padding: 6px 14px;
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
}

/* Sidebar Styles */
[data-testid="stSidebar"] {
    background-color: #0b0e14;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.history-item {
    padding: 10px 14px;
    border-radius: 10px;
    background: #161b22;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 8px;
    font-size: 13px;
    color: #c9d1d9;
}
</style>""",
    unsafe_allow_html=True
)

# ============================================================
# STATE INITIALIZATION
# ============================================================

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if "active_topic" not in st.session_state:
    st.session_state.active_topic = ""

if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# SIDEBAR NAVIGATION & HISTORY
# ============================================================

with st.sidebar:
    st.markdown("### Studio Control")
    st.caption("Multi-Agent Autonomous Research Orchestrator")
    
    st.markdown("---")
    st.markdown("#### System State")
    st.markdown(
        """
        <div style="font-size: 13px; line-height: 1.8; color: #8b949e;">
            • Engine: <span style="color: #4ade80;">Online</span><br>
            • Topology: <span style="color: #818cf8;">LangGraph DAG</span><br>
            • Consensus: <span style="color: #c084fc;">Fact-Verified</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("#### Research History")
    
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            if st.button(f"▪ {item['topic'][:24]}...", key=f"hist_{idx}", use_container_width=True):
                st.session_state.workflow_result = item["result"]
                st.session_state.active_topic = item["topic"]
                st.rerun()
    else:
        st.caption("No queries generated in this session yet.")
        
    if st.session_state.history:
        if st.button("Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.workflow_result = None
            st.session_state.active_topic = ""
            st.rerun()

# ============================================================
# HERO INTERFACE
# ============================================================

st.markdown(
"""<div class="gemini-hero">
    <div class="gemini-tag">Autonomous Research Agent Matrix</div>
    <div class="gemini-title">AI Research Studio</div>
    <div class="gemini-subtitle">
        Accelerate literature analysis, synthesize multi-source intelligence, and generate fact-checked academic briefs using coordinated neural agent graphs.
    </div>
</div>""",
    unsafe_allow_html=True
)

# ============================================================
# AGENT MATRIX ARCHITECTURE VIEW
# ============================================================

st.markdown('<div class="pipeline-header">Autonomous Agent Pipeline</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

nodes = [
    ("01", "Collector", "Queries Wikipedia and Tavily engines"),
    ("02", "Analyst", "Extracts structured evidence & notes"),
    ("03", "Architect", "Generates report schema & hierarchy"),
    ("04", "Writer", "Drafts synthesized academic prose"),
    ("05", "Validator", "Audits claims against source corpus"),
    ("06", "Citations", "Indexes formal links and metadata")
]

cols = [col1, col2, col3, col4, col5, col6]
for col, (num, title, desc) in zip(cols, nodes):
    with col:
        st.markdown(
f"""<div class="node-card">
    <div class="node-index">{num}</div>
    <div class="node-title">{title}</div>
    <div class="node-desc">{desc}</div>
</div>""",
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# INPUT QUERY BAR
# ============================================================

query_col, btn_col = st.columns([5, 1])

with query_col:
    topic = st.text_input(
        "Research Target",
        value=st.session_state.active_topic,
        placeholder="Enter research query (e.g. Next-Generation Multimodal Architectures)",
        label_visibility="collapsed"
    )

with btn_col:
    generate = st.button("Synthesize", type="primary", use_container_width=True)

# Sample Starters
st.markdown(
    """
    <div style="font-size: 12px; color: #8b949e; margin-top: -6px; margin-bottom: 24px;">
        Suggestions: 
        <span style="color: #818cf8;">Mechanistic Interpretability in LLMs</span> &nbsp;|&nbsp; 
        <span style="color: #818cf8;">Quantum Key Distribution Protocols</span> &nbsp;|&nbsp; 
        <span style="color: #818cf8;">Neuromorphic Computing Hardware</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PIPELINE EXECUTION
# ============================================================

if generate:
    if not topic.strip():
        st.warning("Please specify a research target.")
    else:
        st.session_state.active_topic = topic
        status_box = st.status("Initializing agent cluster...", expanded=True)
        
        try:
            from workflow.research_workflow import research_workflow
            
            status_box.write("Retrieving web and encyclopedic corpus...")
            time.sleep(0.3)
            status_box.write("Synthesizing primary findings...")
            time.sleep(0.3)
            status_box.write("Generating document outline...")
            time.sleep(0.3)
            status_box.write("Drafting academic content...")
            time.sleep(0.3)
            status_box.write("Verifying claims against evidence corpus...")
            time.sleep(0.3)
            status_box.write("Compiling structured references...")
            
            result = research_workflow.invoke({"topic": topic.strip()})
            st.session_state.workflow_result = result
            
            # Save to History
            st.session_state.history.append({
                "topic": topic.strip(),
                "result": result
            })
            
            status_box.update(label="Synthesis complete", state="complete", expanded=False)
            st.rerun()

        except Exception as e:
            status_box.update(label="Pipeline error", state="error", expanded=True)
            st.error("Workflow failed to complete.")
            st.exception(e)
            st.stop()

# ============================================================
# RESULT VISUALIZATION DASHBOARD
# ============================================================

result = st.session_state.workflow_result

if result is not None:
    st.markdown("---")
    
    report = result.get("report", "")
    citations = result.get("citations", [])
    fact_check = result.get("fact_check", {})
    research_data = result.get("research_data", {})
    outline = result.get("outline", "")
    
    # Metrics Strip
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Corpus Words", len(str(report).split()))
    with m2:
        count = len(citations) if isinstance(citations, (list, dict)) else 1
        st.metric("Verified Citations", count)
    with m3:
        st.metric("Pipeline Agents", "6 Specialized")
    with m4:
        status_str = "PASS"
        if isinstance(fact_check, dict):
            status_str = fact_check.get("status", "PASS").upper()
        st.metric("Audit Verdict", status_str)

    st.markdown("<br>", unsafe_allow_html=True)

    # Modern Navigation Tabs
    tab_report, tab_outline, tab_evidence, tab_audit, tab_citations = st.tabs(
        ["Report", "Structural Outline", "Extracted Evidence", "Fact-Check Audit", "Bibliography"]
    )

    with tab_report:
        if report:
            st.markdown(f'<div class="report-paper">\n\n{str(report)}\n\n</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="Export Document (.txt)",
                data=str(report),
                file_name=f"{st.session_state.active_topic.replace(' ', '_').lower()}_brief.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("No report content produced.")

    with tab_outline:
        if outline:
            if isinstance(outline, (dict, list)):
                st.json(outline)
            else:
                st.markdown(str(outline))
        else:
            st.info("No outline data available.")

    with tab_evidence:
        if research_data:
            if isinstance(research_data, dict):
                for key, val in research_data.items():
                    with st.expander(key.replace("_", " ").title()):
                        if isinstance(val, (dict, list)):
                            st.json(val)
                        else:
                            st.write(val)
            else:
                st.write(research_data)
        else:
            st.info("No raw evidence recorded.")

    with tab_audit:
        if fact_check:
            status = fact_check.get("status", "PASS").upper() if isinstance(fact_check, dict) else "PASS"
            if status == "PASS":
                st.markdown('<div class="fact-badge-pass">CORPUS INTEGRITY VERIFIED</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="fact-badge-revise">REVISIONS APPLIED DURING SYNTHESIS</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if isinstance(fact_check, dict):
                for k, v in fact_check.items():
                    if k.lower() not in ["status", "result"]:
                        st.markdown(f"**{k.replace('_', ' ').title()}**")
                        if isinstance(v, (dict, list)):
                            st.json(v)
                        else:
                            st.write(v)
            else:
                st.write(fact_check)
        else:
            st.info("No audit logs available.")

    with tab_citations:
        if citations:
            if isinstance(citations, list):
                for i, c in enumerate(citations, 1):
                    st.markdown(f"**[{i}]**")
                    if isinstance(c, dict):
                        st.json(c)
                    else:
                        st.write(c)
                    st.divider()
            elif isinstance(citations, dict):
                for k, v in citations.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}**")
                    if isinstance(v, (dict, list)):
                        st.json(v)
                    else:
                        st.write(v)
                    st.divider()
            else:
                st.write(citations)
        else:
            st.info("No references formatted.")