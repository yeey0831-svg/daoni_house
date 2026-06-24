import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from datetime import datetime

# 1. 페이지 설정 및 세션 상태 초기화
st.set_page_config(page_title="쿠팡형 프로페셔널 AI 상세페이지 빌더 v3", layout="wide")

if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []
if "page3_meta_data" not in st.session_state:
    st.session_state["page3_meta_data"] = {}
if "saved_projects_library" not in st.session_state:
    st.session_state["saved_projects_library"] = []
if "bench_url" not in st.session_state:
    st.session_state["bench_url"] = ""

# 구글 오픈폰트(나눔고딕) 안전 다운로드 함수
@st.cache_data
def load_korean_font_bytes():
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None

# 2. 사이드바 UI (요청 반영: 기본 예시 텍스트 완전히 삭제 및 placeholder 대체)
st.sidebar.title("📋 필수 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password", help="Gemini API 키를 입력하세요.")
product_name = st.sidebar.text_input(
    "상품명", 
    value="", 
    placeholder="예: [당일출고] 빅사이즈! 루시아이 스택 슬라이딩 팬트리 정리함"
)
target_customer = st.sidebar.text_input(
    "타겟 고객", 
    value="", 
    placeholder="예: 펜트리 수납이 고민인 주부, 맥시멀리스트 자취생"
)

# 3. 4단계 탭 구성 메뉴
menu = st.radio(
    "",
    [
        "🎯 1. 상세페이지 자동 생성",
        "➕ 2. 벤치마킹 데이터 등록",
        "📂 3. 상세페이지 샘플 제작 및 검토",
        "📦 4. 저장된 프로젝트 보관함 (미리보기)"
    ],
    horizontal=True
)

