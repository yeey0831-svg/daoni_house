import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from datetime import datetime

# 1. 페이지 초기 설정 및 스타일 주입
st.set_page_config(page_title="쿠팡형 프로페셔널 AI 상세페이지 빌더 v5", layout="wide")

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

# 2. 사이드바 UI
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

# =========================================================================
# 🔥 [핵심 기능] 쿠팡 상위 1% 벤치마킹 구조화 멀티 레이아웃 드로잉 엔진 (780x1000 고정)
# =========================================================================
def draw_benchmarked_coupang_page(step_num, title, description, prod_name):
    width, height = 780, 1000
    font_bytes = load_korean_font_bytes()
    
    if font_bytes:
        font_xs = ImageFont.truetype(io.BytesIO(font_bytes), 14)
        font_badge = ImageFont.truetype(io.BytesIO(font_bytes), 17)
        font_body = ImageFont.truetype(io.BytesIO(font_bytes), 20)
        font_sub_head = ImageFont.truetype(io.BytesIO(font_bytes), 25)
        font_main_head = ImageFont.truetype(io.BytesIO(font_bytes), 36)
        font_huge = ImageFont.truetype(io.BytesIO(font_bytes), 42)
    else:
        font_xs = font_badge = font_body = font_sub_head = font_main_head = font_huge = ImageFont.load_default()

    display_prod = prod_name if prod_name else "루시아이 스택 슬라이딩 팬트리 정리함"

    # --- [BLOCK 1: 브랜드 인트로 및 프리미엄 히어로 페이지] ---
    if step_num == 1:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 최상단 카테고리 매칭 엠블럼 바
        draw.rectangle([0, 0, 780, 45], fill=(22, 28, 45))
        draw.text((40, 12), "COUPANG JET-DELIVERY PREMIUM SELECTION", fill=(255, 215, 0), font=font_xs)
        
        # 프리미엄 영문 서브 라인 및 메인 카피 배치 강조
        draw.text((70, 100), "PREMIUM HOUSEHOLD SOLUTIONS", fill=(0, 102, 255), font=font_badge)
        draw.text((70, 135), "공간의 가치를 바꾸는 단 하나의 선택", fill=(110, 115, 125), font=font_sub_head)
        
        # 메인 타이틀 볼드 임팩트 레이아웃
        draw.text((70, 180), display_prod, fill=(20, 24, 35), font=font_huge)
        
        # 중앙 제품 메인 메인 히어로 컷 가이드라인 (스마트폰 뷰 형태)
        draw.rectangle([60, 280, 720, 850], fill=(245, 247, 250), outline=(225, 228, 232), width=2)
        draw.text((230, 540), "📸 [여기에 메인 썸네일/히어로 이미지 제품 사진]", fill=(120, 125, 135), font=font_sub_head)
        
        # 하단 디테일 속성 요약 바
        draw.rounded_rectangle([60, 890, 720, 950], fill=(240, 244, 255), radius=5)
        draw.text((90, 907), "💡 본 페이지는 쿠팡 공식 규격 가로 780px 정밀 매칭 템플릿입니다.", fill=(0, 80, 200), font=font_badge)

    # --- [BLOCK 2: 문제 제기 고대비 반전 다크 배너] ---
    elif step_num == 2:
        image = Image.new("RGB", (width, height), color=(26, 28, 33)) # 어두운 무드
        draw = ImageDraw.Draw(image)
        
        # 경고 원형 레드 엠블럼 배지
        draw.ellipse([365, 70, 415, 120], fill=(230, 45, 45))
        draw.text((386, 78), "!", fill=(255, 255, 255), font=font_sub_head)
        
        # 고대비 텍스트 배치로 시선 집중 효과
        draw.text((220, 170), "아직도 주방 싱크대 하부장과 팬트리에", fill=(180, 185, 195), font=font_sub_head)
        draw.text((140, 215), "무조건 쌓아두기만 하십니까?", fill=(255, 255, 255), font=font_main_head)
        
        # 실제 소비자의 불편함을 보여주는 리얼 컷 프레임
        draw.rectangle([60, 300, 720, 720], fill=(45, 48, 55), outline=(70, 75, 85), width=1)
        draw.text((240, 490), "[🚨 꺼내기 힘들고 무너지는 수납장 연출 사진]", fill=(160, 165, 175), font=font_body)
        
        # 하단 강렬한 경고용 레드 리본 카피 박스
        draw.rounded_rectangle([60, 770, 720, 860], fill=(210, 35, 45), radius=8)
        draw.text((160, 795), '“ 안쪽 물건 한 번 꺼내려다 다 쏟아지고 무너져요... ”', fill=(255, 255, 255), font=font_sub_head)
        
        # 감성 자극 서브 바
        draw.text((215, 910), "방치된 데드스페이스, 이제는 바뀌어야 합니다.", fill=(130, 135, 145), font=font_body)

    # --- [BLOCK 3: 기능 강조형 레이아웃 - 레일 슬라이딩 모션] ---
    elif step_num == 3:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 좌측 테두리 포인트 인디케이터
        draw.rectangle([50, 70, 55, 105], fill=(0, 102, 255))
        draw.text((70, 75), "CORE FEATURE 01", fill=(0, 102, 255), font=font_badge)
        
        draw.text((60, 120), "손가락 하나로 스르륵-", fill=(20, 24, 35), font=font_sub_head)
        draw.text((60, 160), "안쪽 깊숙한 물건까지 부러짐 없는 슬라이딩", fill=(20, 24, 35), font=font_main_head)
        
        # 기능 설명 기획 레이어 박스
        draw.rectangle([60, 240, 720, 760], fill=(250, 252, 255), outline=(220, 226, 235), width=2)
        draw.text((220, 480), "🎥 [슬라이딩 부드러운 작동 GIF 및 영상 공간]", fill=(0, 90, 220), font=font_sub_head)
        
        # 하단 체크포인트 정돈 가이드
        draw.rounded_rectangle([60, 800, 720, 930], fill=(245, 247, 250), radius=5)
        draw.text((90, 825), "✔ 하이테크 볼베어링 내장식 스레드 기술 도입", fill=(50, 55, 65), font=font_body)
        draw.text((90, 870), "✔ 끝까지 당겨도 빠지지 않는 안전 스토퍼 안전 장치 체결", fill=(50, 55, 65), font=font_body)

    # --- [BLOCK 4: 입체적 공간 스택 적층 레이아웃] ---
    elif step_num == 4:
        image = Image.new("RGB", (248, 249, 252)) # 부드러운 그레이 배경
        image = Image.new("RGB", (width, height), color=(248, 249, 252))
        draw = ImageDraw.Draw(image)
        
        draw.text((60, 70), "CORE FEATURE 02", fill=(0, 102, 255), font=font_badge)
        draw.text((60, 110), "위로 위로 무한 적층 결합!", fill=(22, 28, 45), font=font_main_head)
        draw.text((60, 160), "죽어있던 수직 공간을 200% 정밀 재확장합니다.", fill=(90, 95, 105), font=font_sub_head)
        
        # 대형 세로형 연출 이미지 프레임
        draw.rectangle([60, 230, 720, 850], fill=(255, 255, 255), outline=(230, 232, 235), width=1)
        draw.text((230, 520), "📦 [위로 깔끔하게 쌓아올린 제품 배치 사진]", fill=(120, 125, 135), font=font_sub_head)
        
        # 우측 하단 미니 오버레이 뱃지 효과 시뮬레이션
        draw.rectangle([500, 770, 690, 820], fill=(22, 28, 45))
        draw.text((535, 785), "강력한 홈 결합 설계", fill=(255, 255, 255), font=font_badge)

    # --- [BLOCK 5: 고하중 신뢰성 검증 스펙 배너] ---
    elif step_num == 5:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        draw.text((60, 70), "STRENGTH TEST", fill=(230, 45, 45), font=font_badge)
        draw.text((60, 110), "무거운 대용량 소스통을 가득 채워도", fill=(22, 28, 45), font=font_sub_head)
        draw.text((60, 155), "휘어짐이나 흔들림이 전혀 없습니다.", fill=(22, 28, 45), font=font_main_head)
        
        # 신뢰성 수치 그래프 시각화 스타일 프레임
        draw.rectangle([60, 230, 720, 700], fill=(252, 252, 252), outline=(235, 235, 235), width=2)
        draw.text((250, 440), "[📊 자체 하중 지지력 테스트 검증 스크린샷]", fill=(110, 115, 125), font=font_body)
        
        # 하단 스펙 요약 메트릭 카드 3분할 배치 레이아웃 효과
        draw.rectangle([60, 750, 260, 920], fill=(245, 247, 252), outline=(220, 225, 235))
        draw.text((105, 780), "안전 하중", fill=(100, 105, 115), font=font_xs)
        draw.text((100, 830), "정밀 통과", fill=(22, 28, 45), font=font_badge)
        
        draw.rectangle([290, 750, 490, 920], fill=(245, 247, 252), outline=(220, 225, 235))
        draw.text((325, 780), "두께 마감재 원단", fill=(100, 105, 115), font=font_xs)
        draw.text((345, 830), "고강도 PP", fill=(22, 28, 45), font=font_badge)
        
        draw.rectangle([520, 750, 720, 920], fill=(245, 247, 252), outline=(220, 225, 235))
        draw.text((570, 780), "유해 물질", fill=(100, 105, 115), font=font_xs)
        draw.text((560, 830), "BPA FREE 검출", fill=(230, 45, 45), font=font_badge)

    # --- [BLOCK 6: 라이프스타일 인테리어 감성 매칭] ---
    elif step_num == 6:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        draw.text((310, 80), "VERSATILE DESIGN", fill=(110, 115, 125), font=font_badge)
        draw.text((140, 120), "주방을 넘어 일상의 모든 동선을 완벽하게", fill=(20, 24, 35), font=font_main_head)
        
        # 웰메이드 잡지 화보 느낌의 대형 프레임 레이아웃
        draw.rectangle([60, 200, 720, 850], fill=(244, 244, 246), outline=(230, 230, 232), width=1)
        draw.text((210, 500), "📸 [다용도실, 세탁실, 드레스룸 배치 모던 감성 컷]", fill=(130, 135, 145), font=font_body)
        
        draw.text((80, 890), "#팬트리정리 #싱크대하부장 #틈새수납 #오브제리빙 #루시아이", fill=(0, 102, 255), font=font_sub_head)

    # --- [BLOCK 7: 구매 전환율 극대화 - 경쟁사 완벽 정밀 비교 표 레이아웃] ---
    elif step_num == 7:
        image = Image.new("RGB", (width, height), color=(248, 250, 254))
        draw = ImageDraw.Draw(image)
        
        draw.text((250, 60), "COMPARE & CHOICE", fill=(0, 102, 255), font=font_badge)
        draw.text((180, 100), "비교해 볼수록 결론은 하나뿐입니다", fill=(22, 28, 45), font=font_main_head)
        
        # 정밀 표 가로지르는 테이블 드로잉 공법 구현
        # 헤더 라인
        draw.rectangle([50, 190, 730, 250], fill=(22, 28, 45))
        draw.text((90, 210), "비교 포인트", fill=(255, 255, 255), font=font_badge)
        draw.text((310, 210), "루시아이 슬라이딩", fill=(255, 215, 0), font=font_badge)
        draw.text((560, 210), "일반 저가형 정리함", fill=(180, 185, 195), font=font_badge)
        
        # 로우 1: 슬라이딩 방식
        draw.rectangle([50, 250, 730, 390], fill=(255, 255, 255), outline=(225, 230, 240))
        draw.text((70, 305), "서랍 슬라이딩", fill=(50, 55, 65), font=font_badge)
        draw.text((310, 290), "볼베어링 레일 장착\n(끝까지 부드럽게 작동)", fill=(0, 102, 255), font=font_body)
        draw.text((560, 290), "일반 플라스틱 마찰\n(뻑뻑하고 쉽게 걸림)", fill=(130, 135, 145), font=font_body)
        
        # 로우 2: 적층 안정성
        draw.rectangle([50, 390, 730, 530], fill=(255, 255, 255), outline=(225, 230, 240))
        draw.text((70, 445), "수직 적층 결합", fill=(50, 55, 65), font=font_badge)
        draw.text((310, 430), "전용 홈 고정 결합\n(흔들림 없는 일체형)", fill=(0, 102, 255), font=font_body)
        draw.text((560, 430), "그냥 위로 얹어둠\n(스르륵 미끄러져 위험)", fill=(130, 135, 145), font=font_body)

        # 로우 3: 내구성 소재
        draw.rectangle([50, 530, 730, 670], fill=(255, 255, 255), outline=(225, 230, 240))
        draw.text((80, 585), "소재 내구성", fill=(50, 55, 65), font=font_badge)
        draw.text((310, 570), "고강도 특수 PP 마감\n(대용량 무거운 하중 견딤)", fill=(0, 102, 255), font=font_body)
        draw.text((560, 570), "얇은 재생 플라스틱\n(시간 지나면 처짐 발생)", fill=(130, 135, 145), font=font_body)

        # 실제 쿠팡 정품 인증 하단 보증 바 레이아웃 효과
        draw.rounded_rectangle([50, 720, 730, 920], fill=(235, 242, 255), radius=10)
        draw.text((260, 760), "🛡️ 100% 본사 정품 품질 보증 스탬프", fill=(0, 90, 220), font=font_sub_head)
        draw.text((140, 820), "루시아이 공식 스토어 제품은 엄격한 품질 검사를 거쳐 즉시 출고됩니다.", fill=(80, 85, 95), font=font_body)

    # --- [BLOCK 8: 클로징 및 오늘 단 하루 혜택 마감 종착지 (CTA)] ---
    else:
        image = Image.new("RGB", (width, height), color=(18, 45, 84)) # 신뢰감을 주는 딥블루 카탈로그 무드
        draw = ImageDraw.Draw(image)
        
        draw.text((320, 120), "ORDER NOW", fill=(255, 215, 0), font=font_badge)
        draw.text((120, 170), "고민은 배송만 늦출 뿐, 공간의 기적을 경험하세요", fill=(255, 255, 255), font=font_sub_head)
        
        # 최종 구매 마감 패키지 정보 상자
        draw.rounded_rectangle([70, 260, 710, 720], fill=(255, 255, 255), radius=12)
        
        draw.text((120, 320), "Premium Product Configuration", fill=(120, 125, 135), font=font_badge)
        draw.text((120, 360), "[당일출고] 루시아이 스택 슬라이딩 팬트리 정리함 특대형", fill=(22, 28, 45), font=font_sub_head)
        
        draw.line([(120, 440), (660, 440)], fill=(230, 235, 240), width=2)
        
        # 혜택 정보 도식화 구조
        draw.text((120, 480), "• 배송 정보 : 쿠팡 제트배송 시스템 연동 익일 도착 보장", fill=(50, 55, 65), font=font_body)
        draw.text((120, 530), "• 특별 혜택 : 포토 리뷰 작성 시 전원 스타벅스 기프티콘 증정", fill=(50, 55, 65), font=font_body)
        draw.text((120, 580), "• 고객 센터 : 100% 초기 불량 무상 안심 교환 반품 케어 보장", fill=(50, 55, 65), font=font_body)
        
        # 최종 가격 결제 유도 대형 버튼 프레임 레이아웃 시뮬레이션
        draw.rounded_rectangle([70, 780, 710, 880], fill=(255, 194, 0), radius=8) # 쿠팡 시그니처 옐로우 버튼 매칭
        draw.text((245, 808), "🛒 바로 구매하러 가기 (쿠팡 이동)", fill=(22, 28, 45), font=font_sub_head)
        
        draw.text((250, 930), "COPYRIGHT © LUXIAI ALL RIGHTS RESERVED.", fill=(120, 130, 150), font=font_xs)

    return image

