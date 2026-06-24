import streamlit as st
import json
import os
import time
import requests

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v16.0", layout="wide")

# ==========================================
# 💾 1. 데이터 저장 및 데이터 세팅
# ==========================================
DATA_FILE = "saved_templates.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # 기본 샘플 세팅 (처음 실행 시 자동 등록)
    return {
        "🚀 매출 압도형 8단계 공식": "1.문제제기->2.공감 유도->3.해결책 제시->4.핵심 스펙 안내->5.타사 비교 우위->6.실제 리뷰 증명->7.한정 혜택 강조->8.최종 구매 촉구",
        "🔥 감성 자극 셀링 템플릿": "1.감성 Hooking->2.불편함 공감->3.브랜드 스토리->4.디테일 컷 가이드->5.안전성 검증->6.고객 리얼 후기->7.마감 임박 알림->8.최종 주문서"
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
# 📑 3. 메인 화면 및 탭 구성
# ==========================================
tab1, tab2, tab3 = st.tabs(["🎯 1. 상세페이지 자동 생성", "➕ 2. 벤치마킹 데이터 등록", "🖼️ 3. 상세페이지 샘플 선택 (갤러리)"])

# --------------------------
# 🎯 [1번 탭] 자동 생성 (REST API 하이브리드 적용)
# --------------------------
with tab1:
    st.subheader("🖼️ 상세페이지 8단계 즉시 생성")
    uploaded_files = st.file_uploader("📂 [A] 일반 상품 이미지", type=["png", "jpg"], accept_multiple_files=True)
    screenshot_files = st.file_uploader("📸 [B] 벤치마킹 스크린샷", type=["png", "jpg"], accept_multiple_files=True)
    
    if st.session_state["selected_bench_data"]:
        st.success(f"✅ 3번 탭에서 선택한 구조가 적용되었습니다! (구조: {st.session_state['selected_bench_data'][:60]}...)")
    
    if st.button("🚀 8장 상세페이지 생성 시작", type="primary"):
        if not api_key or not product_name: 
            st.error("🚨 왼쪽 사이드바에서 API Key와 상품명을 필수로 입력해주세요.")
        else:
            loading_ui = st.empty()
            loading_ui.markdown(
                """
                <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                    <img src='https://i.gifer.com/ZKZg.gif' width='60'>
                    <h3 style='color: #1f77b4;'>근본 우회 통신 모듈 가동 중... AI 상세페이지 기획을 시작합니다.</h3>
                </div>
                """, unsafe_allow_html=True
            )
            
            try:
                template = st.session_state["selected_bench_data"] or "1.문제제기->2.공감->3.해결책->4.상세스펙->5.비교우위->6.리뷰->7.혜택->8.구매촉구"
                steps = template.split("->")
                progress_bar = st.progress(0)
                
                for i, step in enumerate(steps):
                    st.markdown(f"---")
                    st.subheader(f"✅ {i+1}단계 기획안: {step}")
                    
                    prompt = f"상품 '{product_name}'을(를) 타겟 '{target_user}'에게 판매하기 위한 쿠팡 상세페이지 '{step}' 단계의 기획 문구와 카피라이팅을 설득력 있게 작성해줘. 디자이너를 위한 세부 시각 연출 가이드도 포함해줘."
                    
                    with st.spinner(f"✨ {step} 생성 중..."):
                        # 라이브러리 충돌 우려를 막기 위한 직통 REST API 통신망 구성 (gemini-1.5-flash 기준)
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        headers = {'Content-Type': 'application/json'}
                        payload = {"contents": [{"parts": [{"text": prompt}]}]}
                        
                        response = requests.post(url, headers=headers, json=payload)
                        res_json = response.json()
                        
                        if response.status_code == 200:
                            result_text = res_json['candidates'][0]['content']['parts'][0]['text']
                            st.write(result_text)
                        else:
                            # 1.5-flash 실패 시 pro 모델로 2차 다이렉트 백업 시도
                            url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
                            response_pro = requests.post(url_pro, headers=headers, json=payload)
                            if response_pro.status_code == 200:
                                st.write(response_pro.json()['candidates'][0]['content']['parts'][0]['text'])
                            else:
                                raise Exception(f"API 호출 실패 (코드 {response.status_code}): {response.text}")
                    
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.5)
                
                loading_ui.empty()
                st.balloons()
                st.success("🎉 8장 상세페이지 전체 기획서가 완성되었습니다!")
                
            except Exception as e:
                loading_ui.empty()
                st.error(f"🚨 시스템 예외 발생: 통신 환경 또는 발급받으신 API Key 자체의 활성화 여부를 확인해 주세요.\n\n오류 내용: {e}")

