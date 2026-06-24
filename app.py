import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 기본 설정
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v22.0", layout="wide")

# 세션 상태 초기화 (3페이지 저장소 연동용)
if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []

# 2. 사이드바 UI 구성
st.sidebar.title("📋 필수 정보 및 파일 업로드")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input(
    "상품명", 
    value="다온이네 다온이네 밀봉 자석집게 6세트+1개 남은과자 식빵 캠핑 소스 보관 다용도 주방 밀폐 봉지집게"
)
target_customer = st.sidebar.text_input("타겟 고객", value="주부, 자취생")

# 3. 메인 상단 타이틀 및 메뉴 탭
st.markdown("# 🚀 우리 회사 전용 AI 상세페이지 제작 클라우드")

menu = st.radio(
    "🏠 메뉴를 이동하며 실습하세요",
    [
        "🚀 1페이지: 기획안 고속 자동화",
        "🎨 2페이지: URL 기반 상세수집",
        "📂 3페이지: 추출 상세페이지 저장소"
    ],
    horizontal=True
)

# 4. Gemini API 호출 함수 (404 에러 해결을 위해 gemini-2.0-flash로 업데이트)
def call_gemini_api(prompt, api_key):
    # 만료된 1.5-flash 대신 2.0-flash 안정 버전을 호출합니다.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
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

# 5. 쿠팡 규격 카드 이미지 생성 함수 (TypeError 해결을 위해 color 인자 수정)
def create_coupang_image(step_num, title, description):
    width, height = 780, 450
    # 'value=' 대형 에러를 'color=' 정식 인자로 전면 수정
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 영역 테두리 그리기
    draw.rectangle([15, 15, width-15, height-15], outline=(230, 230, 230), width=3)
    
    # 텍스트 정보 그리기 (기본 폰트 fallback 구조)
    draw.text((40, 50), f"PAGE {step_num}: {title}", fill=(228, 27, 43))
    draw.text((40, 120), f"■ 기획 방향 및 카피문구:\n{description}", fill=(60, 60, 60))
    
    return image

# ====================================================
# 🚀 1페이지: 기획안 고속 자동화 화면
# ====================================================
if menu == "🚀 1페이지: 기획안 고속 자동화":
    st.subheader("🖼️ 상세페이지 8단계 즉시 생성")
    
    uploaded_files = st.file_uploader("[A] 일반 상품 이미지 (최대 5장)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        st.success(f"✅ 총 {len(uploaded_files)}장의 상품 이미지가 업로드 되었습니다.")
        
    if st.button("🚀 8장 상세페이지 생성 시작"):
        if not api_key:
            st.warning("⚠️ 사이드바에 Google API Key를 입력해 주세요.")
        else:
            with st.spinner("Gemini AI가 고성능 상세페이지 카피라이팅 기획안을 도출하는 중..."):
                prompt = f"""
                상품명: {product_name}
                타겟 고객: {target_customer}
                
                이 상품의 셀링 포인트를 극대화하여 쿠팡 입점용 8단계 흐름의 상세페이지 기획안을 작성해줘.
                소비자의 지갑을 열 수 있는 강력한 후킹 멘트와 설득 구조를 포함해줘.
                """
                response_text = call_gemini_api(prompt, api_key)
                
                if response_text:
                    st.success("✨ 8단계 카피라이팅 기획안 도출 완료!")
                    st.markdown(response_text)
                    
                    # 시뮬레이션용 이미지 카드 8단계 빌드 및 자동 세션 저장
                    steps_sample = [
                        {"num": 1, "title": "강력한 Hooking 문제 제기", "desc": f"과자/식빵 먹다 남기면 금방 눅눅해지셨죠? {product_name}으로 첫 입 그대로 바삭하게!"},
                        {"num": 2, "title": "불편함 해결 및 대안 제시", "desc": "일반 집게와 비교 거부! 강력 밀봉에 냉장고 자석 부착 기능까지 추가 완료."},
                        {"num": 3, "title": "제품 특장점 01", "desc": "자석 내장 설계로 주방 어디든 착! 잃어버릴 염려 없는 스마트한 보관성."},
                        {"num": 4, "title": "제품 특장점 02", "desc": "6세트+1개 초특가 구성으로 캠핑장, 주방, 아이방 어디서나 넉넉하게 사용 가능!"},
                        {"num": 5, "title": "실제 활용 시나리오", "desc": "밀봉이 필요한 모든 곳에 쓱 밀어서 보관 끝! 남은 식재료 신선도 완벽 유지."},
                        {"num": 6, "title": "고객 리뷰 및 증명", "desc": "'주부 필수템', '자취생 신세계' 평점 4.9점이 증명하는 실생활 꿀템!"},
                        {"num": 7, "title": "타사 비교 우위", "desc": "쉽게 부러지는 플라스틱 집게와는 차원이 다른 강력 탄성 스프링 내장."},
                        {"num": 8, "title": "마지막 구매 촉구 (CTA)", "desc": "망설이면 품절! 지금 다온이네 주방 밀봉 자석집게 세트로 주방의 질을 높이세요."}
                    ]
                    
                    generated_cards = []
                    st.markdown("### 🖼️ 실물 그래픽 카드 미리보기")
                    for item in steps_sample:
                        img = create_coupang_image(item["num"], item["title"], item["desc"])
                        generated_cards.append(img)
                        st.image(img, caption=f"Page {item['num']} 레이아웃 가이드")
                    
                    # 3페이지 저장소 탭으로 실시간 연동 처리
                    st.session_state["page3_saved_images"] = generated_cards

# ====================================================
# 🎨 2페이지: URL 기반 상세수집 화면
# ====================================================
elif menu == "🎨 2페이지: URL 기반 상세수집":
    st.subheader("🔗 벤치마킹 데이터 라이브러리")
    url_input = st.text_input("벤치마킹할 경쟁사 상품 페이지 URL을 입력하세요:")
    if st.button("템플릿 구조 분석 및 카피 추출"):
        if url_input:
            st.info("💡 해당 URL 구조 분석이 성공적으로 완료되었습니다! (추출 가상 데이터 적용)")
        else:
            st.warning("분석할 URL 주소를 입력해주세요.")

# ====================================================
# 📂 3페이지: 추출 상세페이지 저장소 화면
# ====================================================
elif menu == "📂 3페이지: 추출 상세페이지 저장소":
    st.subheader("📂 3페이지: 라이브러리 및 실물 이미지 다운로드 센터")
    
    if st.session_state["page3_saved_images"]:
        st.success(f"현재 총 {len(st.session_state['page3_saved_images'])}개의 고해상도 상세페이지 가이드가 저장소에 안전하게 보관 중입니다.")
        
        # ⚠️ [수정 완료] st.get_container() 에러를 정식 st.container()로 전면 수정!
        for idx, img in enumerate(st.session_state["page3_saved_images"]):
            with st.container():
                st.markdown(f"### 📄 PAGE {idx + 1} 단독 카드")
                st.image(img, use_container_width=True)
                
                # 개별 파일 다운로드 기능 제공
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
        st.info("💡 아직 생성되거나 저장된 상세페이지가 없습니다. '1페이지' 메뉴로 이동하여 생성 시작 버튼을 눌러주세요!")
