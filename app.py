import streamlit as st
import google.generativeai as genai
import requests
import time

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v17.0 (안정화)", layout="wide")

st.title("🎯 쿠팡형 AI 상세페이지 마스터 (초간결 핵심 버전)")
st.markdown("---")
st.info("💡 기존의 오류 유발 요소를 모두 제거했습니다. 오직 **[상세페이지 8단계 기획안의 완벽한 자동 생성]**에만 집중합니다.")

# ==========================================
# 📋 1. 사이드바 필수 입력 정보 (초간결 구성)
# ==========================================
st.sidebar.header("📋 필수 마케팅 정보")
raw_api_key = st.sidebar.text_input("Google API Key", type="password", help="구글 AI 스튜디오에서 발급받은 API 키를 입력하세요.")
product_name = st.sidebar.text_input("상품명 (예: 다온 밀봉 자석 밀폐 집게)")
target_user = st.sidebar.text_input("타겟 고객 (예: 주부, 1인 가구, 자취생)")

# 가장 안정적인 최신 1.5 버전 모델 고정
model_choice = "gemini-1.5-flash"

# ==========================================
# 🎯 2. 일관성 있는 쿠팡 최적화 8단계 공식 정의
# ==========================================
STEPS = [
    "1단계: 강력한 Hooking 및 문제 제기 (소비자가 일상에서 느끼는 극심한 불편함 자극)",
    "2단계: 소비자 공감 유도 (나만 겪는 불편함이 아니라는 깊은 유대감 형성)",
    "3단계: 해결책 제시 및 제품 등장 (문제를 한 방에 해결해 줄 우리 제품 최초 공개)",
    "4단계: 핵심 스펙 및 독보적 차별점 (눈으로 확인하는 제품의 압도적인 기술력과 기능 강조)",
    "5단계: 타사 제품과의 비교 우위 (저가형/일반 제품과 확실하게 차별화되는 비교 포인트 기획)",
    "6단계: 실제 고객 리뷰 및 신뢰도 증명 (소비자의 의심을 확신으로 바꾸는 리얼 후기 연출)",
    "7단계: 구매 혜택 및 구성 안내 (지금 사야만 하는 특별 구성 및 한정 이벤트 강조)",
    "8단계: 최종 구매 촉구 및 낙오 방지 (한정 수량 강조 및 심리적 마감 압박으로 구매 유도)"
]

# ==========================================
# 🚀 3. 핵심 자동 생성 엔진 (3중 필터링 우회 통신 적용)
# ==========================================
if st.button("🚀 8단계 상세페이지 기획서 즉시 생성 시작", type="primary"):
    if not raw_api_key:
        st.error("🚨 왼쪽 사이드바에서 Google API Key를 입력해 주세요.")
    elif not product_name:
        st.error("🚨 왼쪽 사이드바에서 상품명을 입력해 주세요.")
    else:
        # API 키 앞뒤 불필요한 공백 제거 (404/403 에러 예방의 핵심)
        api_key = raw_api_key.strip()
        
        progress_bar = st.progress(0)
        st.success(f"🔥 '{product_name}' 상품에 대한 대형 이커머스 상세페이지 기획을 시작합니다. 잠시만 기다려주세요.")
        
        # 8단계 순차 루프 제어
        for i, step in enumerate(STEPS):
            st.markdown(f"### 📦 {step}")
            
            # 일관성 있는 출력을 위한 규격화된 마스터 프롬프트
            prompt = f"""
            당신은 대한민국 최고의 이커머스 CRO(전환율 최적화) 카피라이터이자 UX 디자인 디렉터입니다.
            아래 정보를 바탕으로 쿠팡 상세페이지의 [{step}] 영역에 들어갈 결과물을 만들어주세요.

            [기본 상품 정보]
            - 상품명: {product_name}
            - 타겟 고객: {target_user if target_user else '일반 소비자 및 해당 제품이 필요한 잠재 고객'}

            [출력 서식 - 일관성을 위해 반드시 아래 구조로만 작성하세요]
            ### 1. 메인 헤드카피 (고객의 시선을 멈추게 할 한 줄 문구)
            - 
            ### 2. 상세 카피라이팅 (설득력 있는 본문 글감 및 상세 문구)
            - 
            ### 3. 비주얼 연출 및 UI 가이드 (디자이너를 위한 가로 780px 기준의 이미지 컷, 색상, 배치 그래픽 가이드)
            - 

            주의: 반드시 한국어로 정중하면서도 강력한 구매 유도 어조로 작성해 주세요.
            """
            
            with st.spinner(f"✨ {i+1}/8 단계 작성 중..."):
                result_text = None
                error_logs = []
                
                # [루틴 1] 공식 SDK 라이브러리 호출 시도
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_choice)
                    response = model.generate_content(prompt)
                    if response and response.text:
                        result_text = response.text
                except Exception as e:
                    error_logs.append(f"SDK 통신 오류: {str(e)}")
                
                # [루틴 2] SDK 실패 시 정식 v1 REST API 직통 서버 통신 (우회로 1)
                if not result_text:
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1/models/{model_choice}:generateContent?key={api_key}"
                        headers = {'Content-Type': 'application/json'}
                        payload = {"contents": [{"parts": [{"text": prompt}]}]}
                        res = requests.post(url, headers=headers, json=payload, timeout=30)
                        
                        if res.status_code == 200:
                            result_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                        else:
                            error_logs.append(f"정식 v1 서버 거부 (코드 {res.status_code})")
                    except Exception as e:
                        error_logs.append(f"정식 v1 서버 예외: {str(e)}")
                
                # [루틴 3] 최종 수단 v1beta REST API 통신 (우회로 2)
                if not result_text:
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_choice}:generateContent?key={api_key}"
                        headers = {'Content-Type': 'application/json'}
                        payload = {"contents": [{"parts": [{"text": prompt}]}]}
                        res = requests.post(url, headers=headers, json=payload, timeout=30)
                        
                        if res.status_code == 200:
                            result_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                    except Exception as e:
                        error_logs.append(f"테스트용 v1beta 서버 예외: {str(e)}")
                
                # 화면 최종 출력 처리 및 예외 핸들링
                if result_text:
                    st.markdown(result_text)
                    st.markdown("<br><hr style='border:1px solid #eee;'><br>", unsafe_allow_html=True)
                else:
                    st.error(f"🚨 {i+1}단계 생성 중 통신 장벽이 발생했습니다. API 키가 활성화 상태인지 확인해 주세요.")
                    with st.expander("🔍 기술 디버깅 로그 확인"):
                        for log in error_logs:
                            st.write(log)
            
            # 진행률 바 업데이트 및 미세 과부하 방지 딜레이
            progress_bar.progress((i + 1) / len(STEPS))
            time.sleep(0.3)
            
        st.balloons()
        st.success("🎉 축하합니다! 쿠팡형 8단계 마케팅 상세페이지 기획서가 일관성 있게 모두 완성되었습니다!")
