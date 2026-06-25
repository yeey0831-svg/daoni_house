import streamlit as st
import base64
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =========================================================================
# ⚙️ [글로벌 환경 설정 및 시스템 유틸리티]
# =========================================================================
st.set_page_config(page_title="Daon 코어 상세페이지 엔진 v3.5", layout="wide")

def get_safe_font(font_size=24):
    """서버 환경에 관계없이 폰트 에러(OSError)를 원천 차단하는 안전 백업 시스템"""
    font_names = ["NanumGothic.ttf", "malgun.ttf", "Arial.ttf"]
    for name in font_names:
        try:
            return ImageFont.truetype(name, font_size)
        except Exception:
            continue
    return ImageFont.load_default()

def wrap_text(text, font, max_width=700):
    """가상 캔버스 안에서 텍스트가 삐져나가지 않도록 자동 줄바꿈을 해주는 유틸리티"""
    lines = []
    if not text:
        return lines
    words = text.split(" ")
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        try:
            w = font.getbbox(test_line)[2]
        except Exception:
            w = len(test_line) * 12
            
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Daon 브랜드 커스텀 8단 프레임워크 구조 고정
NANOBANANA_FRAMEWORK = [
    {"num": 1, "tag": "Hero", "title": "👑 01. 메인 감성 서브타이틀", "ph_title": "공간의 가치를 바꾸는 단 하나의 선택", "ph_text": "[공동구매] Daon 스택 슬라이딩 정리함"},
    {"num": 2, "tag": "Pain", "title": "🚨 02. 고객 문제 제기 헤드라인", "ph_title": "아직도 깊숙한 곳의 물건을 쌓아두고 어렵게 꺼내십니까?", "ph_text": "안쪽 물건 꺼내려다 위에 쌓인 물건들이 다 쏟아져 내렸어요..."},
    {"num": 3, "tag": "Detail1", "title": "🛠️ 03. 초정밀 스펙 소구", "ph_title": "손가락 하나로 스르륵, 프리미엄 볼베어링 레일 모션", "ph_text": "고중량 제품을 수납해도 걸림 없이 처음 느낌 그대로 부드럽게 슬라이딩됩니다."},
    {"num": 4, "tag": "Detail2", "title": "📐 04. 공간 극대화 시스템", "ph_title": "위로 쌓아 넓어지는 마법 같은 수납 레이아웃", "ph_text": "흔들림 없는 수직 적층 결합 구조로 데드스페이스를 200% 복원합니다."},
    {"num": 5, "tag": "Safe", "title": "🛡️ 05. 안심 소재 및 내구성", "ph_title": "부식 걱정 없는 두터운 강철 방청 코팅 프레임", "ph_text": "습한 환경에서도 녹슬지 않는 특수 도장 공정을 적용하여 오랜 시간 변형 없이 견고합니다."},
    {"num": 6, "tag": "Review", "title": "⭐️ 06. 실사용자 리얼 리뷰 후킹", "ph_title": "리조트 쇼룸처럼 깔끔해졌어요! (평점 4.9의 찬사)", "ph_text": "'살까 말까 고민했던 시간이 아깝습니다. 한 달째 쓰는데 튼튼함이 다릅니다.'"},
    {"num": 7, "tag": "Compare", "title": "📊 07. 일반 저가형 제품과의 격차 타격", "ph_title": "쉽게 휘어지고 덜덜거리는 싸구려와 비교를 거부합니다", "ph_text": "풀 메탈 강철 뼈대의 압도적인 안정성으로 주방과 거실의 품격을 완성합니다."},
    {"num": 8, "tag": "CTA", "title": "🛒 08. 구매 촉구 마감 메시지", "ph_title": "한정 수량 당일 출고 배송 혜택 종료 임박", "ph_text": "지금 기회를 놓치면 정상가로 환원됩니다. 망설임은 배송만 늦출 뿐입니다."}
]

# 🗂️ [세션 스테이트 보존 엔진 - 불시 초기화 방지 락인]
if "prod_name" not in st.session_state:
    st.session_state["prod_name"] = "Daon 멀티탭 정리함"
if "prod_desc" not in st.session_state:
    st.session_state["prod_desc"] = "지저분한 선들을 깔끔하게 숨겨주는 모던 정리함"