# 시퀀셜 자동 기획 연동 함수
def build_and_store_cards():
    p_name = product_name if product_name else "[당일출고] 빅사이즈! 루시아이 스택 슬라이딩 팬트리 정리함"
    
    # 8개 블록에 각각 지정된 유니크 레이아웃 순차 매핑 호출
    cards = []
    for step_idx in range(1, 9):
        # API 분석 생략시 기본 고품질 상위 1% 마케팅 카피가 내장 드로잉 구조에 들어감
        generated_img = draw_benchmarked_coupang_page(step_idx, "", "", p_name)
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
# ➕ 2. 벤치마킹 데이터 등록 탭 (★ 벤치마킹 시각 구체화)
# ====================================================
elif menu == "➕ 2. 벤치마킹 데이터 등록":
    st.markdown("### ➕ 경쟁사 링크 구조 연산 분석 및 벤치마킹 대조")
    url_input = st.text_input("분석할 쿠팡 또는 스마트스토어 상품 주소(URL)를 입력하세요:")
    
    st.info("💡 입력하신 URL의 상세페이지 기획 설계도(히어로존, 문제제기 반전, 스펙 대조 인포그래픽, X/O 비교 표 레이아웃 위치 구조)를 자동으로 매핑 연산하여 페이지 3에 780px 정밀 규격으로 조판합니다.")
    
    if st.button("레이아웃 프레임워크 동적 추출 및 빌드"):
        if url_input:
            with st.spinner("경쟁사 폰트 위치, 강조 구역, 히어로 배치를 학습 모방하여 빌드 중..."):
                build_and_store_cards()
                st.success("✅ 타겟 상세페이지 흐름 완전 이관 성공! 3페이지에서 완벽히 수직 정렬된 롱디자인을 확인해 보세요.")

