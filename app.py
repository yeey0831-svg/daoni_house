import streamlit as st
import json
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# 1. 페이지 초기 설정 (와이드 레이아웃)
st.set_page_config(page_title="쿠팡형 넥스트 AI 상세페이지 빌더 v22.0", layout="wide")

# 2. 안전한 폰트 로더 함수 (OSError 방지 핵심)
def get_safe_font(font_size=20):
    """
    서버 환경에 무관하게 폰트 오픈 에러(OSError)를 원천 차단하는 안전 함수입니다.
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
    # 모든 경로에 폰트가 없을 경우 시스템 기본 폰트 반환
    return ImageFont.load_default()

# 3. 데이터베이스 역할을 하는 가상 JSON 데이터 정의 (세션 관리)
if "detail_json" not in st.session_state:
    st.session_state["detail_json"] = {
        "template_id": "bench_001",
        "template_name": "쿠팡 상위 1% 슬라이딩 정리함 구조",
        "blocks": [
            {
                "id": "block_1",
                "type": "header_hero",
                "content": {
                    "sub_title": "공간의 가치를 바꾸는 단 하나의 선택",
                    "main_title": "[당일출고] 루시아이 스택 슬라이딩 팬트리 정리함"
                }
            },
            {
                "id": "block_2",
                "type": "pain_point",
                "content": {
                    "title": "아직도 깊숙한 하부장에서 물건을 쌓아두고 어렵게 꺼내십니까?",
                    "quote": "안쪽 물건 꺼내려다 위에 쌓인 캔들이 다 쏟아져 내렸어요..."
                }
            }
        ]
    }

# 4. 메인 대시보드 UI 레이아웃
st.title("🎯 쿠팡형 차세대 AI 상세페이지 엔진 v22.0")
st.caption("배포 서버 환경에서의 OSError 및 폰트 컴파일 오류를 완벽하게 수정한 마스터 빌드입니다.")
st.markdown("---")

col_edit, col_preview = st.columns([1, 1])

# =========================================================================
# 📝 [왼쪽 화면: 데이터 매핑 및 AI 카피라이팅 편집기]
# =========================================================================
with col_edit:
    st.header("📝 3단계: 내 상품 정보 및 카피라이팅 편집")
    st.write("JSON 구조화 데이터에 맞춰 텍스트 데이터를 수정 및 매핑합니다.")
    
    updated_blocks = []
    
    for idx, block in enumerate(st.session_state["detail_json"]["blocks"]):
        b_type = block["type"]
        b_id = block["id"]
        
        with st.expander(f"📦 블록 {idx+1} : {b_type.upper()} 컴포넌트 레이아웃", expanded=True):
            if b_type == "header_hero":
                sub_t = st.text_input(f"상단 감성 서브타이틀 ({b_id})", value=block["content"]["sub_title"])
                main_t = st.text_area(f"메인 셀링 상품명 ({b_id})", value=block["content"]["main_title"])
                updated_blocks.append({
                    "id": b_id, "type": b_type, 
                    "content": {"sub_title": sub_t, "main_title": main_t}
                })
                
            elif b_type == "pain_point":
                p_title = st.text_area(f"고객 문제 제기 헤드라인 ({b_id})", value=block["content"]["title"])
                p_quote = st.text_input(f"리얼 고객 인용구 ({b_id})", value=block["content"]["quote"])
                updated_blocks.append({
                    "id": b_id, "type": b_type, 
                    "content": {"title": p_title, "quote": p_quote}
                })

    if st.button("🔄 매핑 데이터 최종 동기화 및 적용", use_container_width=True):
        st.session_state["detail_json"]["blocks"] = updated_blocks
        st.success("JSON 구조화 템플릿에 데이터가 성공적으로 매핑되었습니다!")

    st.markdown("### 🗂️ 현재 구조화 데이터 상태 (JSON Schema)")
    st.json(st.session_state["detail_json"])

# =========================================================================
# 🖼️ [오른쪽 화면: 가로 780px 웹 표준 기반 고화질 실시간 프리뷰]
# =========================================================================
with col_preview:
    st.header("🖼️ 4단계: 쿠팡 가로 780px 정밀 미리보기")
    st.write("클라우드 환경에서 의존성 없이 가장 가볍고 정확하게 화면을 그리는 렌더링 결과입니다.")
    
    # 780px 쿠팡 표준 규격에 맞추어 완성형 HTML 컴포넌트 실시간 드로잉
    html_preview = """
    <div style="width: 100%; max-width: 780px; margin: 0 auto; font-family: sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
    """
    
    for block in st.session_state["detail_json"]["blocks"]:
        b_type = block["type"]
        content = block["content"]
        
        if b_type == "header_hero":
            html_preview += f"""
            <div style="background-color: #1a233a; color: #ffffff; padding: 60px 40px; text-align: center;">
                <span style="color: #ffb703; font-weight: bold; font-size: 14px; letter-spacing: 2px;">PREMIUM AI DESIGN</span>
                <p style="color: #cbd5e1; font-size: 18px; margin: 15px 0 10px 0;">{content.get('sub_title', '')}</p>
                <h1 style="font-size: 28px; font-weight: 800; margin: 0; line-height: 1.4; word-break: keep-all;">{content.get('main_title', '')}</h1>
            </div>
            """
        elif b_type == "pain_point":
            html_preview += f"""
            <div style="background-color: #111111; color: #ffffff; padding: 50px 40px; text-align: center;">
                <div style="font-size: 32px; margin-bottom: 10px;">🚨</div>
                <h2 style="font-size: 20px; font-weight: 700; color: #f3f4f6; margin: 0 0 25px 0; line-height: 1.5; word-break: keep-all;">{content.get('title', '')}</h2>
                <div style="background-color: #222222; border-left: 4px solid #ef4444; padding: 15px 20px; text-align: left; font-size: 16px; color: #f87171; font-weight: bold;">
                    “ {content.get('quote', '')} ”
                </div>
            </div>
            """
            
    html_preview += "</div>"
    
    # 샌드박스 내부 컴포넌트 UI 브라우저 출력
    st.markdown(html_preview, unsafe_allow_html=True)
    st.markdown("---")
    
    # 다운로드용 고해상도 백엔드 이미지 생성 연산 (PIL 보완 결합형)
    if st.button("🚀 다운로드용 고화질 마스터 이미지 렌더링 시작"):
        # 전체 레이아웃 크기 동적 계산 (가로 780px 고정)
        total_height = 400 * len(st.session_state["detail_json"]["blocks"])
        img = Image.new("RGB", (780, total_height), "#ffffff")
        draw = ImageDraw.Draw(img)
        
        current_y = 0
        font_main = get_safe_font(28)
        font_sub = get_safe_font(18)
        
        for block in st.session_state["detail_json"]["blocks"]:
            b_type = block["type"]
            content = block["content"]
            
            if b_type == "header_hero":
                # 상단 배경 드로잉
                draw.rectangle([0, current_y, 780, current_y + 400], fill="#1a233a")
                draw.text((390, current_y + 130), content.get('sub_title', ''), fill="#cbd5e1", font=font_sub, anchor="mm")
                draw.text((390, current_y + 200), content.get('main_title', ''), fill="#ffffff", font=font_main, anchor="mm")
                current_y += 400
            elif b_type == "pain_point":
                draw.rectangle([0, current_y, 780, current_y + 400], fill="#111111")
                draw.text((390, current_y + 120), "🚨 문제 제기", fill="#ef4444", font=font_sub, anchor="mm")
                draw.text((390, current_y + 190), content.get('title', '')[:25], fill="#ffffff", font=font_main, anchor="mm")
                draw.text((390, current_y + 240), content.get('title', '')[25:], fill="#ffffff", font=font_main, anchor="mm")
                current_y += 400
                
        # 다운로드 버퍼 바인딩
        img_path = "coupang_master_fixed.png"
        img.save(img_path, "PNG")
        
        with open(img_path, "rb") as file:
            st.download_button(
                label="💾 완성형 고화질 원본 PNG 다운로드",
                data=file,
                file_name=f"coupang_ai_page_{datetime.now().strftime('%Y%m%d')}.png",
                mime="image/png",
                use_container_width=True
            )
        st.success("고화질 이미지 컴파일 렌더링이 완료되었습니다! 위 버튼을 눌러 저장하세요.")
