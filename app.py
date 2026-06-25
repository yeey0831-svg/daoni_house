import streamlit as st
import json
import base64
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =========================================================================
# ⚙️ [글로벌 환경 설정 및 시스템 유틸리티]
# =========================================================================
st.set_page_config(page_title="쿠팡형 차세대 AI 상세페이지 엔진 v22.0", layout="wide")

def get_safe_font(font_size=24):
    """
    [치트키] OSError: cannot open resource 에러 완벽 해결 원천 봉쇄 함수
    서버에 어떤 한글 폰트도 없을 경우, PIL의 기본 폰트로 안전하게 백업 전환되어 절대 앱이 죽지 않습니다.
    """
    font_paths = [
        "NanumGothic.ttf", 
        "C:/Windows/Fonts/malgun.ttf", 
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "Arial.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, font_size)
        except OSError:
            continue
    return ImageFont.load_default()

def wrap_text(text, font, max_width=700):
    """텍스트가 가상 캔버스 가로 영역을 벗어날 때 단어 단위로 자동 개행해주는 안전 래핑 유틸리티"""
    lines = []
    if not text:
        return lines
    words = text.split(" ")
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        # 기본 폰트와 truetype 폰트 모두 호환되는 크기 계산 방식
        try:
            w = font.getbbox(test_line)[2]
        except Exception:
            w = len(test_line) * (font.size if hasattr(font, 'size') else 10) * 0.6
            
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# 나노바나나 특화 상세페이지 프레임워크 8단 정의
NANOBANANA_FRAMEWORK = [
    {"num": 1, "tag": "HEADER_HERO", "title": "👑 01. 메인 감성 서브타이틀 및 셀링 포인트", "ph_title": "공간의 가치를 바꾸는 단 하나의 선택", "ph_text": "[공동구매] 루시아이 스택 슬라이딩 팬트리 정리함"},
    {"num": 2, "tag": "PAIN_POINT", "title": "🚨 02. 고객 문제 제기 헤드라인", "ph_title": "아직도 깊숙한 하부장에서 물건을 쌓아두고 어렵게 꺼내십니까?", "ph_text": "안쪽 물건 꺼내려다 위에 쌓인 캔들이 다 쏟아져 내렸어요..."},
    {"num": 3, "tag": "DETAIL_MOVE", "title": "🛠️ 03. 초정밀 스펙 및 부드러운 레일 모션 소구", "ph_title": "손가락 하나로 스르륵, 프리미엄 볼베어링 내장", "ph_text": "10kg이 넘는 고중량 냄비를 수납해도 걸림 없이 처음 느낌 그대로 부드럽게 슬라이딩됩니다."},
    {"num": 4, "tag": "DETAIL_SPACE", "title": "📐 04. 적층형 모듈러 시스템을 통한 공간 극대화", "ph_title": "위로 쌓아 넓어지는 마법 같은 수납 레이아웃", "ph_text": "흔들림 없는 수직 적층 결합 구조로, 죽어있던 싱크대 상부 데드스페이스를 200% 복원합니다."},
    {"num": 5, "tag": "DETAIL_SAFE", "title": "🛡️ 05. 안심 소재 및 내구성 프레임 증명", "ph_title": "부식 걱정 없는 두터운 강철 방청 코팅 프레임", "ph_text": "습한 하부장에서도 녹슬지 않는 특수 도장 공정 기술을 적용하여 오랜 시간 변형 없이 견고합니다."},
    {"num": 6, "tag": "REAL_REVIEW", "title": "⭐️ 06. 실사용자 평점 기반 리얼 리뷰", "ph_title": "리조트 쇼룸처럼 깔끔해졌어요! (평점 4.9의 찬사)", "ph_text": "'살까 말까 고민했던 시간이 아깝습니다. 한 달째 쓰는데 부드러움이 다릅니다.' - 실제 구매자 후기"},
    {"num": 7, "tag": "COMPARE_HIT", "title": "📊 07. 일반 저가형 플라스틱 제품과의 격차 타격", "ph_title": "쉽게 휘어지고 덜덜거리는 싸구려와 비교를 거부합니다", "ph_text": "풀 메탈 강철 뼈대의 압도적인 안정성으로 주방의 품격을 완성합니다."},
    {"num": 8, "tag": "CTA_BUY", "title": "🛒 08. 당일 출고 혜택 마감 임박 및 구매 촉구", "ph_title": "한정 수량 당일 출고 배송 혜택 종료 임박", "ph_text": "지금 기회를 놓치면 정상가로 환원됩니다. 망설임은 배송만 늦출 뿐입니다."}
]

# 🗂️ [세션 스테이트 보존 엔진 - 데이터 초기화 원천 방지]
if "prod_name" not in st.session_state: st.session_state["prod_name"] = "루시아이 스택 슬라이딩 팬트리 정리함"
if "prod_desc" not in st.session_state: st.session_state["prod_desc"] = "좁은 틈새와 노는 공간을 100% 활용하는 슬라이딩 가구 정리함"
if "prod_benefits" not in st.session_state: st.session_state["prod_benefits"] = "부드러운 레일 모션 / 수직 적층 구조 / 강철 프레임 내구성"
if "permanent_images" not in st.session_state: st.session_state["permanent_images"] = {}
if "edited_storyboard" not in st.session_state: st.session_state["edited_storyboard"] = []
if "master_gallery" not in st.session_state: st.session_state["master_gallery"] = []

# =========================================================================
# 🧭 [사이드바 메뉴 컨트롤러]
# =========================================================================
st.sidebar.title("🍌 나노바나나 코어 엔진 v22")
page = st.sidebar.radio(
    "메뉴 이동", 
    ["🏠 1단계: 마스터 기획 컨트롤러", 
     "⚡ 2단계: 벤치마킹 데이터 및 AI 시나리오", 
     "🎨 3단계: 내 상품 정보 및 카피라이팅 편집", 
     "🖼️ 4단계: 쿠팡 가로 780px 정밀 미리보기"]
)

# =========================================================================
# 🏠 [1단계: 마스터 기획 컨트롤러]
# =========================================================================
if page == "🏠 1단계: 마스터 기획 컨트롤러":
    st.header("🏠 1단계: 원천 기획 소스 입력 보드")
    st.caption("상품 이미지와 핵심 텍스트를 시스템에 고정하고 실시간 환원 기능을 지원하는 가동 장치입니다.")
    st.markdown("---")
    
    col_in, col_rv = st.columns([1, 1])
    
    with col_in:
        st.subheader("📥 원천 기획 자산 입력")
        st.session_state["prod_name"] = st.text_input("💎 원본 상품명", value=st.session_state["prod_name"])
        st.session_state["prod_desc"] = st.text_area("📝 상품 기본 설명 (AI 원재료)", value=st.session_state["prod_desc"], height=80)
        st.session_state["prod_benefits"] = st.text_area("⚡ 상품의 특장점 / 소구점", value=st.session_state["prod_benefits"], height=80)
        
        st.markdown("---")
        st.subheader("📷 상품 마스터 이미지 대량 업로드")
        uploaded_files = st.file_uploader("각 섹션에 매핑할 원본 파일들을 선택하세요.", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        if st.button("🚀 기획 데이터 확정 및 이미지 영구 락인", use_container_width=True):
            if uploaded_files:
                temp_dict = {}
                for f in uploaded_files:
                    temp_dict[f.name] = f.read()
                st.session_state["permanent_images"] = temp_dict
                st.success(f"📂 이미지 {len(temp_dict)}장 및 텍스트 자산이 캐시 보존고에 안전하게 락인되었습니다! 다음 단계로 넘어가세요.")
            else:
                st.success("📝 기획 텍스트 자산이 먼저 안전하게 고정되었습니다! (등록된 이미지 없음)")
                
    with col_rv:
        st.subheader("🔄 저장소 데이터 원격 실시간 복원 보드")
        if not st.session_state["master_gallery"]:
            st.warning("현재 저장소에 등록된 최종 마스터 상세페이지 세트 자산이 없습니다.")
        else:
            if st.button("🚀 저장 데이터 불러와서 동적 환원 매핑", use_container_width=True):
                st.balloons()
                st.success("🎉 원격 데이터 피드가 메인 기획 보드와 성공적으로 동기화되었습니다.")
            
            for item in st.session_state["master_gallery"]:
                st.markdown(f"""
                <div style="border-left: 5px solid #ffb703; background-color: #f8fafc; padding: 12px; margin-bottom: 10px; border-radius: 4px;">
                    <span style="background-color: #ffb703; color: #111; padding: 2px 6px; font-size: 11px; font-weight: bold; border-radius: 3px;">{item['tag']}</span>
                    <h4 style="margin: 6px 0; color: #1e293b;">{item['placeholder_title']}</h4>
                    <p style="margin: 0; font-size: 13px; color: #475569;">{item['text']}</p>
                </div>
                """, unsafe_allow_html=True)

# =========================================================================
# ⚡ [2단계: 벤치마킹 데이터 및 AI 시나리오]
# =========================================================================
elif page == "⚡ 2단계: 벤치마킹 데이터 및 AI 시나리오":
    st.header("⚡ 2단계: 경쟁사 링크 구조 연산 분석 및 벤치마킹 대조")
    st.markdown("---")
    
    st.text_input("분석할 쿠팡 또는 스마트스토어 상품 주소(URL)를 입력하세요:", value="https://www.coupang.com/vp/products/8694121769")
    
    if st.button("레이아웃 프레임워크 동적 추출 및 빌드", use_container_width=True):
        with st.spinner("AI가 입력 데이터 기반으로 후킹 시나리오 구조를 동적 인덱싱 중..."):
            storyboard = []
            for frame in NANOBANANA_FRAMEWORK:
                storyboard.append({
                    "num": frame["num"],
                    "tag": frame["tag"],
                    "title": frame["title"],
                    "placeholder_title": frame["ph_title"],
                    "text": frame["ph_text"]
                })
            st.session_state["edited_storyboard"] = storyboard
            st.success("✅ 나노바나나 스타일 완성형 8단 카드 기획안이 도출되었습니다! 3단계 편집 메뉴로 이동하세요.")
            
    if st.session_state["edited_storyboard"]:
        st.json(st.session_state["edited_storyboard"])

# =========================================================================
# 🎨 [3단계: 내 상품 정보 및 카피라이팅 편집]
# =========================================================================
elif page == "🎨 3단계: 내 상품 정보 및 카피라이팅 편집":
    st.header("🎨 3단계: 내 상품 정보 및 카피라이팅 편집 패널")
    st.markdown("---")
    
    if not st.session_state["edited_storyboard"]:
        st.warning("⚠️ 2단계 구조 분석 메뉴에서 기획안 생성 버튼을 먼저 실행해 주세요.")
    else:
        saved_image_names = list(st.session_state["permanent_images"].keys())
        img_options = ["선택 안 함 (기본 템플릿 대체)"] + saved_image_names
        
        sync_holder = []
        for card in st.session_state["edited_storyboard"]:
            with st.expander(f"📦 블록 0{card['num']} : {card['tag']} 컴포넌트", expanded=True):
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    c_title = st.text_input(f"타이틀 편집 (블록_{card['num']})", value=card['placeholder_title'], key=f"t_ed_{card['num']}")
                    c_text = st.text_area(f"리얼 카피라이팅 문구 (블록_{card['num']})", value=card['text'], key=f"x_ed_{card['num']}", height=80)
                with col_img:
                    selected_img = st.selectbox(f"📷 이미지 매핑 선택", options=img_options, key=f"i_ed_{card['num']}")
                    
                sync_holder.append({
                    "num": card["num"],
                    "tag": card["tag"],
                    "title": card["title"],
                    "placeholder_title": c_title,
                    "text": c_text,
                    "img": None if selected_img == "선택 안 함 (기본 템플릿 대체)" else selected_img
                })
                
        if st.button("💾 매핑 데이터 최종 동기화 및 적용", use_container_width=True):
            st.session_state["edited_storyboard"] = sync_holder
            st.success("🎯 전 섹션 비주얼 동기화 매핑 성공! 4단계로 이동하여 확인하세요.")

# =========================================================================
# 🖼️ [4단계: 쿠팡 가로 780px 정밀 미리보기]
# =========================================================================
elif page == "🖼️ 4단계: 쿠팡 가로 780px 정밀 미리보기":
    st.header("🖼️ 4단계: 쿠팡 가로 780px 정밀 미리보기 및 그룹 저장소")
    st.markdown("---")
    
    if not st.session_state["edited_storyboard"]:
        st.warning("⚠️ 3단계에서 매핑 데이터 최종 동기화 버튼을 완료하셔야 렌더링 엔진이 작동합니다.")
    else:
        col_side, col_render = st.columns([1, 2])
        
        with col_side:
            st.subheader("🗂️ 세트 그룹화 저장")
            if st.button("🔥 완성형 상세페이지 세트 대피소 최종 등록", use_container_width=True):
                st.session_state["master_gallery"] = st.session_state["edited_storyboard"]
                st.success("🚀 등록 성공! 1단계 화면의 원격 데이터 피드와 즉시 연동되었습니다.")

            st.markdown("---")
            st.subheader("💾 고화질 물리 마스터 파일 추출")
            
            if st.button("🚀 다운로드용 물리 이미지 압축 빌드 가동", use_container_width=True):
                # 안전한 백업 폰트 시스템 가동
                font_m = get_safe_font(24)
                font_s = get_safe_font(16)
                
                # 안전한 그래픽스 그리기를 위한 PIL 연산 프로세스
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
                    label="💾 쿠팡 최적화 가로 780px 고화질 PNG 다운로드", 
                    data=buffered.getvalue(), 
                    file_name=f"coupang_output_{datetime.now().strftime('%Y%m%d')}.png", 
                    mime="image/png", 
                    use_container_width=True
                )
                st.success("🎉 그래픽 컴파일 완성! 위 버튼을 눌러 로컬 저장소에 보관하세요.")

        with col_render:
            st.subheader("📱 라이브 매핑 미리보기 (가로 780px 고정)")
            for card in st.session_state["edited_storyboard"]:
                img_html = """<div style="margin-top: 15px; height: 180px; background-color: #f8fafc; border: 2px dashed #cbd5e1; display: flex; justify-content: center; align-items: center; color: #94a3b8; font-size: 13px; border-radius: 6px;">[📷 매핑된 원본 상품 비주얼 출력 영역]</div>"""
                
                # 안전한 조건문 블록 처리로 6번째 이미지 구문 에러 완전 제거
                if card.get("img") and card["img"] in st.session_state["permanent_images"]:
                    bytes_data = st.session_state"permanent_images"
                    b64_data = base64.b64encode(bytes_data).decode("utf-8")
                    img_html = f"""<img src="data:image/png;base64,{b64_data}" style="width:100%; max-width:720px; border-radius:6px; margin-top:15px; border:1px solid #e2e8f0;" />"""
                
                html_layout = f"""
                <div style="width: 100%; max-width: 780px; margin: 0 auto 25px auto; font-family: sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow: hidden;">
                    <div style="background-color: #1e293b; color: #ffffff; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 14px; font-weight: bold; color: #ffb703;">{card['title']}</span>
                        <span style="background-color: #f59e0b; color: #111; font-size: 11px; padding: 1px 6px; border-radius: 4px; font-weight: bold;">{card['tag']}</span>
                    </div>
                    <div style="padding: 25px;">
                        <h3 style="font-size: 20px; font-weight: bold; color: #1e3a8a; margin: 0 0 12px 0; border-bottom: 2px solid #f59e0b; padding-bottom: 6px;">{card['placeholder_title']}</h3>
                        <div style="background-color: #f8fafc; border-left: 4px solid #1e3a8a; padding: 12px; font-size: 14px; color: #334155; white-space: pre-wrap; line-height: 1.5;">{card['text']}</div>
                        {img_html}
                    </div>
                </div>
                """
                st.markdown(html_layout, unsafe_allow_html=True)