if "permanent_images" not in st.session_state:
    st.session_state["permanent_images"] = {}
if "edited_storyboard" not in st.session_state:
    st.session_state["edited_storyboard"] = []

# =========================================================================
# 🧭 [사이드바 메뉴 컨트롤러]
# =========================================================================
st.sidebar.title("🍌 Daon 코어 빌더 v3.5")
page = st.sidebar.radio(
    "작업 단계 선택", 
    ["🏠 1단계: 마스터 기획 입력", 
     "⚡ 2단계: AI 시나리오 빌드", 
     "🎨 3단계: 텍스트 및 이미지 매핑", 
     "🖼️ 4단계: 780px 정밀 미리보기 및 다운로드"]
)

# =========================================================================
# 🏠 1단계: 마스터 기획 입력
# =========================================================================
if page == "🏠 1단계: 마스터 기획 입력":
    st.header("🏠 1단계: 원천 기획 소스 입력")
    st.session_state["prod_name"] = st.text_input("💎 원본 상품명", value=st.session_state["prod_name"])
    st.session_state["prod_desc"] = st.text_area("📝 상품 기본 설명", value=st.session_state["prod_desc"], height=80)
    
    st.markdown("---")
    st.subheader("📷 마스터 이미지 대량 업로드")
    uploaded_files = st.file_uploader("사용할 원본 파일들을 선택하세요.", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("🚀 기획 데이터 및 이미지 캐시 저장", use_container_width=True):
        if uploaded_files:
            temp_dict = {}
            for f in uploaded_files:
                temp_dict[f.name] = f.read()
            st.session_state["permanent_images"] = temp_dict
            st.success(f"📂 이미지 {len(temp_dict)}장이 캐시 보존고에 저장되었습니다! 2단계로 이동하세요.")
        else:
            st.success("📝 텍스트 자산만 안전하게 저장되었습니다. (등록된 이미지 없음)")

# =========================================================================
# ⚡ 2단계: AI 시나리오 빌드
# =========================================================================
elif page == "⚡ 2단계: AI 시나리오 빌드":
    st.header("⚡ 2단계: 8단 시나리오 구조 생성")
    if st.button("기본 프레임워크 불러오기", use_container_width=True):
        storyboard = []
        for frame in NANOBANANA_FRAMEWORK:
            storyboard.append({
                "num": frame["num"],
                "tag": frame["tag"],
                "title": frame["title"],
                "placeholder_title": frame["ph_title"],
                "text": frame["ph_text"],
                "img": None
            })
        st.session_state["edited_storyboard"] = storyboard
        st.success("✅ 시나리오 구조가 성공적으로 동적 배치되었습니다! 3단계로 이동하세요.")
        
    if st.session_state["edited_storyboard"]:
        st.json([{"단계": s["num"], "타이틀": s["placeholder_title"]} for s in st.session_state["edited_storyboard"]])

# =========================================================================
# 🎨 3단계: 텍스트 및 이미지 매핑
# =========================================================================
elif page == "🎨 3단계: 텍스트 및 이미지 매핑":
    st.header("🎨 3단계: 상세 매핑 편집기")
    if not st.session_state["edited_storyboard"]:
        st.warning("⚠️ 2단계에서 프레임워크 빌드 버튼을 먼저 실행해 주세요.")
    else:
        saved_image_names = ["선택 안 함"] + list(st.session_state["permanent_images"].keys())
        sync_holder = []
        
        for card in st.session_state["edited_storyboard"]:
            with st.expander(f"📦 블록 0{card['num']} : {card['title']}", expanded=True):
                c_title = st.text_input(f"타이틀 편집 (블록_{card['num']})", value=card['placeholder_title'], key=f"t_{card['num']}")
                c_text = st.text_area(f"리얼 카피라이팅 문구 (블록_{card['num']})", value=card['text'], key=f"x_{card['num']}", height=80)
                
                if card.get("img") in saved_image_names:
                    default_idx = saved_image_names.index(card.get("img"))
                else:
                    default_idx = 0
                    
                selected_img = st.selectbox(f"📷 매핑할 이미지 선택", options=saved_image_names, index=default_idx, key=f"i_{card['num']}")
                
                sync_holder.append({
                    "num": card["num"],
                    "tag": card["tag"],
                    "title": card["title"],
                    "placeholder_title": c_title,
                    "text": c_text,
                    "img": None if selected_img == "선택 안 함" else selected_img
                })
                
        if st.button("💾 매핑 데이터 최종 동기화 및 적용", use_container_width=True):
            st.session_state["edited_storyboard"] = sync_holder
            st.success("🎯 전 섹션 비주얼 동기화 매핑 성공! 4단계로 이동하여 확인하세요.")

# =========================================================================
# 🖼️ 4단계: 780px 정밀 미리보기 및 다운로드
# =========================================================================
elif page == "🖼️ 4단계: 780px 정밀 미리보기 및 다운로드":
    st.header("🖼️ 4단계: 쿠팡 가로 780px 정밀 미리보기 및 마스터 파일 추출")
    if not st.session_state["edited_storyboard"]:
        st.warning("⚠️ 3단계에서 매핑 데이터 최종 동기화 버튼을 완료하셔야 렌더링 엔진이 작동합니다.")
    else:
        col_side, col_render = st.columns([1, 2])
        
        with col_side:
            st.subheader("💾 고화질 마스터 파일 추출")
            if st.button("🚀 샘플 1번 카드 PNG 다운로드 빌드", use_container_width=True):
                font_m = get_safe_font(24)
                font_s = get_safe_font(16)
                
                sample_card = st.session_state["edited_storyboard"][0]
                img = Image.new("RGB", (780, 450), "#1e3a8a")
                draw = ImageDraw.Draw(img)
                
                draw.text((390, 50), f"{sample_card['placeholder_title']}", fill="#ffb703", font=font_m, anchor="mm")
                wrapped_lines = wrap_text(sample_card['text'], font_s, max_width=700)
                y_offset = 150
                for line in wrapped_lines:
                    draw.text((390, y_offset), line, fill="#ffffff", font=font_s, anchor="mm")
                    y_offset += 30
                
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                
                st.download_button(
                    label="💾 PNG 마스터 파일 다운로드", 
                    data=buffered.getvalue(), 
                    file_name=f"daon_output_{datetime.now().strftime('%Y%m%d')}.png", 
                    mime="image/png", 
                    use_container_width=True
                )
                st.success("🎉 그래픽 컴파일 완수!")

        with col_render:
            st.subheader("📱 라이브 매핑 미리보기 (가로 780px 고정)")
            for card in st.session_state["edited_storyboard"]:
                img_html = '<div style="margin-top: 15px; height: 180px; background-color: #f8fafc; border: 2px dashed #cbd5e1; display: flex; justify-content: center; align-items: center; color: #94a3b8; font-size: 13px; border-radius: 6px;">[📷 이미지가 선택되지 않았습니다]</div>'
                
                chosen_img = card.get("img")
                if chosen_img and chosen_img in st.session_state["permanent_images"]:
                    bytes_data = st.session_state["permanent_images"][chosen_img]
                    b64_data = base64.b64encode(bytes_data).decode("utf-8")
                    img_html = f'<img src="data:image/png;base64,{b64_data}" style="width:100%; max-width:720px; border-radius:6px; margin-top:15px; border:1px solid #e2e8f0;" />'
                
                html_layout = f"""
                <div style="width: 100%; max-width: 780px; margin: 0 auto 25px auto; font-family: sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow: hidden;">
                    <div style="background-color: #1e293b; color: #ffffff; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; font-weight: bold; color: #ffb703;">{card['title']}</span>
                    </div>
                    <div style="padding: 25px;">
                        <h3 style="font-size: 20px; font-weight: bold; color: #1e3a8a; margin: 0 0 12px 0; border-bottom: 2px solid #f59e0b; padding-bottom: 6px;">{card['placeholder_title']}</h3>
                        <div style="background-color: #f8fafc; border-left: 4px solid #1e3a8a; padding: 12px; font-size: 14px; color: #334155; white-space: pre-wrap; line-height: 1.5;">{card['text']}</div>
                        {img_html}
                    </div>
                </div>
                """
                st.markdown(html_layout, unsafe_allow_html=True)