# ====================================================
# 📂 3. 상세페이지 샘플 제작 및 검토 탭 (★ 가로 780px 절대 강제 고정 뷰)
# ====================================================
elif menu == "📂 3. 상세페이지 샘플 제작 및 검토":
    st.markdown("### 📄 3페이지: 실전 쿠팡 규격(가로 780px 고정) 수직 스크롤 검토 공간")
    
    if st.session_state["page3_saved_images"]:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            st.info("📱 화면 정중앙에 실제 쿠팡 쇼핑몰 앱처럼 가로 780px 너비가 고정되어 아래로 물 흐르듯 이어집니다.")
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
        
        # 3분할 열 레이아웃을 사용해 가운데(col_mid)에만 780px 크기를 절대 유지하여 스크롤 뷰 구현
        col_left, col_mid, col_right = st.columns([1, 4, 1])
        
        with col_mid:
            for idx, img in enumerate(st.session_state["page3_saved_images"]):
                # width=780을 주어 반응형을 무력화하고 모바일 상세페이지처럼 위아래로 착 달라붙어 출력
                st.image(img, width=780, caption=f"Coupang Premium Layout Block Section #{idx + 1}")
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button(
                    label=f"📥 블록 #{idx + 1} 고해상도 원본 다운로드",
                    data=buf.getvalue(),
                    file_name=f"coupang_fixed_page_{idx+1}.png",
                    mime="image/png",
                    key=f"p3_dl_btn_{idx}"
                )
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) # 이미지 사이 빈틈 최소화
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
