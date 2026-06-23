import streamlit as st
import google.generativeai as genai
import io
from PIL import Image

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v14.0", layout="wide")

# 세션 상태 초기화
if "custom_templates" not in st.session_state: st.session_state["custom_templates"] = {}
if "selected_bench_data" not in st.session_state: st.session_state["selected_bench_data"] = None

# [공통 사이드바: 입력]
st.sidebar.header("📋 기본 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("상품명")
target_user = st.sidebar.text_input("타겟 고객")

# 3개의 탭 구성
tab1, tab2, tab3 = st.tabs(["🎯 1. 상세페이지 자동 생성", "➕ 2. 벤치마킹 데이터 등록", "🖼️ 3. 상세페이지 샘플 선택"])

with tab1:
    st.subheader("🖼️ 상세페이지 8단계 즉시 생성")
    # 이미지 업로드 필드 복구
    uploaded_files = st.file_uploader("📂 [A] 일반 상품 이미지", type=["png", "jpg"], accept_multiple_files=True)
    screenshot_files = st.file_uploader("📸 [B] 벤치마킹 스크린샷", type=["png", "jpg"], accept_multiple_files=True)
    
    if st.button("🚀 8장 상세페이지 생성 시작"):
        if not api_key or not product_name: st.error("API Key와 상품명을 확인하세요.")
        else:
            st.write(f"⚙️ {product_name}에 대한 8단계 상세페이지 기획을 시작합니다.")
            # 이곳에 제미나이 생성 로직 + 이미지 처리 로직 구현

with tab2:
    st.subheader("➕ 벤치마킹 데이터 등록")
    new_title = st.text_input("템플릿 이름")
    bench_text = st.text_area("벤치마킹 뼈대/설명")
    if st.button("템플릿 저장"):
        st.session_state["custom_templates"][new_title] = bench_text
        st.success(f"'{new_title}'이 저장되었습니다.")

with tab3:
    st.subheader("🖼️ 상세페이지 샘플 라이브러리")
    # 등록된 템플릿 목록 출력
    if not st.session_state["custom_templates"]:
        st.info("등록된 샘플이 없습니다. 2번 탭에서 샘플을 먼저 등록하세요.")
    else:
        for title, data in st.session_state["custom_templates"].items():
            with st.expander(f"📦 {title}"):
                st.write(data)
                if st.button(f"이 샘플로 1번 탭 이동", key=title):
                    st.session_state["selected_bench_data"] = data
                    st.success("샘플이 선택되었습니다! 1번 탭에서 상세페이지를 제작하세요.")
