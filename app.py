import streamlit as st
import google.generativeai as genai
import json
import os
import time

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v15.0", layout="wide")

# ==========================================
# 💾 1. 로컬 데이터 저장/불러오기 기능 (웹이 꺼져도 보관)
# ==========================================
DATA_FILE = "saved_templates.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 세션 상태 초기화 (JSON 파일에서 불러오기)
if "custom_templates" not in st.session_state:
    st.session_state["custom_templates"] = load_data()
if "selected_bench_data" not in st.session_state: 
    st.session_state["selected_bench_data"] = None

# ==========================================
# 📋 2. 공통 사이드바 설정
# ==========================================
st.sidebar.header("📋 기본 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("상품명")
target_user = st.sidebar.text_input("타겟 고객")

# ==========================================
# 📑 3. 메인 화면 (3개의 탭)
# ==========================================
tab1, tab2, tab3 = st.tabs(["🎯 1. 상세페이지 자동 생성", "➕ 2. 벤치마킹 데이터 등록", "🖼️ 3. 상세페이지 샘플 선택 (갤러리)"])

# --------------------------
# 🎯 [1번 탭] 자동 생성 & 애니메이션
# --------------------------
with tab1:
    st.subheader("🖼️ 상세페이지 8단계 즉시 생성")
    uploaded_files = st.file_uploader("📂 [A] 일반 상품 이미지", type=["png", "jpg"], accept_multiple_files=True)
    screenshot_files = st.file_uploader("📸 [B] 벤치마킹 스크린샷", type=["png", "jpg"], accept_multiple_files=True)
    
    if st.session_state["selected_bench_data"]:
        st.success(f"✅ 선택된 템플릿이 적용되었습니다! (내용: {st.session_state['selected_bench_data'][:30]}...)")
    
    if st.button("🚀 8장 상세페이지 생성 시작", type="primary"):
        if not api_key or not product_name: 
            st.error("🚨 왼쪽 사이드바에서 API Key와 상품명을 필수로 입력해주세요.")
        else:
            # 💡 로딩 애니메이션 컨테이너
            loading_ui = st.empty()
            loading_ui.markdown(
                """
                <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                    <img src='https://i.gifer.com/ZKZg.gif' width='60'>
                    <h3 style='color: #1f77b4;'>AI가 상세페이지를 열심히 기획하고 있습니다... 잠시만 기다려주세요!</h3>
                </div>
                """, unsafe_allow_html=True
            )
            
            try:
                genai.configure(api_key=api_key)
                # 💡 404 에러 해결을 위해 -latest 명시
                model = genai.GenerativeModel("gemini-pro") 
                
                template = st.session_state["selected_bench_data"] or "1.문제제기->2.공감->3.해결책->4.상세스펙->5.비교우위->6.리뷰->7.혜택->8.구매촉구"
                steps = template.split("->")
                
                # 진행 상태 표시기 (진행 바)
                progress_bar = st.progress(0)
                
                for i, step in enumerate(steps):
                    st.markdown(f"---")
                    st.subheader(f"✅ {i+1}단계: {step}")
                    
                    prompt = f"상품 '{product_name}'을(를) 타겟 '{target_user}'에게 판매하기 위한 상세페이지 {step} 단계의 내용을 설득력 있게 작성해줘. 시각적인 이미지 연출 가이드도 포함해줘."
                    
                    with st.spinner(f"✨ {step} 단계 내용 생성 중..."):
                        response = model.generate_content(prompt)
                        st.write(response.text)
                        
                    # 진행률 업데이트
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(1) # 시각적 효과를 위한 약간의 딜레이
                
                # 완료 후 로딩 애니메이션 제거 및 성공 메시지
                loading_ui.empty()
                st.balloons()
                st.success("🎉 8장 상세페이지 기획이 완벽하게 끝났습니다!")
                
            except Exception as e:
                loading_ui.empty()
                st.error(f"🚨 생성 중 에러가 발생했습니다. (API 키나 네트워크를 확인하세요)\n\n상세 오류: {e}")

# --------------------------
# ➕ [2번 탭] 벤치마킹 등록
# --------------------------
with tab2:
    st.subheader("➕ 벤치마킹 데이터 등록 (영구 저장)")
    new_title = st.text_input("템플릿 이름 (예: 신뢰도 상승형 공식)")
    bench_text = st.text_area("벤치마킹 뼈대/설명 (예: 1.후킹->2.증명->3.혜택)")
    
    if st.button("💾 템플릿 영구 저장"):
        if new_title and bench_text:
            st.session_state["custom_templates"][new_title] = bench_text
            save_data(st.session_state["custom_templates"]) # JSON 파일에 저장
            st.success(f"'{new_title}' 템플릿이 저장되었습니다! 브라우저를 닫아도 유지됩니다.")
        else:
            st.warning("템플릿 이름과 내용을 모두 입력해주세요.")

# --------------------------
# 🖼️ [3번 탭] 피코파일럿 스타일 갤러리
# --------------------------
with tab3:
    st.subheader("🎨 상세페이지 템플릿 라이브러리")
    st.markdown("피코파일럿처럼 원하는 템플릿을 한눈에 보고 선택하세요.")
    
    if not st.session_state["custom_templates"]:
        st.info("현재 등록된 템플릿이 없습니다. 2번 탭에서 새로운 템플릿을 등록해주세요.")
    else:
        # 가로로 3개씩 나열되는 그리드 레이아웃 생성
        cols = st.columns(3)
        
        for i, (title, data) in enumerate(st.session_state["custom_templates"].items()):
            # i % 3을 통해 1, 2, 3번째 칸에 순차적으로 카드 배치
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="color: #333; margin-bottom: 10px;">{title}</h4>
                        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=300&q=80" style="width: 100%; border-radius: 5px; margin-bottom: 10px;" alt="placeholder">
                        <p style="font-size: 12px; color: #666; height: 40px; overflow: hidden;">{data[:50]}...</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                
                # 선택 버튼
                if st.button(f"✨ '{title}' 선택하기", key=f"select_{title}", use_container_width=True):
                    st.session_state["selected_bench_data"] = data
                    st.success(f"[{title}] 선택 완료! 1번 탭으로 이동해서 생성을 시작하세요.")
