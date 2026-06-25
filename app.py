import streamlit as st

# 페이지 레이아웃을 넓게 설정
st.set_page_config(layout="wide")

st.title("🛍️ AI 상품 상세페이지 생성기 (코딩 파트너 버전)")
st.caption("템플릿 기반 상세페이지 생성 및 실시간 편집 스튜디오")

# 1. 초기 상태 변수(session_state) 설정 (실시간 편집의 핵심)
if "generated_data" not in st.session_state:
    st.session_state.generated_data = {
        "title": "",
        "description": "",
        "bg_color": "#ffffff",
        "image_status": "default"
    }

if "is_generated" not in st.session_state:
    st.session_state.is_generated = False

# 가상의 템플릿 데이터 데이터베이스 (추후 JSON 파일 등으로 확장 가능)
TEMPLATES = {
    "심플 모던 스튜디오": {"bg": "#f8f9fa", "text_align": "center"},
    "내추럴 감성 가든": {"bg": "#f1f3f0", "text_align": "left"},
    "럭셔리 다크룸": {"bg": "#1a1a1a", "text_align": "center"}
}

# -----------------------------------------------------------------
# 2. UI 레이아웃 분할 (좌측: 입력 및 제어 / 우측: 결과 미리보기 및 편집)
# -----------------------------------------------------------------
left_col, right_col = st.columns([1, 1])

# --- [좌측 열] 데이터 입력 및 생성 요청 ---
with left_col:
    st.header("📋 상품 정보 입력")
    
    # 템플릿 선택
    selected_template = st.selectbox("디자인 템플릿 선택", list(TEMPLATES.keys()))
    
    # 데이터 입력 수집
    uploaded_file = st.file_uploader("상품 원본 이미지 첨부", type=["png", "jpg", "jpeg"])
    product_name = st.text_input("상품 이름", placeholder="예: 유기농 바나나 칩")
    product_desc = st.text_area("상품 설명", placeholder="예: 인공 첨가물 없이 자연 그대로 건조하여 바삭하고 건강한 간식입니다.")
    
    # 생성 버튼
    if st.button("✨ 전문가 스타일 상세페이지 생성", type="primary"):
        if uploaded_file and product_name:
            with st.spinner("AI가 이미지를 고품질로 변환하고 카피라이팅을 배치 중입니다..."):
                # [참고] 이 부분에 추후 Gemini API와 이미지 변환 API 연동 코드가 들어갑니다.
                # 지금은 입력받은 데이터를 바탕으로 상태를 업데이트하는 로직을 구현합니다.
                st.session_state.generated_data["title"] = f"🌟 [Premium] {product_name}"
                st.session_state.generated_data["description"] = f"진심을 담아 만들었습니다.\n\n{product_desc}\n\n지금 바로 만나보세요."
                st.session_state.generated_data["bg_color"] = TEMPLATES[selected_template]["bg"]
                st.session_state.generated_data["image_status"] = "transformed" # 변환 완료 상태 표시
                st.session_state.is_generated = True
                st.success("상세페이지가 생성되었습니다! 우측에서 확인하고 수정하세요.")
        else:
            st.error("상품 이미지와 이름을 모두 입력해 주세요.")

# --- [우측 열] 실시간 미리보기 및 세부 수정 ---
with right_col:
    st.header("🖼️ 상세페이지 미리보기 & 실시간 편집")
    
    if st.session_state.is_generated:
        # 실시간 수정을 위한 편집 UI (Expander 폼으로 깔끔하게 정리)
        with st.expander("✏️ 원하는 내용 직접 수정하기", expanded=True):
            edit_title = st.text_input("타이틀 문구 수정", value=st.session_state.generated_data["title"])
            edit_desc = st.text_area("본문 문구 수정", value=st.session_state.generated_data["description"])
            edit_bg = st.color_picker("배경색 변경", value=st.session_state.generated_data["bg_color"])
            
            # 입력폼의 변경사항을 session_state에 실시간 반영
            st.session_state.generated_data["title"] = edit_title
            st.session_state.generated_data["description"] = edit_desc
            st.session_state.generated_data["bg_color"] = edit_bg

        # 상세페이지 실제 렌더링 영역 (HTML/CSS 스타일 적용)
        st.markdown(f"""
            <div style="background-color: {st.session_state.generated_data['bg_color']}; padding: 40px; border-radius: 10px; border: 1px solid #ddd; text-align: center; color: {'#ffffff' if st.session_state.generated_data['bg_color'] == '#1a1a1a' else '#333333'};">
                <p style="font-size: 14px; color: #888;">BRAND STORY</p>
                <h1 style="margin-bottom: 20px;">{st.session_state.generated_data['title']}</h1>
                <div style="margin: 30px 0; background: #eaeaea; padding: 50px; border-radius: 8px; color: #555;">
                    📸 <b>[스튜디오 촬영본 변환 이미지 영역]</b><br>
                    (추후 이곳에 AI가 변환한 전문가 스타일의 상품 이미지가 표시됩니다)
                </div>
                <div style="white-space: pre-wrap; line-height: 1.6; font-size: 16px;">
                    {st.session_state.generated_data['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 다운로드 혹은 저장 버튼
        st.button("💾 최종 완성본 깃허브/DB 저장")
    else:
        st.info("좌측에서 정보를 입력하고 생성 버튼을 누르면, 이곳에 편집 가능한 상세페이지가 나타납니다.")