# --------------------------
# ➕ [2번 탭] 벤치마킹 등록
# --------------------------
with tab2:
    st.subheader("➕ 벤치마킹 데이터 등록 (영구 저장)")
    new_title = st.text_input("템플릿 이름 (예: 다온 프리미엄 레이아웃)")
    bench_text = st.text_area("벤치마킹 뼈대 구조 입력", placeholder="예: 1.후킹->2.소비자공감->3.기술력인증->4.특장점->5.실험데이터->6.실사용리뷰->7.보증제도->8.마감세일")
    
    if st.button("💾 템플릿 영구 저장"):
        if new_title and bench_text:
            st.session_state["custom_templates"][new_title] = bench_text
            save_data(st.session_state["custom_templates"])
            st.success(f"'{new_title}' 템플릿이 안전하게 로컬 디스크에 보관되었습니다.")
        else:
            st.warning("이름과 구조 내용을 빠짐없이 입력하세요.")

# --------------------------
# 🖼️ [3번 탭] 피코파일럿 스타일 가상 이미지 갤러리 UI
# --------------------------
with tab3:
    st.subheader("🎨 상세페이지 템플릿 실물 갤러리")
    st.markdown("쿠팡 최적화 규격 비율 레이아웃입니다. 구조를 시각적으로 확인하고 마음에 드는 템플릿을 고르세요.")
    
    if not st.session_state["custom_templates"]:
        st.info("등록된 데이터가 없습니다. 2번 탭에서 템플릿 구조를 등록해 주세요.")
    else:
        for title, data in st.session_state["custom_templates"].items():
            st.markdown(f"### 📦 {title}")
            steps_list = data.split("->")
            
            # 가로 4칸 배열로 8장의 상세페이지 레이아웃 시각화
            col_sub1 = st.columns(4)
            for idx, step_name in enumerate(steps_list[:4]):
                with col_sub1[idx]:
                    st.markdown(
                        f"""
                        <div style="border: 2px solid #1f77b4; border-radius: 8px; padding: 15px; background-color: #ffffff; text-align: center; box-shadow: 1px 1px 6px rgba(0,0,0,0.1); margin-bottom: 10px;">
                            <span style="background-color: #1f77b4; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">PAGE {idx+1}</span>
                            <h5 style="margin-top: 10px; color: #333;">{step_name}</h5>
                            <div style="background-color: #f7f9fa; border: 1px dashed #ccc; height: 140px; margin-top: 8px; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #888;">
                                쿠팡 규격 가로 780px 비율 영역
                            </div>
                        </div>
                        """, unsafe_allow_html=True
                    )
            
            col_sub2 = st.columns(4)
            for idx, step_name in enumerate(steps_list[4:8]):
                real_idx = idx + 4
                with col_sub2[idx]:
                    st.markdown(
                        f"""
                        <div style="border: 2px solid #2ca02c; border-radius: 8px; padding: 15px; background-color: #ffffff; text-align: center; box-shadow: 1px 1px 6px rgba(0,0,0,0.1); margin-bottom: 15px;">
                            <span style="background-color: #2ca02c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">PAGE {real_idx+1}</span>
                            <h5 style="margin-top: 10px; color: #333;">{step_name}</h5>
                            <div style="background-color: #f7f9fa; border: 1px dashed #ccc; height: 140px; margin-top: 8px; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #888;">
                                쿠팡 규격 가로 780px 비율 영역
                            </div>
                        </div>
                        """, unsafe_allow_html=True
                    )
            
            # 선택 버튼 배치
            if st.button(f"🎯 해당 8장 레이아웃 선택 후 자동생성 이동", key=f"btn_{title}", use_container_width=True):
                st.session_state["selected_bench_data"] = data
                st.success(f"[{title}] 적용 완료! 이제 1번 탭으로 가셔서 생성 버튼만 누르시면 됩니다.")
            st.markdown("<br><hr>", unsafe_allow_html=True)
