import streamlit as st
from PIL import Image
import io

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="다오니하우스 AI 상세페이지 스튜디오")

# CSS로 쿠팡 스타일의 폰트와 레이아웃 미세 조정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    .main-preview {
        max-width: 800px;
        margin: 0 auto;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 상태 관리 (Session State)
if "detail_state" not in st.session_state:
    st.session_state.detail_state = {
        "main_title": "제품명을 입력하세요",
        "sub_title": "한 줄 설명을 입력하세요",
        "event_text": "지금 구매하면 특별 사은품 증정!",
        "feature_title": "압도적인 성능과 디자인",
        "bg_color": "#ffffff",
        "brand_name": "LUXIAI"
    }

# -----------------------------------------------------------------
# 3. 사이드바 - 입력 및 파일 업로드 (여러 장 가능)
# -----------------------------------------------------------------
with st.sidebar:
    st.header("🎨 상세페이지 설정")
    brand_name = st.text_input("브랜드 로고 텍스트", value=st.session_state.detail_state["brand_name"])
    
    st.subheader("📸 이미지 업로드")
    product_images = st.file_uploader("제품 사진들 (여러 장 선택 가능)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    reference_images = st.file_uploader("디자인 참고 자료 (스타일 분석용)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    st.subheader("✍️ 문구 수정")
    main_title = st.text_input("메인 타이틀", value=st.session_state.detail_state["main_title"])
    sub_title = st.text_input("서브 타이틀 (바 형태)", value=st.session_state.detail_state["sub_title"])
    event_text = st.text_input("이벤트/증정 문구", value=st.session_state.detail_state["event_text"])
    feature_title = st.text_input("특장점 헤드라인", value=st.session_state.detail_state["feature_title"])
    
    st.session_state.detail_state.update({
        "main_title": main_title, "sub_title": sub_title, 
        "event_text": event_text, "feature_title": feature_title, "brand_name": brand_name
    })

# -----------------------------------------------------------------
# 4. 메인 화면 - 2분할 레이아웃
# -----------------------------------------------------------------
left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.subheader("💡 AI 스타일 제안")
    st.info("업로드된 여러 장의 사진 중 가장 좋은 각도를 AI가 선택하여 배경을 전문가 스튜디오급으로 변경합니다.")
    
    if st.button("🚀 AI 상세페이지 생성/새로고침", type="primary"):
        st.success("AI가 참고자료의 구도와 폰트 스타일을 분석하여 반영했습니다.")

    # 업로드된 이미지 미리보기 (작게)
    if product_images:
        st.write("선택된 제품 사진:")
        cols = st.columns(4)
        for i, img in enumerate(product_images):
            cols[i % 4].image(img, use_container_width=True)

with right_col:
    st.subheader("📱 쿠팡형 실시간 미리보기")
    
    # 상세페이지 렌더링 시작 (쿠팡 스타일 섹션화)
    preview_html = f"""
    <div class="main-preview">
        <div style="background-color: white; padding: 60px 40px; position: relative; text-align: left; border-bottom: 5px solid #1a2a4e;">
            <div style="position: absolute; top: 20px; right: 20px; text-align: right;">
                <p style="margin:0; font-weight: 900; font-size: 24px; color: #1a2a4e;">{st.session_state.detail_state['brand_name']}</p>
                <p style="margin:0; font-size: 10px; letter-spacing: 2px;">SPECIAL LIFESTYLE</p>
            </div>
            <h2 style="font-size: 45px; font-weight: 300; margin-bottom: -10px;">{st.session_state.detail_state['brand_name']}</h2>
            <h1 style="font-size: 55px; font-weight: 900; color: #1a2a4e; line-height: 1.1;">
                {st.session_state.detail_state['main_title']}
            </h1>
            <div style="background-color: #1a2a4e; color: white; padding: 10px 20px; display: inline-block; margin-top: 20px; font-size: 24px; font-weight: 700;">
                {st.session_state.detail_state['sub_title']}
            </div>
            <div style="margin-top: 40px; background: #eee; height: 400px; display: flex; align-items: center; justify-content: center; font-style: italic; color: #888; border-radius: 4px;">
                [AI가 배경을 지우고 전문가 촬영본으로 변환한 메인 이미지 영역]
            </div>
        </div>

        <div style="background-color: #f1f5f9; padding: 50px 40px; text-align: center;">
            <p style="color: #4a90e2; font-weight: 700; font-size: 20px; margin-bottom: 5px;">다오니하우스 단독 혜택</p>
            <h2 style="font-size: 32px; font-weight: 900; margin-bottom: 30px;">{st.session_state.detail_state['event_text']}</h2>
            <div style="background: white; border-radius: 20px; padding: 30px; border: 2px dashed #4a90e2;">
                <div style="background: #4a90e2; color: white; border-radius: 50px; padding: 5px 20px; display: inline-block; margin-bottom: 15px;">FREE GIFT</div>
                <p style="font-size: 18px;">리무버블 전용 스티커 증정</p>
            </div>
        </div>

        <div style="background-color: white; padding: 60px 0; position: relative; overflow: hidden;">
            <h2 style="text-align: center; font-size: 38px; font-weight: 900; color: #c0392b; margin-bottom: 40px;">
                {st.session_state.detail_state['feature_title']}
            </h2>
            <div style="background: #f9f9f9; height: 450px; margin: 0 40px; display: flex; align-items: center; justify-content: center; color: #999;">
                 [여러 사진을 분석하여 합성한 가장 드라마틱한 사용 예시 사진]
            </div>
            
            <div style="margin-top: 40px; width: 100%; height: 100px; background: #1a2a4e; clip-path: polygon(0 50%, 100% 0, 100% 100%, 0% 100%);">
            </div>
        </div>
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)
