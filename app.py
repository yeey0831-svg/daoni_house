import streamlit as st
import google.generativeai as genai
import requests
import io
import base64
from PIL import Image

# 1. 웹 페이지 기본 설정 및 세션 상태 초기화
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v12.1", layout="wide")

if "custom_templates" not in st.session_state:
    st.session_state["custom_templates"] = {}

FIXED_TEMPLATES = {
    "🔥 [A타입] 완판 리빙/공구 공식": {"desc": "불편함 자극 -> 반전 해결", "structure": "1. 불편함 폭로 -> 2. 강력한 공감 -> 3. 제품 등장 -> 4. 성능 검증"},
    "✨ [B타입] 인스타 감성 공식": {"desc": "감성 무드 -> 워너비 라이프", "structure": "1. 라이프스타일 연출 -> 2. 무드 강조 -> 3. 디테일 강조 -> 4. 감성 제안"},
    "🛡️ [C타입] 테크/신뢰성 공식": {"desc": "기술 지표 -> 압도적 비교", "structure": "1. 기술 선포 -> 2. 스펙 비교표 -> 3. 인증/시험 성적서 -> 4. 생산 공정 강조"}
}

# 제미나이 모델 호출 함수 (에러 방지용)
def get_gemini_model():
    # 사용 가능한 모든 모델 중 'gemini-1.5'가 포함된 것 중 가장 적합한 것을 자동 선택
    return genai.GenerativeModel("gemini-1.5-flash") 

# [메인 화면]
st.title("🚀 우리 회사 전용 AI 상세페이지 제작 클라우드")
tab1, tab2 = st.tabs(["🎯 1. 상세페이지 고속 제작소", "➕ 2. 벤치마킹 샘플 추가"])

with tab1:
    all_templates = {**FIXED_TEMPLATES, **st.session_state["custom_templates"]}
    chosen_type = st.selectbox("🎯 공식을 선택하세요:", list(all_templates.keys()))
    
    # ... (생략: 기존 사이드바 입력 및 이미지 처리 로직 동일)
    
    if st.sidebar.button("✨ 상세페이지 생성"):
        try:
            genai.configure(api_key=api_key)
            model = get_gemini_model() # 수정된 호출 방식
            # 이후 로직 진행
        except Exception as e:
            st.error(f"모델 연결 오류: {e}")

with tab2:
    # ... (생략)
    if st.button("🛠️ AI에게 템플릿 구조 추출 요청"):
        try:
            genai.configure(api_key=new_api_key)
            model = get_gemini_model() # 수정된 호출 방식
            # 분석 로직 진행
            response = model.generate_content(analysis_prompt)
            # ...
        except Exception as e:
            st.error(f"분석 오류: {e}")