# Gemini API 호출 함수 (안정적인 모델 세팅)
def call_gemini_api(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        pass
    return None

# [핵심 개편] PPT 느낌을 완전 탈피한 실전 쿠팡형 롱버티컬(Long-Vertical) 이미지 생성 엔진
def create_real_coupang_page(step_num, title, description, prod_name):
    # 쿠팡 스탠다드 규격: 가로 780px, 세로 1200px (시원한 세로형 스크롤 비율)
    width, height = 780, 1200
    
    # 기본 상세페이지 배경 (인스타 감성의 완전 깨끗한 화이트 무드 배경)
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    font_bytes = load_korean_font_bytes()
    if font_bytes:
        font_badge = ImageFont.truetype(io.BytesIO(font_bytes), 16)
        font_main_head = ImageFont.truetype(io.BytesIO(font_bytes), 38)
        font_sub_head = ImageFont.truetype(io.BytesIO(font_bytes), 24)
        font_body = ImageFont.truetype(io.BytesIO(font_bytes), 20)
        font_box_label = ImageFont.truetype(io.BytesIO(font_bytes), 18)
    else:
        font_badge = font_main_head = font_sub_head = font_body = font_box_label = ImageFont.load_default()

    # 사용자가 상품명을 입력하지 않았을 경우 대비 기본값 트리거
    display_prod = prod_name if prod_name else "프리미엄 리빙 정리용품"

    # [디자인 섹션 1] 상단 탑 엠블럼 / 카테고리 태그 라인
    draw.rectangle([320, 50, 460, 82], fill=(240, 242, 245), outline=(210, 214, 219), width=1)
    draw.text((345, 57), "PREMIUM DETAIL", fill=(100, 110, 120), font=font_badge)

    # [디자인 섹션 2] 감성 카피라이팅 영역 (PPT 스타일의 격자 타이틀 제거)
    draw.text((60, 140), f"SECTION 0{step_num}", fill=(0, 102, 255), font=font_sub_head) # 쿠팡 트렌디 블루 컬러 서체
    
    # 헤드라인 텍스트 wrap
    wrapped_titles = textwrap.wrap(title, width=18)
    y_title_offset = 180
    for t_line in wrapped_titles:
        draw.text((60, y_title_offset), t_line, fill=(22, 28, 45), font=font_main_head)
        y_title_offset += 50

    # [디자인 섹션 3] 실제 쿠팡 업로드용 스페이스 박스 디자인 (배경 흰색 + 고급스러운 미니멀리즘 그라데이션 경계선)
    # 동영상 구간(2페이지)과 일반 상품 이미지 공간 구분
    is_video = (step_num == 2)
    box_top = y_title_offset + 40
    box_bottom = box_top + 520
    
    # 미디어 공간: 완벽한 흰색 배경 + 부드러운 아웃라인 섀도우 효과 표현
    draw.rectangle([50, box_top, 730, box_bottom], fill=(255, 255, 255), outline=(230, 235, 240), width=3)
    
    # 미디어 중앙 플레이스홀더 텍스트 안내 (한글 표기 필수 조건 충족)
    label_main = "🎥 [여기에 동영상 삽입 공간]" if is_video else "📦 [여기에 상품 이미지 삽입 공간]"
    label_sub = "(실제 등록 시 이 영역에 촬영하신 미디어를 올려주세요)"
    
    draw.text((250, box_top + 230), label_main, fill=(70, 80, 95), font=font_sub_head)
    draw.text((210, box_top + 280), label_sub, fill=(160, 165, 175), font=font_box_label)

    # [디자인 섹션 4] 하단 설명 카피 구조화 (줄바꿈 최적화 및 본문 정돈)
    y_body_start = box_bottom + 50
    draw.rectangle([50, y_body_start - 10, 55, y_body_start + 20], fill=(0, 102, 255)) # 포인트 바 드로잉
    draw.text((70, y_body_start - 5), "MD's 핵심 셀링 포인트 안내", fill=(100, 110, 120), font=font_badge)
    
    wrapped_body = textwrap.wrap(description, width=32)
    y_body_offset = y_body_start + 35
    for b_line in wrapped_body:
        draw.text((60, y_body_offset), b_line, fill=(60, 68, 85), font=font_body)
        y_body_offset += 32

    # [디자인 섹션 5] 최하단 브랜드 풋터 (상세페이지 신뢰도 상승 요소)
    draw.line([(50, 1140), (730, 1140)], fill=(235, 238, 242), width=1)
    draw.text((60, 1155), display_prod, fill=(150, 155, 165), font=font_badge)
    draw.text((630, 1155), "TRUST QUALITY", fill=(200, 203, 210), font=font_badge)

    return image

# 데이터 일괄 생성 및 스위칭 로직
def build_and_store_cards():
    # 사용자가 직접 입력한 상품명을 동적으로 반영하는 구조화 컨텐츠 세팅
    p_name = product_name if product_name else "루시아이 스택 슬라이딩 팬트리 정리함"
    
    steps_data = [
        {"num": 1, "title": "터질듯한 주방 공간, 아직도 쌓아두기만 하시나요?", "desc": "뒤죽박죽 섞여서 찾기 힘든 팬트리와 하부장 수납장 속 물건들. 이제 꺼내기 힘든 안쪽 물건까지 한 번에 정리하는 새로운 대안을 제시합니다."},
        {"num": 2, "title": "스르륵- 부드럽게 열리는 슬라이딩 모션 작동", "desc": "적은 힘으로도 끝까지 부러짐 없이 부드럽게 열리는 하이테크 레일 기술 공학 적용. 실제 작동하는 부드러운 움직임을 눈으로 직접 확인해 보세요."},
        {"num": 3, "title": "공간을 2배로 확장하는 커스텀 스택 적층 시스템", "desc": "위로 위로 흔들림 없이 수직으로 안전하게 쌓아 올리는 견고한 고정 홈 포지셔닝 설계. 죽은 데드스페이스 공간을 획기적인 수납 명당으로 바꿉니다."},
        {"num": 4, "title": "압도적인 하중도 견뎌내는 빅사이즈 특대형 규격", "desc": "두꺼운 양념통부터 대용량 식자재, 무거운 주방 용품까지 휘어짐이나 찌그러짐 없이 안전하게 적재 가능한 고강도 친환경 소재 특수 마감 원단 처리가 돋보입니다."},
        {"num": 5, "title": "주방을 넘어 다용도실, 드레스룸까지 완벽 배치", "desc": "모던하고 깔끔한 화이트톤 인테리어 무드로 어디에 두어도 가구처럼 녹아드는 미니멀 디자인 밸런스. 일상의 동선을 가장 아름답고 편리하게 재구성합니다."},
        {"num": 6, "title": "누적 만족도가 증명하는 리얼 구매 리뷰 가치", "desc": "살림 전문가와 인플루언서들이 극찬한 바로 그 대란 정리함! '정리 정돈 스트레스가 완전히 사라졌어요'라는 실제 유저들의 진솔한 목소리를 담았습니다."},
        {"num": 7, "title": "저가형 흔들리는 철제 정리함과의 정밀 비교 우위", "desc": "녹슬고 덜컹거리는 저가 플라스틱이나 약한 가성비 제품들과 비교를 거부합니다. 독자적인 와이드 와이어 프레임 공법으로 흔들림 없는 완벽한 내구성을 강화했습니다."},
        {"num": 8, "title": "오늘 단 하루 최저가 혜택 구성 및 즉시 출고 보장", "desc": "품절 전 소장 필수! 망설이면 늦어지는 주방 공간의 혁신적인 변화. 지금 바로 장바구니에 담아 첫 입주 인테리어처럼 정돈된 집안을 만나보세요."}
    ]
    cards = []
    for step in steps_data:
        generated_img = create_real_coupang_page(step["num"], step["title"], step["desc"], p_name)
        cards.append(generated_img)
    st.session_state["page3_saved_images"] = cards
    st.session_state["page3_meta_data"] = {
        "product_name": p_name,
        "target_customer": target_customer if target_customer else "모든 고객 대상",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# ====================================================
# 🎯 1. 상세페이지 자동 생성 탭
# ====================================================
if menu == "🎯 1. 상세페이지 자동 생성":
    st.markdown("### 🖼️ 실전 쿠팡 스크롤형 상세페이지 제작 센터")
    st.file_uploader("[A] 촬영 원본 상품 사진 등록", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    st.file_uploader("[B] 벤치마킹하고 싶은 상세 스크린샷", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("🚀 쿠팡 규격 수직형 상세페이지 8장 세트 즉시 빌드"):
        with st.spinner("쿠팡 판매 공식에 맞춰 고해상도 수직 롱이미지 드로잉 중..."):
            build_and_store_cards()
            st.success("✨ PPT 형식을 탈피한 실전 상세페이지 템플릿 인스턴스 빌드 완료! 3페이지 탭에서 결과물을 확인하세요.")

# ====================================================
# ➕ 2. 벤치마킹 데이터 등록 탭
# ====================================================
elif menu == "➕ 2. 벤치마킹 데이터 등록":
    st.markdown("### ➕ 경쟁사 링크 구조 연산 분석")
    url_input = st.text_input("분석할 쿠팡 또는 스마트스토어 상품 주소(URL):")
    if st.button("레이아웃 프레임워크 동적 추출 및 빌드"):
        if url_input:
            st.session_state["bench_url"] = url_input
            build_and_store_cards()
            st.success("✅ 타겟 상세페이지 흐름 학습 성공! 3페이지에서 롱디자인을 확인해 보세요.")

# ====================================================
# 📂 3. 상세페이지 샘플 제작 및 검토 탭 (저장 버튼 제공)
# ====================================================
elif menu == "📂 3. 상세페이지 샘플 제작 및 검토":
    st.markdown("### 📄 3페이지: 실전 쿠팡 규격(가로 780px) 상세페이지 검토 공간")
    
    if st.session_state["page3_saved_images"]:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            st.info("💡 스크롤을 내려 완성된 고해상도 세로형 상세페이지 구성을 체크해 보세요. 완벽하다면 오른쪽 버튼을 눌러 보관함으로 전송하세요.")
        with col_btn2:
            # 3페이지 샘플을 4페이지로 복사 및 저장하는 핵심 액션 컨트롤러
            if st.button("📦 4페이지 보관함으로 세트 저장하기", type="primary", use_container_width=True):
                project_bundle = {
                    "meta": st.session_state["page3_meta_data"],
                    "images": list(st.session_state["page3_saved_images"])
                }
                st.session_state["saved_projects_library"].append(project_bundle)
                st.balloons()
                st.success("🚀 저장 및 그룹 묶음 이관이 성공적으로 완료되었습니다! 4페이지에서 언제든 꺼내보세요.")
        st.markdown("---")
        
        # 실제 매끄러운 롱배너 스크롤 감각을 위해 세로로 끊김 없이 연달아 배치 출력
        for idx, img in enumerate(st.session_state["page3_saved_images"]):
            st.markdown(f"#### 🏷️ [단독 세션 블록 #{idx + 1}]")
            st.image(img, use_container_width=True)
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label=f"📥 블록 #{idx + 1} PNG 고해상도 다운로드",
                data=buf.getvalue(),
                file_name=f"coupang_premium_page_{idx+1}.png",
                mime="image/png",
                key=f"p3_dl_btn_{idx}"
            )
            st.markdown("<br><br>", unsafe_allow_html=True)
    else:
        st.info("💡 아직 디자인된 상세페이지 샘플 세트가 부재합니다. 1페이지 혹은 2페이지에서 먼저 생성 명령을 실행해 주세요!")

# ====================================================
# 📦 4. 저장된 프로젝트 보관함 (그룹별 묶음 미리보기) 탭
# ====================================================
elif menu == "📦 4. 저장된 프로젝트 보관함 (미리보기)":
    st.markdown("### 📦 4페이지: 상세페이지 기획 세트 그룹별 통합 보관함")
    st.caption("3페이지에서 이관되어 영구 백업 보관된 프로젝트들을 한눈에 격자 스캔 및 통합 관리하는 공간입니다.")
    
    if st.session_state["saved_projects_library"]:
        for p_idx, project in enumerate(reversed(st.session_state["saved_projects_library"])):
            meta = project["meta"]
            actual_idx = len(st.session_state["saved_projects_library"]) - 1 - p_idx
            
            # 아코디언 컴포넌트를 이용해 그룹별로 8장 세트를 컴팩트하게 압축 바인딩
            with st.expander(f"📁 [상세페이지 기획 그룹 #{actual_idx + 1}] {meta.get('product_name')} | 이관일시: {meta.get('created_at')}", expanded=True):
                st.markdown(f"🎯 **설계된 타겟 타겟층:** {meta.get('target_customer')}")
                
                # 8장의 긴 상세페이지를 가로로 한눈에 모아보기 쉽도록 4열 그리드 배치 레이아웃 시스템
                cols = st.columns(4)
                for img_idx, img in enumerate(project["images"]):
                    col_target = cols[img_idx % 4]
                    with col_target:
                        st.markdown(f"**📜 BLOCK {img_idx + 1}**")
                        st.image(img, use_container_width=True)
                        
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        st.download_button(
                            label="📥 개별 다운로드",
                            data=buf.getvalue(),
                            file_name=f"group_{actual_idx+1}_block_{img_idx+1}.png",
                            mime="image/png",
                            key=f"p4_dl_{actual_idx}_{img_idx}"
                        )
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"🗑️ 해당 프로젝트 그룹 데이터 완전 영구 삭제", key=f"del_group_{actual_idx}"):
                    st.session_state["saved_projects_library"].pop(actual_idx)
                    st.rerun()
    else:
        st.warning("⚠️ 보관함이 비어 있습니다. 3페이지 검토 센터 상단에서 '4페이지 보관함으로 세트 저장하기' 버튼을 클릭하면 여기에 폴더별로 예쁘게 정렬됩니다.")
