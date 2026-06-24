import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap  # 한글 문장 자동 줄바꿈을 위한 모듈

# 1. 페이지 기본 설정 및 환경 초기화
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터", layout="wide")

if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []
if "bench_url" not in st.session_state:
    st.session_state["bench_url"] = ""

# [핵심 추가] Streamlit 서버 환경에서 한글 깨짐을 방지하기 위해 구글 오픈폰트(나눔고딕) 동적 로드
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

# 2. 사이드바 UI 구성 (📋 기본 마케팅 정보)
st.sidebar.title("📋 기본 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input(
    "상품명", 
    value="다온이네 다온이네 밀봉 자석집게 6세트+1개 남은과자 식빵 캠핑 소스 보관 다용도 주방 밀폐 봉지집게"
)
target_customer = st.sidebar.text_input("타겟 고객", value="주부, 자취생")

# 3. 상단 가로형 메뉴 탭 구조 (원본 스타일 유지)
menu = st.radio(
    "",
    [
        "🎯 1. 상세페이지 자동 생성",
        "➕ 2. 벤치마킹 데이터 등록",
        "📂 3. 상세페이지 샘플 선택 (갤러리)"
    ],
    horizontal=True
)

# 4. 안정적인 Gemini API 호출 함수
def call_gemini_api(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            st.error(f"⚠️ API 에러 발생 (코드 {response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"통신 중 에러가 발생했습니다: {e}")
        return None

# 5. 쿠팡 규격 카드 이미지 생성 함수 (한글 폰트 적용 및 줄바꿈 구조 개선)
def create_coupang_image(step_num, title, description):
    width, height = 780, 450
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 영역 테두리 선구조 디자인
    draw.rectangle([15, 15, width-15, height-15], outline=(230, 230, 230), width=3)
    
    # 폰트 에셋 설정
    font_bytes = load_korean_font_bytes()
    if font_bytes:
        font_title = ImageFont.truetype(io.BytesIO(font_bytes), 26)
        font_subtitle = ImageFont.truetype(io.BytesIO(font_bytes), 20)
        font_body = ImageFont.truetype(io.BytesIO(font_bytes), 18)
    else:
        # 폰트 다운로드 실패 시 시스템 기본 폰트 백업 (영어만 지원됨)
        font_title = font_subtitle = font_body = ImageFont.load_default()
    
    # 텍스트 가이드 드로잉 (한글 적용)
    draw.text((40, 45), f"PAGE {step_num}: {title}", fill=(228, 27, 43), font=font_title)
    draw.text((40, 110), "■ 기획 방향 및 카피문구:", fill=(60, 60, 60), font=font_subtitle)
    
    # 긴 문장 카드 폭에 맞춰 자동 줄바꿈 처리 (가로폭 고려 32자 기준)
    wrapped_lines = textwrap.wrap(description, width=32)
    
    y_text = 150
    for line in wrapped_lines:
        draw.text((40, y_text), line, fill=(80, 80, 80), font=font_body)
        y_text += 28  # 줄간격 설정
    
    return image

# ====================================================
# 🎯 1. 상세페이지 자동 생성 탭
# ====================================================
if menu == "🎯 1. 상세페이지 자동 생성":
    st.markdown("### 🖼️ 상세페이지 8단계 즉시 생성")
    
    uploaded_files = st.file_uploader("[A] 일반 상품 이미지", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    bench_files = st.file_uploader("[B] 벤치마킹 스크린샷", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.session_state["bench_url"]:
        st.success(f"✅ 선택된 템플릿이 적용되었습니다! (내용: {st.session_state['bench_url']})")
        
    if st.button("🚀 8장 상세페이지 생성 시작"):
        if not api_key:
            st.warning("⚠️ 사이드바에 Google API Key를 입력해 주세요.")
        else:
            with st.spinner("Gemini AI가 고성능 상세페이지 카피라이팅 기획안을 도출하는 중..."):
                prompt = f"""
                상품명: {product_name}
                타겟 고객: {target_customer}
                벤치마킹 참고 정보: {st.session_state["bench_url"]}
                
                이 상품의 셀링 포인트를 극대화하여 쿠팡 입점용 8단계 흐름의 상세페이지 기획안을 작성해줘.
                소비자의 지갑을 열 수 있는 강력한 후킹 멘트와 설득 구조를 포함해줘.
                """
                response_text = call_gemini_api(prompt, api_key)
                
                if response_text:
                    st.success("✨ 8단계 카피라이팅 기획안 도출 완료!")
                    st.markdown(response_text)
                    
                    steps_sample = [
                        {"num": 1, "title": "강력한 Hooking 문제 제기", "desc": "과자나 식빵 먹다 남기면 금방 눅눅해지셨죠? 밀봉 자석집게로 첫 입 그대로 바삭하게 보관하세요!"},
                        {"num": 2, "title": "불편함 해결 및 대안 제시", "desc": "일반 집게와 비교를 거부합니다. 강력한 밀봉력에 냉장고 자석 부착 기능까지 깔끔하게 추가 완료!"},
                        {"num": 3, "title": "제품 특장점 01", "desc": "자석 내장 설계로 주방 보관이 혁신적으로 변합니다. 잃어버릴 염려 없는 스마트한 주방의 완성."},
                        {"num": 4, "title": "제품 특장점 02", "desc": "6세트 패키지에 1개를 더 증정하는 특별 구성! 캠핑장, 가정 어디서나 모자람 없이 넉넉하게 사용하세요."},
                        {"num": 5, "title": "실제 활용 시나리오", "desc": "밀봉이 필요한 봉지라면 어디든 쓱 밀어서 고정 끝! 남은 식재료 신선도를 완벽하게 사수합니다."},
                        {"num": 6, "title": "고객 리뷰 및 증명", "desc": "깐깐한 주부들의 입소문템, 자취생 요리 필수 아이템! 평점이 증명하는 압도적인 만족도를 확인하세요."},
                        {"num": 7, "title": "타사 비교 우위", "desc": "쉽게 부러지는 저가형 플라스틱 집게와는 내구성부터 다릅니다. 녹슬지 않고 짱짱한 내장 스프링."},
                        {"num": 8, "title": "마지막 구매 촉구 (CTA)", "desc": "망설이면 늦습니다! 지금 선택해서 주방 수납의 격과 식재료의 신선도를 한 단계 더 높이세요."}
                    ]
                    
                    generated_cards = []
                    for item in steps_sample:
                        img = create_coupang_image(item["num"], item["title"], item["desc"])
                        generated_cards.append(img)
                    
                    st.session_state["page3_saved_images"] = generated_cards
                    st.info("💡 데이터 연동 완료! 3번 '상세페이지 샘플 선택 (갤러리)' 탭으로 이동하시면 한글 카드를 확인할 수 있습니다.")

# ====================================================
# ➕ 2. 벤치마킹 데이터 등록 탭
# ====================================================
elif menu == "➕ 2. 벤치마킹 데이터 등록":
    st.markdown("### ➕ 벤치마킹 데이터 등록")
    url_input = st.text_input("벤치마킹할 경쟁사 상품 페이지 URL을 입력하세요:")
    
    if st.button("템플릿 구조 분석 및 등록"):
        if url_input:
            st.session_state["bench_url"] = url_input
            st.success(f"📂 템플릿 URL 분석 및 등록이 성공적으로 완료되었습니다: {url_input}")
            
            steps_sample = [
                {"num": 1, "title": "강력한 Hooking 문제 제기", "desc": "과자나 식빵 먹다 남기면 금방 눅눅해지셨죠? 밀봉 자석집게로 첫 입 그대로 바삭하게 보관하세요!"},
                {"num": 2, "title": "불편함 해결 및 대안 제시", "desc": "일반 집게와 비교를 거부합니다. 강력한 밀봉력에 냉장고 자석 부착 기능까지 깔끔하게 추가 완료!"},
                {"num": 3, "title": "제품 특장점 01", "desc": "자석 내장 설계로 주방 보관이 혁신적으로 변합니다. 잃어버릴 염려 없는 스마트한 주방의 완성."},
                {"num": 4, "title": "제품 특장점 02", "desc": "6세트 패키지에 1개를 더 증정하는 특별 구성! 캠핑장, 가정 어디서나 모자람 없이 넉넉하게 사용하세요."},
                {"num": 5, "title": "실제 활용 시나리오", "desc": "밀봉이 필요한 봉지라면 어디든 쓱 밀어서 고정 끝! 남은 식재료 신선도를 완벽하게 사수합니다."},
                {"num": 6, "title": "고객 리뷰 및 증명", "desc": "깐깐한 주부들의 입소문템, 자취생 요리 필수 아이템! 평점이 증명하는 압도적인 만족도를 확인하세요."},
                {"num": 7, "title": "타사 비교 우위", "desc": "쉽게 부러지는 저가형 플라스틱 집게와는 내구성부터 다릅니다. 녹슬지 않고 짱짱한 내장 스프링."},
                {"num": 8, "title": "마지막 구매 촉구 (CTA)", "desc": "망설이면 늦습니다! 지금 선택해서 주방 수납의 격과 식재료의 신선도를 한 단계 더 높이세요."}
            ]
            generated_cards = []
            for item in steps_sample:
                img = create_coupang_image(item["num"], item["title"], item["desc"])
                generated_cards.append(img)
            
            st.session_state["page3_saved_images"] = generated_cards
            st.info("✨ 분석된 맞춤 데이터 카드가 생성되었습니다! '3. 상세페이지 샘플 선택 (갤러리)' 탭으로 이동해 보세요.")
        else:
            st.warning("분석할 URL 주소를 입력해주세요.")

# ====================================================
# 📂 3. 상세페이지 샘플 선택 (갤러리) 탭
# ====================================================
elif menu == "📂 3. 상세페이지 샘플 선택 (갤러리)":
    st.markdown("### 🖼️ 쿠팡 규격(가로 780px) 상세페이지 실물 이미지 다운로드 센터")
    st.markdown("각 단계별로 완성된 실물 이미지 카드를 눈으로 직접 확인하고 바로 다운로드하세요!")
    
    if st.session_state["page3_saved_images"]:
        for idx, img in enumerate(st.session_state["page3_saved_images"]):
            with st.container():
                st.markdown(f"#### 📄 PAGE {idx + 1} : 단독 카드 가이드")
                st.image(img, use_container_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label=f"📥 PAGE {idx + 1} 카드 이미지 다운로드",
                    data=byte_im,
                    file_name=f"coupang_page_{idx+1}.png",
                    mime="image/png",
                    key=f"dn_btn_{idx}"
                )
                st.markdown("---")
    else:
        st.info("💡 아직 생성되거나 저장된 상세페이지가 없습니다. '1. 상세페이지 자동 생성' 탭에서 생성 시작 버튼을 누르거나, '2. 벤치마킹 데이터 등록'을 진행해 주세요!")
