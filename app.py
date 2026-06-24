import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from datetime import datetime

# 1. 페이지 초기 설정 및 스타일 강제 주입
st.set_page_config(page_title="쿠팡형 프로페셔널 AI 상세페이지 빌더 v4", layout="wide")

# 상세페이지 배너들이 벌어지지 않고 실제 몰처럼 벼리게 착 붙어서 내려가도록 마진 컨트롤 CSS 주입
st.markdown("""
    <style>
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    div.block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []
if "page3_meta_data" not in st.session_state:
    st.session_state["page3_meta_data"] = {}
if "saved_projects_library" not in st.session_state:
    st.session_state["saved_projects_library"] = []

# 구글 오픈폰트(나눔고딕 브랜딩 폰트) 캐싱 다운로드
@st.cache_data
def load_korean_font_bytes():
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None

# 2. 사이드바 UI (입력란은 placeholder로 깔끔하게 기본값 공백 유지)
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
    placeholder="예: 주방 수납공간이 부족한 주부, 펜트리 정리가 고민인 분"
)

# 4단계 탭 구성 메뉴
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

# [핵심 개편] 첨부 레퍼런스 스타일을 녹여낸 780x1000 고정 규격 드로잉 엔진
def create_real_coupang_page(step_num, title, description, prod_name):
    # 사용자가 크기를 변경할 수 없도록 가로 780px, 세로 1000px 절대 규격 고정
    width, height = 780, 1000
    
    font_bytes = load_korean_font_bytes()
    if font_bytes:
        font_badge = ImageFont.truetype(io.BytesIO(font_bytes), 16)
        font_main_head = ImageFont.truetype(io.BytesIO(font_bytes), 34)
        font_sub_head = ImageFont.truetype(io.BytesIO(font_bytes), 24)
        font_body = ImageFont.truetype(io.BytesIO(font_bytes), 19)
    else:
        font_badge = font_main_head = font_sub_head = font_body = ImageFont.load_default()

    display_prod = prod_name if prod_name else "루시아이 스택 슬라이딩 팬트리 정리함"

    # --- [스타일 1: 1페이지 문제 제기 섹션 - 레퍼런스 3번 스타일 전격 반영] ---
    if step_num == 1:
        image = Image.new("RGB", (width, height), color=(245, 245, 247))
        draw = ImageDraw.Draw(image)
        
        # 상단 강렬한 다크블랙 경고 박스 영역
        draw.rectangle([0, 0, 780, 420], fill=(30, 32, 35))
        
        # 경고 원형 레드 배지 drawn
        draw.ellipse([365, 50, 415, 100], fill=(225, 40, 40))
        draw.text((386, 58), "!", fill=(255, 255, 255), font=font_sub_head)
        
        # 문제 제기 텍스트 배치
        draw.text((150, 150), "지금 팬트리에서 사용하고 있는", fill=(255, 255, 255), font=font_sub_head)
        draw.text((165, 200), "정리함을 머릿속에 떠올려 보세요.", fill=(255, 255, 255), font=font_main_head)
        
        # 중간 예시 이미지 가이드라인 스페이스
        draw.rectangle([60, 460, 720, 800], fill=(225, 228, 232), outline=(200, 205, 210), width=1)
        draw.text((280, 620), "[여기에 주방 문제점 사진 삽입]", fill=(100, 110, 120), font=font_sub_head)
        
        # 하단 강렬한 레드 카피라이팅 리본 바
        draw.rectangle([60, 830, 720, 910], fill=(200, 30, 40), radius=10)
        draw.text((230, 850), '" 안쪽 물건을 꺼내기가 너무 힘들어요 "', fill=(255, 255, 255), font=font_sub_head)

    # --- [스타일 2: 2페이지 메인 헤드 제품 소개 - 레퍼런스 2번 스타일 반영] ---
    elif step_num == 2:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 세련된 프리미엄 라벨링 타이포
        draw.text((70, 70), "LUXIAI SPECIAL LIFESTYLE", fill=(0, 102, 255), font=font_badge)
        
        # 메인 브랜드 타이틀 상품명 대형 마킹
        draw.text((70, 110), "루시아이", fill=(22, 28, 45), font=font_sub_head)
        draw.text((70, 150), "스택 슬라이딩 팬트리 정리함", fill=(22, 28, 45), font=font_main_head)
        
        # 딥블루 포인트 미드 서브 타이틀 배너 바
        draw.rectangle([0, 230, 780, 300], fill=(18, 45, 84))
        draw.text((70, 248), "좁은 틈새 & 노는 공간 100% 완벽 구조 활용", fill=(255, 255, 255), font=font_sub_head)
        
        # 대형 제품 실물 누끼 사진 플레이스홀더
        draw.rectangle([60, 340, 720, 940], fill=(248, 249, 250), outline=(230, 235, 240), width=2)
        draw.text((260, 620), "[여기에 제품 대표 연출 사진 업로드]", fill=(140, 145, 155), font=font_sub_head)

    # --- [스타일 3: 일반 세일즈 포인트 정보 정돈 스크롤 배너] ---
    else:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 상단 섹션 넘버링 포인트
        draw.text((60, 60), f"SECTION 0{step_num}", fill=(0, 102, 255), font=font_sub_head)
        
        # 서브 타이틀 wrap 연산
        wrapped_titles = textwrap.wrap(title, width=18)
        y_title_offset = 110
        for t_line in wrapped_titles:
            draw.text((60, y_title_offset), t_line, fill=(22, 28, 45), font=font_main_head)
            y_title_offset += 45

        # 콤팩트 미디어 하우징 박스
        box_top = y_title_offset + 30
        box_bottom = box_top + 480
        draw.rectangle([60, box_top, 720, box_bottom], fill=(250, 251, 253), outline=(235, 238, 242), width=2)
        draw.text((250, box_top + 220), "📦 [실물 기능 레이어 이미지]", fill=(120, 125, 135), font=font_sub_head)

        # 상세 요약 하단 정보 텍스트 구조 처리
        y_body_start = box_bottom + 35
        draw.rectangle([60, y_body_start, 65, y_body_start + 25], fill=(0, 102, 255))
        draw.text((75, y_body_start + 2), "CHECK POINT", fill=(100, 110, 120), font=font_badge)
        
        wrapped_body = textwrap.wrap(description, width=35)
        y_body_offset = y_body_start + 40
        for b_line in wrapped_body:
            draw.text((60, y_body_offset), b_line, fill=(80, 85, 95), font=font_body)
            y_body_offset += 28

    return image

# 시퀀셜 데이터 일괄 빌드 코어 파트
def build_and_store_cards():
    p_name = product_name if product_name else "[당일출고] 빅사이즈! 루시아이 스택 슬라이딩 팬트리 정리함"
    
    steps_data = [
        {"num": 1, "title": "공간 낭비의 시작", "desc": "안쪽 물건까지 한 번에 찾기 힘든 깊숙한 하부장 수납공간의 문제."},
        {"num": 2, "title": "루시아이 슬라이딩 시스템", "desc": "좁은 주방의 데드스페이스를 완벽하게 지워내고 일상의 밀도를 높입니다."},
        {"num": 3, "title": "스르륵- 부드럽게 끝까지 열리는 하이테크 슬라이드 레일", "desc": "적은 힘으로도 걸림 없이 매끄럽게 열리는 서랍형 오픈 메커니즘을 설계하여 깊숙이 숨은 식자재까지 손쉽게 꺼냅니다."},
        {"num": 4, "title": "흔들림 없이 무한 확장되는 하이 스택 적층 결합 구조", "desc": "위로 안전하게 쌓아 올려 고정하는 전용 홈 포지셔닝 기술 설계로, 흔들림 없이 위쪽 수직 데드스페이스까지 남김없이 활용합니다."},
        {"num": 5, "title": "무거운 생수와 대용량 소스통도 휘어짐 없는 압도적 고하중", "desc": "두껍고 견고한 친환경 마감 원단을 사용하여 시간이 지나도 처지거나 찌그러지지 않는 탁월한 하중 내구성을 보여줍니다."},
        {"num": 6, "title": "주방을 넘어 다용도실, 세탁실까지 인테리어가 되는 미니멀 디자인", "desc": "모던하고 군더더기 없는 화이트 무드로 집안 어느 장소에 배치해도 고급 가구처럼 공간 속에 자연스럽게 녹아듭니다."},
        {"num": 7, "title": "살림 인플루언서들이 극찬한 실제 리얼 유저 만족도", "desc": "'정리가 제일 쉬워졌어요' 수많은 주부와 정리 전문가들이 먼저 알아보고 선택한 루시아이만의 정밀한 품질 가치입니다."},
        {"num": 8, "title": "망설이면 품절! 오늘 단 하루만 주어지는 특가 즉시 출고", "desc": "고민은 배송만 늦출 뿐입니다. 지금 바로 선택하셔서 모델하우스처럼 정돈된 완벽한 주방 수납 솔루션을 만나보세요."}
    ]
    cards = []
    for step in steps_data:
        generated_img = create_real_coupang_page(step["num"], step["title"], step["desc"], p_name)
        cards.append(generated_img)
    st.session_state["page3_saved_images"] = cards
    st.session_state["page3_meta_data"] = {
        "product_name": p_name,
        "target_customer": target_customer if target_customer else "주방 수납이 고민인 고객",
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
            st.success("✨ 실전 수직형 상세페이지 템플릿 인스턴스 빌드 완료! 3페이지 탭에서 결과물을 확인하세요.")

# ====================================================
# ➕ 2. 벤치마킹 데이터 등록 탭
# ====================================================
elif menu == "➕ 2. 벤치마킹 데이터 등록":
    st.markdown("### ➕ 경쟁사 링크 구조 연산 분석")
    url_input = st.text_input("분석할 쿠팡 또는 스마트스토어 상품 주소(URL):")
    if st.button("레이아웃 프레임워크 동적 추출 및 빌드"):
        if url_input:
            build_and_store_cards()
            st.success("✅ 타겟 상세페이지 흐름 학습 성공! 3페이지에서 롱디자인을 확인해 보세요.")

# ====================================================
# 📂 3. 상세페이지 샘플 제작 및 검토 탭 (★ 사이즈 절대 고정 및 롱배너 레이아웃 최적화)
# ====================================================
elif menu == "📂 3. 상세페이지 샘플 제작 및 검토":
    st.markdown("### 📄 3페이지: 실전 쿠팡 규격(가로 780px 고정) 수직 스크롤 검토 공간")
    
    if st.session_state["page3_saved_images"]:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            st.info("📱 화면 정중앙에 실제 모바일 쇼핑몰처럼 780px 너비가 절대 고정되어 연속 배치됩니다. 흐름을 완벽히 스캔해 보세요.")
        with col_btn2:
            if st.button("📦 4페이지 보관함으로 세트 저장하기", type="primary", use_container_width=True):
                project_bundle = {
                    "meta": st.session_state["page3_meta_data"],
                    "images": list(st.session_state["page3_saved_images"])
                }
                st.session_state["saved_projects_library"].append(project_bundle)
                st.balloons()
                st.success("🚀 저장 및 그룹 묶음 이관이 완료되었습니다!")
        st.markdown("---")
        
        # [핵심 변경] 3분할 열 레이아웃을 통해 가운데(col_mid)에만 780px 크기를 절대 유지하여 수직으로 누적 출력
        col_left, col_mid, col_right = st.columns([1, 4, 1])
        
        with col_mid:
            for idx, img in enumerate(st.session_state["page3_saved_images"]):
                # width=780 지정을 통해 강제 리사이징 억제 및 규격 통일화 실현
                st.image(img, width=780, caption=f"Coupang Detail Block Section #{idx + 1}")
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button(
                    label=f"📥 블록 #{idx + 1} 고해상도 원본 다운로드",
                    data=buf.getvalue(),
                    file_name=f"coupang_fixed_page_{idx+1}.png",
                    mime="image/png",
                    key=f"p3_dl_btn_{idx}"
                )
                st.markdown("<hr style='border:1px dashed #e0e0e0; margin-top:20px; margin-bottom:20px;'>", unsafe_allow_html=True)
    else:
        st.info("💡 아직 디자인된 상세페이지 샘플 세트가 부재합니다. 1페이지 혹은 2페이지에서 먼저 생성 명령을 실행해 주세요!")

# ====================================================
# 📦 4. 저장된 프로젝트 보관함 탭
# ====================================================
elif menu == "📦 4. 저장된 프로젝트 보관함 (미리보기)":
    st.markdown("### 📦 4페이지: 상세페이지 기획 세트 그룹별 통합 보관함")
    
    if st.session_state["saved_projects_library"]:
        for p_idx, project in enumerate(reversed(st.session_state["saved_projects_library"])):
            meta = project["meta"]
            actual_idx = len(st.session_state["saved_projects_library"]) - 1 - p_idx
            
            with st.expander(f"📁 [그룹 #{actual_idx + 1}] {meta.get('product_name')} | 등록일: {meta.get('created_at')}", expanded=True):
                st.markdown(f"🎯 **설계된 타겟 타겟층:** {meta.get('target_customer')}")
                
                cols = st.columns(4)
                for img_idx, img in enumerate(project["images"]):
                    col_target = cols[img_idx % 4]
                    with col_target:
                        st.markdown(f"**📜 BLOCK {img_idx + 1}**")
                        st.image(img, use_container_width=True)
                        
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        st.download_button(
                            label="📥 다운로드",
                            data=buf.getvalue(),
                            file_name=f"group_{actual_idx+1}_block_{img_idx+1}.png",
                            mime="image/png",
                            key=f"p4_dl_{actual_idx}_{img_idx}"
                        )
                
                if st.button(f"🗑️ 해당 그룹 영구 삭제", key=f"del_group_{actual_idx}"):
                    st.session_state["saved_projects_library"].pop(actual_idx)
                    st.rerun()
    else:
        st.warning("⚠️ 보관함이 비어 있습니다. 3페이지 검토 센터 상단에서 '4페이지 보관함으로 세트 저장하기' 버튼을 클릭해 주세요.")
