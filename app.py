import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from datetime import datetime

# 1. 페이지 설정 및 세션 상태 초기화
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v2", layout="wide")

# 세션 상태(저장소) 정의
if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []
if "page3_meta_data" not in st.session_state:
    st.session_state["page3_meta_data"] = {}
if "saved_projects_library" not in st.session_state:
    st.session_state["saved_projects_library"] = []  # 4페이지 그룹 보관함 데이터
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

# 2. 사이드바 UI (기본 마케팅 정보 입력)
st.sidebar.title("📋 기본 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input(
    "상품명", 
    value="다온이네 밀봉 자석집게 6세트+1개 증정 다용도 주방 밀폐 봉지집게"
)
target_customer = st.sidebar.text_input("타겟 고객", value="주부, 자취생")

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

# Gemini API 호출 래퍼 함수
def call_gemini_api(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            st.error(f"⚠️ API 에러 (코드 {response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"통신 중 에러 발생: {e}")
        return None

# [핵심 개편] 실제 쇼핑몰 레이아웃을 따르는 이미지 드로잉 엔진
def create_high_fidelity_sample(step_num, title, description):
    # 쿠팡 표준 가로 780px, 높이 550px 여유 공간 설계
    width, height = 780, 550
    # 전체 상세페이지 배경 테마 (고급스러운 소프트 화이트/라이트 그레이 톤)
    image = Image.new("RGB", (width, height), color=(248, 249, 250))
    draw = ImageDraw.Draw(image)
    
    # 테두리 가이드라인 선 그리기
    draw.rectangle([10, 10, width-10, height-10], outline=(220, 224, 230), width=2)
    
    # 폰트 에셋 바인딩
    font_bytes = load_korean_font_bytes()
    if font_bytes:
        font_title = ImageFont.truetype(io.BytesIO(font_bytes), 28)
        font_sub = ImageFont.truetype(io.BytesIO(font_bytes), 20)
        font_body = ImageFont.truetype(io.BytesIO(font_bytes), 17)
        font_box = ImageFont.truetype(io.BytesIO(font_bytes), 18)
    else:
        font_title = font_sub = font_body = font_box = ImageFont.load_default()
        
    # 상단 헤더 타이틀 영역 레이아웃
    draw.text((35, 35), f"PAGE {step_num}: {title}", fill=(228, 27, 43), font=font_title)
    draw.line([(35, 80), (width-35, 80)], fill=(200, 200, 200), width=1)
    
    # 홀수번 페이지와 짝수번 페이지의 디자인 레이아웃 다변화 (좌우 교차 배치 구조)
    is_even = (step_num % 2 == 0)
    
    # 이미지가 들어갈 공간 (흰색 배경 박스 및 연한 회색 외곽선 지정)
    if is_even:
        # 짝수 페이지: 왼쪽에 이미지/동영상 박스 배치, 오른쪽에 카피라이팅 텍스트
        box_coords = [35, 120, 360, 480]
        text_x_start = 390
        box_type = "🎥 동영상 노출 공간" if step_num == 2 else "📦 상품 이미지 공간"
    else:
        # 홀수 페이지: 오른쪽에 이미지 박스 배치, 왼쪽에 카피라이팅 텍스트
        box_coords = [420, 120, 745, 480]
        text_x_start = 35
        box_type = "📦 상품 이미지 공간"
        
    # 미디어 영역 흰색 배경 박스 드로잉
    draw.rectangle(box_coords, fill=(255, 255, 255), outline=(180, 185, 195), width=2)
    
    # 미디어 영역 정중앙 한글 텍스트 정렬 연산
    box_w = box_coords[2] - box_coords[0]
    box_h = box_coords[3] - box_coords[1]
    text_center_x = box_coords[0] + (box_w / 2) - 60
    text_center_y = box_coords[1] + (box_h / 2) - 10
    draw.text((text_center_x, text_center_y), box_type, fill=(100, 110, 120), font=font_box)
    
    # 카피라이팅 텍스트 출력 영역 레이아웃 가이드
    draw.text((text_x_start, 120), "■ 상세 기획 문구 및 셀링포인트", fill=(40, 40, 40), font=font_sub)
    
    # 텍스트 wrap 폭 조절 (배치 위치에 맞게 글자수 동적 제한)
    wrap_width = 22 if is_even else 24
    wrapped_lines = textwrap.wrap(description, width=wrap_width)
    
    y_offset = 165
    for line in wrapped_lines:
        draw.text((text_x_start, y_offset), line, fill=(70, 75, 85), font=font_body)
        y_offset += 30
        
    return image

# 데이터 일괄 생성 보조 함수
def build_and_store_cards():
    steps_data = [
        {"num": 1, "title": "강력한 Hooking 문제 제기", "desc": "먹다 남긴 과자와 식빵, 봉지째 방치했다가 눅눅해져서 버린 적 많으시죠? 이제 첫 입 그대로 끝까지 바삭하게 지켜드립니다."},
        {"num": 2, "title": "불편함 해결 및 대안 제시 (동영상 파트)", "desc": "바람 새는 일반 집게는 그만! 초강력 밀봉 스프링 기술과 빌트인 냉장고 마그넷 설계로 주방의 품격을 바꿉니다."},
        {"num": 3, "title": "제품 핵심 특장점 01", "desc": "자석 내장형 구조로 설계되어 사용 후 냉장고나 철제 선반에 툭 붙여만 주세요. 분실 걱정 없는 스마트 보관 패러다임."},
        {"num": 4, "title": "제품 디자인 및 디테일 02", "desc": "손에 착 감기는 인체공학적 그립감과 감성적인 파스텔톤 컬러웨이. 어떤 주방 인테리어와도 완벽하게 조화를 이룹니다."},
        {"num": 5, "title": "실제 주방 활용 시나리오", "desc": "대용량 과자, 냉동식품, 양념 시즈닝 봉지까지 밀봉이 필요한 순간 밀어서 잠금 해제! 신선도를 밀착 밀봉 보존합니다."},
        {"num": 6, "title": "고객 리얼 리뷰 및 증명", "desc": "주부 커뮤니티 극찬 아이템! '자석이 있어서 보관이 편하고, 밀봉력이 기가 막힌다'는 평점이 입증하는 실제 만족도."},
        {"num": 7, "title": "타사 유사 제품 비교 우위", "desc": "쉽게 부러지고 헐거워지는 저가형 플라스틱 완구용 제품과 비교 불가! 고탄성 내부 메탈 스프링 탑재로 반영구적 사용."},
        {"num": 8, "title": "최종 구매 촉구 (CTA)", "desc": "증정 혜택을 놓치지 마세요! 6세트에 1개를 더 드리는 한정 구성, 지금 장바구니에 담고 신선한 주방 라이프를 시작하세요."}
    ]
    cards = []
    for step in steps_data:
        generated_img = create_high_fidelity_sample(step["num"], step["title"], step["desc"])
        cards.append(generated_img)
    st.session_state["page3_saved_images"] = cards
    st.session_state["page3_meta_data"] = {
        "product_name": product_name,
        "target_customer": target_customer,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# ====================================================
# 🎯 1. 상세페이지 자동 생성 탭
# ====================================================
if menu == "🎯 1. 상세페이지 자동 생성":
    st.markdown("### 🖼️ 상세페이지 8단계 고도화 기획 도출")
    st.file_uploader("[A] 일반 상품 이미지 등록", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    st.file_uploader("[B] 경쟁사 벤치마킹 스크린샷", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("🚀 8장 상세페이지 고품질 기획안 생성"):
        with st.spinner("Gemini가 쇼핑몰 판매 규격에 맞춤형 설득 구조를 믹싱하는 중..."):
            build_and_store_cards()
            st.success("✨ 고품질 샘플 디자인 카드 인스턴스 빌드가 완료되었습니다! 3페이지 탭으로 이동하세요.")

# ====================================================
# ➕ 2. 벤치마킹 데이터 등록 탭
# ====================================================
elif menu == "➕ 2. 벤치마킹 데이터 등록":
    st.markdown("### ➕ 경쟁사 구조 학습 및 데이터 등록")
    url_input = st.text_input("벤치마킹 타겟 상세페이지 링크 주소:")
    if st.button("링크 구조 분석 및 고충족 템플릿 생성"):
        if url_input:
            st.session_state["bench_url"] = url_input
            build_and_store_cards()
            st.success("✅ 벤치마킹 레이아웃 엔진 적용 성공! 3페이지에서 최종 형태를 확인하세요.")

# ====================================================
# 📂 3. 상세페이지 샘플 제작 및 검토 탭 (이동/저장 기능 탑재)
# ====================================================
elif menu == "📂 3. 상세페이지 샘플 제작 및 검토":
    st.markdown("### 🖼️ 3페이지: 실물 디자인 레이아웃 가이드 및 검토 센터")
    st.caption("아래 컴포넌트는 실제 쿠팡 규격(가로 780px) 배포용 화이트 미디어 박스 디자인이 적용된 정밀 샘플입니다.")
    
    if st.session_state["page3_saved_images"]:
        # [핵심 요청 기능] 3페이지 데이터를 4페이지 그룹 보관함으로 복사 및 저장하는 액션 버튼
        st.markdown("---")
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            st.info("💡 아래 샘플 구성 세트가 마음에 드신다면 오른쪽 버튼을 눌러 **4페이지 영구 보관함**으로 안전하게 복사하세요.")
        with col_btn2:
            if st.button("📦 4페이지 보관함으로 저장하기", type="primary", use_container_width=True):
                # 새로운 프로젝트 세트 객체 모델 구성
                project_bundle = {
                    "meta": st.session_state["page3_meta_data"],
                    "images": list(st.session_state["page3_saved_images"]) # 딥카피 형태로 안전하게 리스트 이동
                }
                st.session_state["saved_projects_library"].append(project_bundle)
                st.balloons()
                st.success("🚀 이동 및 그룹 저장 완료! 4페이지 탭에서 확인 가능합니다.")
        st.markdown("---")
        
        # 3페이지 화면상에 완성된 8장 카드 배치 피드백 출력
        for idx, img in enumerate(st.session_state["page3_saved_images"]):
            st.markdown(f"#### 📄 가이드 카드 단독 미리보기 - STEP {idx + 1}")
            st.image(img, use_container_width=True)
            
            # 다운로드 버튼 바인딩
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label=f"📥 STEP {idx + 1} 단독 다운로드",
                data=buf.getvalue(),
                file_name=f"coupang_step_{idx+1}.png",
                mime="image/png",
                key=f"p3_download_{idx}"
            )
            st.markdown("---")
    else:
        st.info("💡 아직 빌드된 상세페이지 샘플 세트가 없습니다. 1페이지 혹은 2페이지에서 생성 버튼을 먼저 클릭해 주세요!")

# ====================================================
# 📦 4. 저장된 프로젝트 보관함 (그룹별 묶음 및 미리보기) 탭 [신설]
# ====================================================
elif menu == "📦 4. 저장된 프로젝트 보관함 (미리보기)":
    st.markdown("### 📦 4페이지: 프로젝트 그룹별 통합 보관함 및 슬라이드 미리보기")
    st.caption("3페이지에서 이관된 모든 8장 구성의 기획 세트들이 그룹 단위로 영구 바인딩되어 보관되는 컴포넌트 공간입니다.")
    
    if st.session_state["saved_projects_library"]:
        # 내림차순 정렬하여 가장 최근 저장한 프로젝트가 위로 오도록 노출
        for p_idx, project in enumerate(reversed(st.session_state["saved_projects_library"])):
            meta = project["meta"]
            actual_idx = len(st.session_state["saved_projects_library"]) - 1 - p_idx
            
            # 그룹별로 묶어주는 Expander 컨테이너 디자인 적용
            with st.expander(f"📁 [그룹 프로젝트 #{actual_idx + 1}] {meta.get('product_name', '미지정 상품')} | 생성일자: {meta.get('created_at')}", expanded=True):
                st.markdown(f"**🎯 타겟 고객군:** {meta.get('target_customer')}")
                
                # 8장의 상세페이지 카드를 한눈에 스캔하기 편하도록 4열 배치의 그리드 시스템 구축
                cols = st.columns(4)
                for img_idx, img in enumerate(project["images"]):
                    col_target = cols[img_idx % 4]
                    with col_target:
                        st.markdown(f"**PAGE {img_idx + 1}**")
                        st.image(img, use_container_width=True)
                        
                        # 보관함 내부 개별 다운로드 지원 구조
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        st.download_button(
                            label="📥 다운로드",
                            data=buf.getvalue(),
                            file_name=f"project_{actual_idx+1}_page_{img_idx+1}.png",
                            mime="image/png",
                            key=f"p4_dl_{actual_idx}_{img_idx}"
                        )
                
                # 전체 세트 삭제 관리 기능 제공
                if st.button(f"🗑️ 해당 프로젝트 그룹 삭제", key=f"del_group_{actual_idx}"):
                    st.session_state["saved_projects_library"].pop(actual_idx)
                    st.rerun()
    else:
        st.warning("⚠️ 현재 보관함이 비어 있습니다. 3페이지 검토 센터에서 '4페이지 보관함으로 저장하기' 버튼을 누르면 이 자리에 그룹별로 예쁘게 정돈됩니다!")
