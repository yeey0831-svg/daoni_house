import streamlit as st
import google.generativeai as genai
import io
from PIL import Image

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v14.1", layout="wide")

# 세션 상태 초기화
if "custom_templates" not in st.session_state: st.session_state["custom_templates"] = {}
if "selected_bench_data" not in st.session_state: st.session_state["selected_bench_data"] = None

# [공통 사이드바: 입력]
st.sidebar.header("📋 기본 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("상품명")
target_user = st.sidebar.text_input("타겟 고객")

tab1, tab2, tab3 = st.tabs(["🎯 1. 상세페이지 자동 생성", "➕ 2. 벤치마킹 데이터 등록", "🖼️ 3. 상세페이지 샘플 선택"])

with tab1:
    st.subheader("🖼️ 상세페이지 8단계 즉시 생성")
    uploaded_files = st.file_uploader("📂 [A] 일반 상품 이미지", type=["png", "jpg"], accept_multiple_files=True)
    
    # 샘플이 선택되었다면 표시
    if st.session_state["selected_bench_data"]:
        st.info(f"현재 선택된 템플릿: {st.session_state['selected_bench_data'][:50]}...")
    
    if st.button("🚀 8장 상세페이지 생성 시작"):
        if not api_key or not product_name: 
            st.error("API Key와 상품명을 확인하세요.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # 8단계 구조 정의 (선택된 템플릿이 없으면 기본값 사용)
                template = st.session_state["selected_bench_data"] or "1.문제제기->2.공감->3.해결책->4.상세스펙->5.비교우위->6.리뷰->7.혜택->8.구매촉구"
                steps = template.split("->")
                
                for i, step in enumerate(steps):
                    st.markdown(f"---")
                    st.subheader(f"✅ {i+1}단계: {step}")
                    
                    # AI에게 기획 요청
                    prompt = f"상품 '{product_name}'을(를) 타겟 '{target_user}'에게 판매하기 위한 상세페이지 {step} 단계의 내용을 설득력 있게 작성해줘."
                    with st.spinner(f"{step} 단계 생성 중..."):
                        response = model.generate_content(prompt)
                        st.write(response.text)
            except Exception as e:
                st.error(f"생성 중 오류 발생: {e}")

with tab2:
    st.subheader("➕ 벤치마킹 데이터 등록")
    new_title = st.text_input("템플릿 이름")
    bench_text = st.text_area("벤치마킹 뼈대/설명 (예: 1.후킹->2.증명->3.혜택)")
    if st.button("템플릿 저장"):
        st.session_state["custom_templates"][new_title] = bench_text
        st.success(f"'{new_title}'이 저장되었습니다.")

with tab3:
    st.subheader("🖼️ 상세페이지 샘플 라이브러리")
    if not st.session_state["custom_templates"]:
        st.info("등록된 샘플이 없습니다.")
    else:
        for title, data in st.session_state["custom_templates"].items():
            with st.expander(f"📦 {title}"):
                st.write(data)
                if st.button(f"이 샘플로 1번 탭 이동", key=title):
                    st.session_state["selected_bench_data"] = data
                    st.success(f"'{title}' 샘플이 선택되었습니다! 1번 탭으로 이동하세요.")
