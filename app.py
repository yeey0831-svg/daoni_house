import streamlit as st
import google.generativeai as genai
import requests
import io
import base64
from PIL import Image

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v13.0", layout="wide")

# 세션 상태 초기화
if "custom_templates" not in st.session_state:
    st.session_state["custom_templates"] = {}

# 사이드바: 고정 입력값
st.sidebar.header("📋 필수 입력 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("상품명")
target_user = st.sidebar.text_input("타겟 고객")

# 탭 구성
tab1, tab2 = st.tabs(["🎯 1. 상세페이지 자동 생성 (8장)", "➕ 2. 벤치마킹 템플릿 등록"])

with tab1:
    st.subheader("🖼️ 상세페이지 8단계 자동 제작")
    all_templates = {**{
        "🔥 [A타입] 불편함 해결형": "1.불편함 폭로->2.공감->3.반전 솔루션->4.성능지표->5.리뷰인증->6.비교우위->7.가격혜택->8.구매촉구",
        "✨ [B타입] 감성 라이프형": "1.감성 연출->2.일상을 바꾸는 순간->3.디테일 마감->4.공간 활용->5.패키징->6.선물 추천->7.고객 후기->8.브랜드 스토리"
    }, **st.session_state["custom_templates"]}
    
    selected_template = st.selectbox("공식 선택", list(all_templates.keys()))
    
    if st.button("🚀 8장 상세페이지 전체 생성 시작"):
        if not api_key: st.error("API Key 필요")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            structure = all_templates[selected_template].split("->")
            
            for i, step in enumerate(structure):
                st.markdown(f"--- \n ### {i+1}단계: {step}")
                # 1. 텍스트 기획
                prompt = f"{product_name} 상품을 위해 '{step}'에 맞는 상세페이지 내용과 이미지 생성 프롬프트를 작성해줘."
                text_res = model.generate_content(prompt)
                st.write(text_res.text)
                
                # 2. 이미지 생성
                img_prompt = f"Professional e-commerce product banner for {product_name}, {step}, high quality, photorealistic"
                # (이곳에 이전과 동일한 Imagen API 호출 코드 삽입)
                st.info(f"✨ {step} 이미지 생성 완료 (예정)")

with tab2:
    st.subheader("🔗 벤치마킹 데이터 추출")
    new_title = st.text_input("템플릿 이름")
    bench_data = st.text_area("벤치마킹할 내용 입력")
    if st.button("템플릿 저장"):
        st.session_state["custom_templates"][new_title] = bench_data
        st.success("새 템플릿이 저장되었습니다!")
