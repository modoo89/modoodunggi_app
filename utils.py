
import pandas as pd

def extract_info_from_pdf(file):
    # 실제 등기부 분석 로직은 별도 처리
    return {
        "소유자": "홍길동",
        "주소": "서울시 송파구 문정동 100",
        "전용면적": "84.99㎡",
        "지역": "서울",
        "loan_summary": {
            "근저당권자": "국민은행",
            "채권최고액": 220000000,
            "적용비율": "110%",
            "추정원금": 200000000
        }
    }

def simulate_loan_products(kb_price, existing_loan, region):
    data = []
    for name, ltv, rate in [
        ("은행-1주택", 0.7, 0.042),
        ("보험-1주택", 0.7, 0.045),
        ("상호금융", 0.85, 0.046)
    ]:
        max_amount = int(kb_price * ltv * 10000)
        if "상호금융" in name:
            bg = 55000000 if region == "서울" else 48000000
            max_amount -= bg
        if max_amount <= existing_loan:
            continue
        monthly = int((max_amount * rate) / 12)
        data.append({
            "상품": name,
            "LTV": f"{ltv*100:.0f}%",
            "금리": f"{rate*100:.2f}%",
            "대출한도": f"{max_amount:,}원",
            "월이자": f"{monthly:,}원"
        })
    return pd.DataFrame(data)

def generate_report(info, kb_price, sim_df):
    lines = [
        f"**소유자**: {info['소유자']}",
        f"**주소**: {info['주소']}",
        f"**전용면적**: {info['전용면적']}",
        f"**KB 시세**: {kb_price}만원",
        "---",
        "**📊 대출 시나리오 요약 (가능 상품만)**"
    ]
    for _, row in sim_df.iterrows():
        lines.append(f"- {row['상품']}: {row['대출한도']} / {row['월이자']} / 금리 {row['금리']}")
    return "\n".join(lines)
