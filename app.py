import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os

# [추가] 최신 Gemini API 패키지 (설치 필요: pip install google-genai)
# import google.genai as genai 

# 1. 페이지 초기 설정 및 스타일 주입
st.set_page_config(page_title="쿠팡형 프로페셔널 AI 상세페이지 빌더 v16.0", layout="wide")

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

# 세션 상태 초기화
if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []
if "page3_meta_data" not in st.session_state:
    st.session_state["page3_meta_data"] = {}

@st.cache_data
def load_korean_font():
    # 1차 시도: 구글 나눔고딕 웹 폰트 다운로드
    url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return io.BytesIO(response.content)
    except Exception:
        pass
    
    # 2차 시도: 운영체제별 로컬 한글 폰트 패스 탐색
    system_fonts = [
        "C:/Windows/Fonts/malgun.ttf",       # Windows
        "C:/Windows/Fonts/malgunbd.ttf",     # Windows Bold
        "/System/Library/Fonts/AppleSDGothicNeo.ttc", # MacOS
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" # Linux
    ]
    for font_path in system_fonts:
        if os.path.exists(font_path):
            return font_path
            
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
        "📂 3. 상세페이지 샘플 제작 및 검토"
    ],
    horizontal=True
)

# =========================================================================
# 🔥 [핵심 기능] 쿠팡 상위 1% 벤치마킹 구조화 멀티 레이아웃 드로잉 엔진 (780x1000 고정)
# =========================================================================
def draw_benchmarked_coupang_page(step_num, title="", description="", prod_name=""):
    width, height = 780, 1000
    font_src = load_korean_font()
    
    # 폰트 로드 및 크기 세팅 (예외 처리 강화)
    try:
        if font_src:
            font_xs = ImageFont.truetype(font_src, 14)
            font_badge = ImageFont.truetype(font_src, 17)
            font_body = ImageFont.truetype(font_src, 20)
            font_sub_head = ImageFont.truetype(font_src, 25)
            font_main_head = ImageFont.truetype(font_src, 32)
            font_huge = ImageFont.truetype(font_src, 40)
        else:
            raise ValueError("Font not found")
    except Exception:
        font_xs = font_badge = font_body = font_sub_head = font_main_head = font_huge = ImageFont.load_default()

    display_prod = prod_name if prod_name else "루시아이 스택 슬라이딩 팬트리 정리함"

    # --- [BLOCK 1: 브랜드 인트로 및 프리미엄 히어로 페이지] ---
    if step_num == 1:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        draw.rectangle([0, 0, 780, 45], fill=(22, 28, 45))
        draw.text((40, 12), "COUPANG JET-DELIVERY PREMIUM SELECTION", fill=(255, 215, 0), font=font_xs)
        
        draw.text((70, 100), "PREMIUM HOUSEHOLD SOLUTIONS", fill=(0, 102, 255), font=font_badge)
        draw.text((70, 135), "공간의 가치를 바꾸는 단 하나의 선택", fill=(110, 115, 125), font=font_sub_head)
        
        wrapped_lines = textwrap.wrap(display_prod, width=14)
        y_offset = 180
        for line in wrapped_lines:
            draw.text((70, y_offset), line, fill=(20, 24, 35), font=font_huge)
            y_offset += 48
        
        draw.rectangle([60, 320, 720, 850], fill=(245, 247, 250), outline=(225, 228, 232), width=2)
        draw.text((210, 570), "📸 [여기에 메인 썸네일 제품 사진]", fill=(120, 125, 135), font=font_sub_head)
        
        draw.rounded_rectangle([60, 890, 720, 950], fill=(240, 244, 255), radius=5)
        draw.text((90, 910), "💡 본 페이지는 쿠팡 공식 규격 가로 780px 정밀 매칭 템플릿입니다.", fill=(0, 80, 200), font=font_badge)

    # --- [BLOCK 2: 문제 제기 고대비 반전 다크 배너] ---
    elif step_num == 2:
        image = Image.new("RGB", (width, height), color=(26, 28, 33))
        draw = ImageDraw.Draw(image)
        
        draw.ellipse([365, 70, 415, 120], fill=(230, 45, 45))
        draw.text((386, 78), "!", fill=(255, 255, 255), font=font_sub_head)
        
        draw.text((200, 170), "아직도 주방 싱크대 하부장과 팬트리에", fill=(180, 185, 195), font=font_sub_head)
        draw.text((140, 215), "무조건 쌓아두기만 하십니까?", fill=(255, 255, 255), font=font_main_head)
        
        draw.rectangle([60, 300, 720, 720], fill=(45, 48, 55), outline=(70, 75, 85), width=1)
        draw.text((220, 490), "[🚨 꺼내기 힘들고 무너지는 수납장 연출 사진]", fill=(160, 165, 175), font=font_body)
        
        draw.rounded_rectangle([60, 770, 720, 860], fill=(210, 35, 45), radius=8)
        draw.text((150, 795), '“ 안쪽 물건 한 번 꺼내려다 다 쏟아지고 무너져요... ”', fill=(255, 255, 255), font=font_sub_head)
        
        draw.text((215, 910), "방치된 데드스페이스, 이제는 바뀌어야 합니다.", fill=(130, 135, 145), font=font_body)

    # --- [BLOCK 3: 기능 강조형 레이아웃 - 레일 슬라이딩 모션] ---
    elif step_num == 3:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        draw.rectangle([50, 70, 55, 105], fill=(0, 102, 255))
        draw.text((70, 75), "CORE FEATURE 01", fill=(0, 102, 255), font=font_badge)
        
        draw.text((60, 120), "손가락 하나로 스르륵-", fill=(20, 24, 35), font=font_sub_head)
        draw.text((60, 160), "안쪽 깊숙한 물건까지 부러짐 없는 슬라이딩", fill=(20, 24, 35), font=font_main_head)
        
        draw.rectangle([60, 240, 720, 760], fill=(250, 252, 255), outline=(220, 226, 235), width=2)
        draw.text((200, 480), "🎥 [슬라이딩 부드러운 작동 GIF 공간]", fill=(0, 90, 220), font=font_sub_head)
        
        draw.rounded_rectangle([60, 800, 720, 930], fill=(245, 247, 250), radius=5)
        draw.text((90, 825), "✔ 하이테크 볼베어링 내장식 스레드 기술 도입", fill=(50, 55, 65), font=font_body)
        draw.text((90, 870), "✔ 끝까지 당겨도 빠지지 않는 안전 스토퍼 장치 체결", fill=(50, 55, 65), font=font_body)

    # --- [BLOCK 4: 입체적 공간 스택 적층 레이아웃] ---
    elif step_num == 4:
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        draw.rectangle([50, 70, 55, 105], fill=(0, 102, 255))
        draw.text((70, 75), "CORE FEATURE 02", fill=(0, 102, 255), font=font_badge)
        
        draw.text((60, 120), "위로 위로, 빈틈없이 수납 완성!", fill=(20, 24, 35), font=font_sub_head)
        draw.text((60, 160), "무너지지 않는 견고한 모듈러 스택 시스템", fill=(20, 24, 35), font=font_main_head)
        
        draw.rectangle([60, 240, 720, 760], fill=(245, 248, 255), outline=(210, 220, 240), width=2)
        draw.text((180, 480), "📦 [다단 적층으로 수납 효율 200% 극대화 연출 이미지]", fill=(0, 90, 220), font=font_body)
        
        draw.rounded_rectangle([60, 800, 720, 930], fill=(245, 247, 250), radius=5)
        draw.text((90, 825), "✔ 상하단 결합 홈 설계로 흔들림 없는 완벽 적층 고정", fill=(50, 55, 65), font=font_body)
        draw.text((90, 870), "✔ 고강도 고순도 PP 소재 채택으로 고하중도 휨 없이 지탱", fill=(50, 55, 65), font=font_body)

    # --- [BLOCK 5: 내구성 및 고하중 테스트 검증] ---
    elif step_
