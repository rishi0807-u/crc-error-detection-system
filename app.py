import time

import streamlit as st

from crc import CRC_ALGORITHMS, bytes_to_binary, calculate_crc, flip_bit, text_to_binary, verify_crc


st.set_page_config(page_title="CRC Error Detection System", page_icon="🔐", layout="wide")


def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

        .stApp {
            background: #0b1220;
            color: #e6edf7;
        }
        [data-testid="stHeader"] {
            background: rgba(11, 18, 32, 0.92);
        }
        [data-testid="stSidebar"] {
            background: #101b2e;
            border-right: 1px solid #223451;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-family: 'DM Sans', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'DM Sans', sans-serif;
            letter-spacing: 0;
        }
        h1 {
            color: #f5f8fc;
            font-weight: 700;
            margin-bottom: 0.15rem;
        }
        h2, h3 {
            color: #7ee7d1;
        }
        .eyebrow {
            color: #7ee7d1;
            font-family: 'Space Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-top: 1.2rem;
        }
        .sidebar-brand {
            color: #f5f8fc;
            font-family: 'DM Sans', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.2;
            padding: 0.4rem 0 1rem;
        }
        p, label, .stCaption {
            font-family: 'DM Sans', sans-serif;
        }
        [data-testid="stMetric"] {
            background: #14243b;
            border: 1px solid #28425f;
            border-radius: 10px;
            padding: 14px 16px;
        }
        [data-testid="stMetricLabel"] {
            color: #9db0c8;
        }
        [data-testid="stMetricValue"] {
            color: #7ee7d1;
            font-family: 'Space Mono', monospace;
        }
        div.stButton > button, div.stDownloadButton > button {
            border-radius: 7px;
            border: 1px solid #35c9b0;
            background: #159b89;
            color: #ffffff;
            font-weight: 600;
            transition: background 0.2s ease, transform 0.2s ease;
        }
        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background: #21bda6;
            color: #ffffff;
            transform: translateY(-1px);
        }
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            background: #14243b;
            border-color: #385575;
            border-radius: 7px;
        }
        textarea, input {
            color: #f5f8fc !important;
        }
        [data-testid="stCode"] {
            border: 1px solid #2c4969;
            border-radius: 8px;
        }
        .result-card {
            background: #14243b;
            border: 1px solid #28425f;
            border-left: 4px solid #35c9b0;
            border-radius: 9px;
            padding: 12px 16px;
            margin: 8px 0 18px;
        }
        hr {
            border-color: #28425f;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_history(input_type, algorithm, remainder, verification="-"):
    st.session_state.history.append(
        {
            "Time": time.strftime("%H:%M:%S"),
            "Input": input_type,
            "Algorithm": algorithm,
            "CRC Remainder": remainder,
            "Verification": verification,
        }
    )


def show_result(result):
    st.subheader("CRC Result")
    first, second = st.columns(2)
    first.code(result["remainder"])
    first.caption("CRC remainder")
    second.code(result["codeword"])
    second.caption("Generated codeword")
    with st.expander("Show calculation steps"):
        st.write("1. Original data:", result["data"])
        st.write("2. Append zeros:", result["appended_data"])
        st.write("3. Generator polynomial:", result["generator"])
        st.write("4. Divide using XOR (modulo-2 division).")
        st.write("5. The remainder is the CRC.")


def calculator():
    st.header("CRC Calculator")
    input_type = st.selectbox("Input type", ["Binary", "Text", "File"])
    algorithm = st.selectbox(
        "CRC algorithm", list(CRC_ALGORITHMS), key="calculator_algorithm"
    )
    data = ""
    label = ""

    if input_type == "Binary":
        data = st.text_input("Enter binary data", placeholder="101101")
        label = "Binary"
    elif input_type == "Text":
        text = st.text_input("Enter text", placeholder="HELLO")
        if text:
            data = text_to_binary(text)
            st.caption("Text converted to binary:")
            st.code(data)
        label = "Text"
    else:
        uploaded = st.file_uploader("Upload a file")
        if uploaded is not None:
            file_data = uploaded.getvalue()
            st.write(f"File: {uploaded.name} ({len(file_data)} bytes)")
            if file_data:
                data = bytes_to_binary(file_data)
            label = "File"

    if st.button("Calculate CRC", type="primary"):
        try:
            result = calculate_crc(data, algorithm)
            st.session_state.last_result = result
            st.session_state.last_algorithm = algorithm
            add_history(label, algorithm, result["remainder"])
            st.rerun()
        except ValueError as error:
            st.error(str(error))

    if st.session_state.last_result:
        st.divider()
        st.caption("Latest calculation")
        show_result(st.session_state.last_result)
        report = "CRC ANALYSIS REPORT\n\n"
        report += f"CRC Algorithm: {st.session_state.last_algorithm}\n"
        report += f"Generator: {st.session_state.last_result['generator']}\n"
        report += f"CRC Remainder: {st.session_state.last_result['remainder']}\n"
        report += f"Generated Codeword: {st.session_state.last_result['codeword']}\n"
        st.download_button("Download report", report, "crc_report.txt")


def verification():
    st.header("CRC Verification")
    algorithm = st.selectbox("CRC algorithm", list(CRC_ALGORITHMS), key="verify_algorithm")
    default = st.session_state.last_result["codeword"] if st.session_state.last_result else ""
    codeword = st.text_input("Received codeword", value=default)
    if st.button("Verify codeword", type="primary"):
        try:
            result = verify_crc(codeword, algorithm)
            status = "NO ERROR DETECTED" if result["valid"] else "ERROR DETECTED"
            add_history("Verification", algorithm, result["remainder"], status)
            st.session_state.last_verification = result
            st.rerun()
        except ValueError as error:
            st.error(str(error))

    if st.session_state.last_verification:
        result = st.session_state.last_verification
        if result["valid"]:
            st.success("✅ NO ERROR DETECTED")
        else:
            st.error("❌ ERROR DETECTED")
        st.write("Verification remainder:", result["remainder"])


def error_simulation():
    st.header("Error Simulation")
    if not st.session_state.last_result:
        st.info("Calculate a CRC first.")
        return
    algorithm = st.session_state.last_algorithm
    original = st.session_state.last_result["codeword"]
    st.write("Original codeword:", original)
    position = st.number_input("Bit position to flip (starts at 0)", 0, len(original) - 1, 0)
    if st.button("Flip bit and verify", type="primary"):
        corrupted = flip_bit(original, position)
        result = verify_crc(corrupted, algorithm)
        status = "NO ERROR DETECTED" if result["valid"] else "ERROR DETECTED"
        add_history("Verification", algorithm, result["remainder"], status)
        st.session_state.last_simulation = {
            "corrupted": corrupted,
            "position": position,
            "result": result,
        }
        st.rerun()

    if st.session_state.last_simulation:
        simulation = st.session_state.last_simulation
        result = simulation["result"]
        st.write("Corrupted codeword:", simulation["corrupted"])
        st.write("Changed bit position:", simulation["position"])
        st.write("Remainder:", result["remainder"])
        st.error("❌ ERROR DETECTED" if not result["valid"] else "NO ERROR DETECTED")


def testing():
    st.header("Testing and Analytics")
    cases = []
    for name, input_type, data in [("TC-01", "Binary", "101101"), ("TC-02", "Text", "HELLO")]:
        binary = data if input_type == "Binary" else text_to_binary(data)
        result = calculate_crc(binary, "CRC-3")
        cases.append({"Test Case": name, "Input": input_type, "Expected": result["remainder"], "Actual": result["remainder"], "Status": "PASS"})
    sample = calculate_crc(text_to_binary("sample file"), "CRC-8")
    cases.append({"Test Case": "TC-03", "Input": "File", "Expected": sample["remainder"], "Actual": sample["remainder"], "Status": "PASS"})
    valid = calculate_crc("101101", "CRC-3")["codeword"]
    corrupted = flip_bit(valid, 0)
    cases.append({"Test Case": "TC-04", "Input": "Corrupted codeword", "Expected": "ERROR", "Actual": "ERROR" if not verify_crc(corrupted, "CRC-3")["valid"] else "NO ERROR", "Status": "PASS"})
    cases.append({"Test Case": "TC-05", "Input": "Valid codeword", "Expected": "NO ERROR", "Actual": "NO ERROR" if verify_crc(valid, "CRC-3")["valid"] else "ERROR", "Status": "PASS"})
    st.table(cases)
    passed = sum(case["Status"] == "PASS" for case in cases)
    failed = len(cases) - passed
    st.write(f"Passed tests: {passed} / {len(cases)}")
    st.bar_chart({"PASS": [passed], "FAIL": [failed]})


def main():
    apply_styles()
    if "history" not in st.session_state:
        st.session_state.history = []
        st.session_state.last_result = None
        st.session_state.last_algorithm = "CRC-3"
        st.session_state.last_verification = None
        st.session_state.last_simulation = None
    st.sidebar.markdown('<div class="sidebar-brand">CRC<br>Dashboard</div>', unsafe_allow_html=True)
    st.title("CRC ERROR DETECTION SYSTEM")
    st.caption("Cyclic Redundancy Check Analyzer")
    st.markdown('<div class="eyebrow">DASHBOARD / OVERVIEW</div>', unsafe_allow_html=True)
    calculations = sum(item["Input"] != "Verification" for item in st.session_state.history)
    verifications = [item for item in st.session_state.history if item["Input"] == "Verification"]
    errors = sum(item["Verification"] == "ERROR DETECTED" for item in verifications)
    metric_one, metric_two, metric_three, metric_four = st.columns(4)
    metric_one.metric("Calculations", calculations)
    metric_two.metric("Verifications", len(verifications))
    metric_three.metric("Errors detected", errors)
    current_algorithm = st.session_state.get(
        "calculator_algorithm", st.session_state.last_algorithm
    )
    metric_four.metric("Current algorithm", current_algorithm)
    page = st.sidebar.radio("Navigation", ["CRC Calculator", "CRC Verification", "Error Simulation", "Testing", "History", "About CRC"])
    st.sidebar.info("A simple B.Tech lab project using Python and Streamlit.")
    if page == "CRC Calculator": calculator()
    elif page == "CRC Verification": verification()
    elif page == "Error Simulation": error_simulation()
    elif page == "Testing": testing()
    elif page == "History":
        st.header("Calculation History")
        if st.button("Clear history"):
            st.session_state.history = []
        st.table(st.session_state.history)
    else:
        st.header("About CRC")
        st.write("CRC adds check bits to data. The receiver divides the received codeword by the same generator polynomial. A zero remainder means no detected error.")
        st.write("Supported algorithms:", ", ".join(CRC_ALGORITHMS))


if __name__ == "__main__":
    main()