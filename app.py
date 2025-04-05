
import streamlit as st
from utils import extract_info_from_pdf, simulate_loan_products, generate_report

st.set_page_config(page_title="모두등기", layout="wide")

st.title("🏠 모두등기 – 등기부 & 시세 기반 대출 리포트 자동 생성")

pdf_file = st.file_uploader("📄 등기부등본 PDF 업로드", type=["pdf"])
kb_price_input = st.number_input("💰 KB 시세 (만원 단위)", min_value=0, step=100, format="%d")

if pdf_file and kb_price_input:
    with st.spinner("등기부 분석 중..."):
        info = extract_info_from_pdf(pdf_file)

    if info:
        st.success("✅ 등기부 분석 완료!")
        st.write("### 🧾 고객 기본 정보")
        st.json(info)

        st.write("### 💳 기대출 정보 요약 (을구 기준)")
        st.json(info["loan_summary"])

        st.write("### 📊 상품별 대출 시뮬레이션")
        sim_result = simulate_loan_products(kb_price_input, info["loan_summary"]["추정원금"], info["지역"])
        st.dataframe(sim_result)

        st.write("### 💡 대출 가능 시나리오 요약")
        st.markdown(generate_report(info, kb_price_input, sim_result))
    else:
        st.error("❌ 등기부 정보 추출 실패. 다시 시도해주세요.")
