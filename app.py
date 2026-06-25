import streamlit as st
import base64
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =========================================================================
# ⚙️ [글로벌 환경 설정 및 시스템 유틸리티]
# =========================================================================
st.set_page_config(page_title="Daon 원화면 통합 빌더 v4.0", layout="wide")

# CSS를 이용해 가독성 및 UI 레이아웃 소폭 조정
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Malgun Gothic', sans-serif; }
    </style>
""", unsafe_allow_html=True)

def get_safe_font(font_size=24):
    """서버 환경 오류를 차단하는 안전 백업 폰트 시스템"""
    font_names = ["NanumGothic.ttf", "malgun.ttf", "Arial.ttf"]
    for name in font_names:
        try:
            return ImageFont.truetype(name, font_size)
        except Exception:
            continue
    return ImageFont.load_default()

def wrap_text(text, font, max_width=700):
    """가상 캔버스 안에서 자동 줄바꿈을 처리하는 헬퍼"""
    lines = []
    if not text:
        return lines
    words = text.split(" ")
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        try: w = font.getbbox(test_line)[2]
        except Exception: w = len(test_line) * 12
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# =========================================================================
# 🗂️ [세션 스테이트 메모리 고정 고리]
# =========================================================================
if "generated" not in st.session_state:
    st.session_state["generated"] = False
if "storyboard_data" not in st.session_state:
    st.session_state["storyboard_data"] = []
if "img_cache" not in st.session_state:
    st.session_state["img_cache"] = {}

# =========================================================================
# 🏗️ [단일 화면 레이아웃 정의: 좌측 제어 타워 | 우측 실시간 프리뷰]
# =========================================================================
col_input, col_preview = st.columns([1, 1.2], gap="large")

# -------------------------------------------------------------------------
# ⬅️ [좌측 영역] 상품 정보 입력 및 제어 타워
# -------------------------------------------------------------------------
with col_input:
    st.title("🍌 Daon 통합 빌더 v4.0")
    st.subheader("📝 1. 원천 기획 데이터 입력")
    
    # 대표님이 입력하시는 실제 상품 정보 칸
    prod_name = st.text_input("💎 원본 상품명", value="다온이네 밀봉 자석집게 6세트")
    prod_desc = st.text_area(
        "📝 상품 핵심 요약 및 설명", 
        value="자석집게로 냉장고 등 자석이 붙는 곳이면 어디든 간편하게 부착하여 보관 가능. 먹고남은 과자 봉투를 접어서 꽉 집어주세요.",
        height=100
    )
    
    st.markdown("---")
    st.subheader("📷 2. 이미지 에셋 일괄 업로드")
    uploaded_files = st.file_uploader("상세페이지에 매핑할 이미지들을 한 번에 선택하세요.", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    # 이미지 업로드 시 즉각 캐시 컨테이너에 저장
    if uploaded_files:
        for f in uploaded_files:
            st.session_state["img_cache"][f.name] = f.read()

    st.markdown("---")
    
    # [핵심] 생성 버튼 클릭 시, 고정된 값이 아니라 대표님이 위에 입력한 상품명/설명을 기반으로 8단 배열을 즉시 조립합니다.
    if st.button("🚀 입력 정보 기반 8단 상세페이지 생성", use_container_width=True, type="primary"):
        framework_templates = [
            {"num": 1, "tag": "Hero", "title": "👑 01. 메인 감성 타이틀", "suffix": "공간의 가치를 바꾸는 단 하나의 선택", "text": f"[공동구매/특가] {prod_name} 드디어 상륙!"},
            {"num": 2, "tag": "Pain", "title": "🚨 02. 문제 제기 후킹", "suffix": "아직도 눅눅해진 봉지 그대로 방치하십니까?", "text": f"기존 방식은 쉽게 풀리고 공기가 통해 금방 상해버립니다. {prod_name}(으)로 해결하세요."},
            {"num": 3, "tag": "Detail1", "title": "🛠️ 03. 초정밀 스펙 소구", "suffix": "강력한 고정력과 빈틈없는 완전 밀봉 성능", "text": f"{prod_desc} - 성능 시험을 모두 통과한 압도적 퀄리티를 자랑합니다."},
            {"num": 4, "tag": "Detail2", "title": "📐 04. 사용자 편의성", "suffix": "자석 설계로 보관과 사용을 동시에 편리하게", "text": "냉장고나 철제 벽면에 쓱 붙여두고 필요할 때마다 1초 만에 꺼내 쓰세요."},
            {"num": 5, "tag": "Safe", "title": "🛡️ 05. 내구성 및 안심 소재", "suffix": "오래 써도 변함없는 견고한 스프링 장력", "text": "싸구려 플라스틱과 비교 불가! 녹슬지 않는 내장 부품과 두터운 마감 처리를 완료했습니다."},
            {"num": 6, "tag": "Review", "title": "⭐️ 06. 실사용자 후기 조명", "suffix": "살까 말까 고민했던 시간이 아깝습니다!", "text": "'디자인도 예쁘고 자석이 있어서 잃어버릴 염려가 없네요. 주방 필수템 인정입니다.'"},
            {"num": 7, "tag": "Compare", "title": "📊 저가형 대비 격차 타격", "suffix": "쉽게 부러지는 일반 집게와의 비교를 거부합니다", "text": "다온(Daon)만의 독점 공정 퀄리티로 한 번 사면 평생 쓰는 주방의 품격을 완성합니다."},
            {"num": 8, "tag": "CTA", "title": "🛒 구매 촉구 엔딩 메시지", "suffix": "한정 수량 당일 출고 마감 임박", "text": "망설임은 배송만 늦출 뿐입니다. 지금 특가 혜택으로 스마트한 라이프를 시작하세요!"}
        ]
        
        st.session_state["storyboard_data"] = framework_templates
        st.session_state["generated"] = True
        st.success("🎯 우측에 대표님의 상품 맞춤형 8단 상세페이지가 실시간 빌드되었습니다!")

    # 다운로드 유틸리티 기능 배치
    if st.session_state["generated"]:
        st.markdown("---")
        st.subheader("💾 고화질 통이미지 다운로드 추출기")
        if st.button("🖼️ 1번 메인 카드 PNG 파일로 컴파일", use_container_width=True):
            font_m = get_safe_font(24)
            font_s = get_safe_font(16)
            card = st.session_state["storyboard_data"][0]
            
            img = Image.new("RGB", (780, 450), "#1e3a8a")
            draw = ImageDraw.Draw(img)
            draw.text((390, 50), f"{card['suffix']}", fill="#ffb703", font=font_m, anchor="mm")
            
            wrapped = wrap_text(card['text'], font_s, max_width=700)
            y_off = 150
            for ln in wrapped:
                draw.text((390, y_off), ln, fill="#ffffff", font=font_s, anchor="mm")
                y_off += 30
                
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="💾 1번 PNG 마스터 파일 다운로드 받기",
                data=buf.getvalue(),
                file_name=f"daon_master_card.png",
                mime="image/png",
                use_container_width=True
            )

# -------------------------------------------------------------------------
# ➡️ [우측 영역] 실시간 8장 상세페이지 위젯 + 이미지 매핑 및 시각화
# -------------------------------------------------------------------------
with col_preview:
    st.title("🖼️ 실시간 8단 편집 & 가로 780px 프리뷰")
    
    if not st.session_state["generated"]:
        st.info("💡 좌측에서 상품명과 설명을 작성하신 뒤 [🚀 입력 정보 기반 8단 상세페이지 생성] 버튼을 누르면 이 공간에 편집 매핑 레이아웃이 즉시 표시됩니다.")
    else:
        # 가용 가능한 업로드 파일 목록 구성
        img_options = ["선택 안 함"] + list(st.session_state["img_cache"].keys())
        
        # 8장의 카드를 루프 돌며 편집창과 프리뷰를 일체형으로 표기
        for idx, card in enumerate(st.session_state["storyboard_data"]):
            with st.container():
                # 개별 블록 테두리 구분선
                st.markdown(f"### {card['title']}")
                
                # 실시간 카피 문구 미세 편집 칸
                edited_suffix = st.text_input(f"소제목 수정 (카드 {card['num']})", value=card['suffix'], key=f"sub_{idx}")
                edited_text = st.text_area(f"본문 문구 수정 (카드 {card['num']})", value=card['text'], key=f"txt_{idx}", height=70)
                
                # 이미지 즉시 매핑 칸 (좌측에서 올린 이미지가 여기 실시간 리스트로 등장)
                chosen_img = st.selectbox(f"📷 0{card['num']} 장에 배치할 이미지 매핑", options=img_options, key=f"sel_img_{idx}")
                
                # HTML 780px 실시간 렌더링 엔진 작동
                img_html_render = '<div style="margin-top: 12px; height: 140px; background-color: #f1f5f9; border: 2px dashed #cbd5e1; display: flex; justify-content: center; align-items: center; color: #64748b; font-size: 13px; border-radius: 6px;">[📷 매핑 선택된 이미지가 없습니다]</div>'
                
                if chosen_img != "선택 안 함" and chosen_img in st.session_state["img_cache"]:
                    raw_bytes = st.session_state["img_cache"][chosen_img]
                    b64_str = base64.b64encode(raw_bytes).decode("utf-8")
                    img_html_render = f'<img src="data:image/png;base64,{b64_str}" style="width:100%; max-width:740px; border-radius:6px; margin-top:12px; border:1px solid #cbd5e1;" />'
                
                # 최종 쿠팡형 가로 780px 박스 아웃풋 디자인 실시간 표출
                html_card_box = f"""
                <div style="width: 100%; max-width: 780px; margin: 15px auto 40px auto; font-family: sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); overflow: hidden;">
                    <div style="background-color: #1e293b; color: #ffffff; padding: 10px 18px; font-size: 13px; font-weight: bold; letter-spacing: 0.5px;">
                        DAON CORE FRAMEWORK BLOCKED #0{card['num']}
                    </div>
                    <div style="padding: 22px;">
                        <h4 style="font-size: 18px; font-weight: bold; color: #1e3a8a; margin: 0 0 10px 0; border-bottom: 2px solid #f59e0b; padding-bottom: 5px;">{edited_suffix}</h4>
                        <div style="background-color: #fafafa; border-left: 4px solid #1e3a8a; padding: 12px; font-size: 14px; color: #334155; line-height: 1.6; white-space: pre-wrap;">{edited_text}</div>
                        {img_html_render}
                    </div>
                </div>
                """
                st.markdown(html_card_box, unsafe_allow_html=True)
                st.markdown("<hr style='border:1px dashed #e2e8f0; margin:30px 0;' />", unsafe_allow_html=True)
