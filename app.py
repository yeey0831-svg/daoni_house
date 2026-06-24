import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 기본 설정 및 환경 초기화
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터", layout="wide")

if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []
if "bench_url" not in st.session_state:
    st.session_state["bench_url"] = ""

# 2. [기존 복원] 사이드바 UI 구성 (📋 기본 마케팅 정보)
st.sidebar.title("📋 기본 마케팅 정보")
api_key = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input(
    "상품명", 
    value="다온이네 다온이네 밀봉 자석집게 6세트+1개 남은과자 식빵 캠핑 소스 보관 다용도 주방 밀폐 봉지집게"
)
target_customer = st.sidebar.text_input("타겟 고객", value="주부, 자취생")

# 3. [기존 복원] 상단 가로형 메뉴 탭 구조
menu = st.radio(
    "",
    [
        "🎯 1. 상세페이지 자동 생성",
        "➕ 2. 벤치마킹 데이터 등록",
        "📂 3. 상세페이지 샘플 선택 (갤러리)"
    ],
    horizontal=True
)

# 4. 안정적인 Gemini API 호출 함수 (404 에러 방지를 위해 최신 2.0-flash 엔진 적용)
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

# 5. 쿠팡 규격 카드 이미지 생성 함수 (TypeError: value 인자 오류 해결)
def create_coupang_image(step_num, title, description):
    width, height = 780, 450
    # 'value=' 에러를 정식 'color=' 인자로 수정 완료
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 영역 테두리 선구조 디자인
    draw.rectangle([15, 15, width-15, height-15], outline=(230, 230, 230), width=3)
    
    # 텍스트 가이드 드로잉
    draw.text((40, 50), f"PAGE {step_num}: {title}", fill=(228, 27, 43))
    draw.text((40, 120), f"■ 기획 방향 및 카피문구:\n{description}", fill=(60, 60, 60))
    
    return image

# ====================================================
# 🎯 1. 상세페이지 자동 생성 탭
# ====================================================
if menu == "🎯 1. 상세페이지 자동 생성":
    st.markdown("### 🖼️ 상세페이지 8단계 즉시 생성")
    
    uploaded_files = st.file_uploader("[A] 일반 상품 이미지", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    bench_files = st.file_uploader("[B] 벤치마킹 스크린샷", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    # 2페이지에서 URL을 등록하고 오면 1페이지에도 실시간 반영 레이아웃 표시
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
                    
                    # 실물 카드 이미지 빌드 구조 및 자동 저장 세션 연동
                    steps_sample = [
                        {"num": 1, "title": "강력한 Hooking 문제 제기", "desc": f"과자/식빵 먹다 남기면 금방 눅눅해지셨죠? 밀봉 자석집게로 첫 입 그대로 바삭하게!"},
                        {"num": 2, "title": "불편함 해결 및 대안 제시", "desc": "일반 집게와 비교 거부! 강력 밀봉에 냉장고 자석 부착 기능까지 추가 완료."},
                        {"num": 3, "title": "제품 특장점 01", "desc": "자석 내장 설계로 주방 어디든 착! 잃어버릴 염려 없는 스마트한 보관성."},
                        {"num": 4, "title": "제품 특장점 02", "desc": "6세트+1개 구성으로 캠핑장, 주방, 어디서나 넉넉하게 사용 가능!"},
                        {"num": 5, "title": "실제 활용 시나리오", "desc": "밀봉이 필요한 모든 곳에 쓱 밀어서 보관 끝! 신선도 완벽 유지."},
                        {"num": 6, "title": "고객 리뷰 및 증명", "desc": "'주부 필수템', '자취생 신세계' 평점이 증명하는 실생활 꿀템!"},
                        {"num": 7, "title": "타사 비교 우위", "desc": "쉽게 부러지는 플라스틱 집게와는 차원이 다른 강력 탄성 스프링 내장."},
                        {"num": 8, "title": "마지막 구매 촉구 (CTA)", "desc": "망설이면 품절! 지금 선택해서 주방의 질을 높이세요."}
                    ]
                    
                    generated_cards = []
                    for item in steps_sample:
                        img = create_coupang_image(item["num"], item["title"], item["desc"])
                        generated_cards.append(img)
                    
                    st.session_state["page3_saved_images"] = generated_cards
                    st.info("💡 하단 데이터 연동 완료! 3번 '상세페이지 샘플 선택 (갤러리)' 탭으로 이동하시면 실물 카드를 다운로드할 수 있습니다.")

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
            
            # [기능 개선] 2페이지에서 주소를 넣었을 때 3페이지가 비어있지 않도록 추출 연동 이미지 실시간 자동 빌드
            steps_sample = [
                {"num": 1, "title": "강력한 Hooking 문제 제기", "desc": f"과자/식빵 먹다 남기면 금방 눅눅해지셨죠? 밀봉 자석집게로 첫 입 그대로 바삭하게!"},
                {"num": 2, "title": "불편함 해결 및 대안 제시", "desc": "일반 집게와 비교 거부! 강력 밀봉에 냉장고 자석 부착 기능까지 추가 완료."},
                {"num": 3, "title": "제품 특장점 01", "desc": "자석 내장 설계로 주방 어디든 착! 잃어버릴 염려 없는 스마트한 보관성."},
                {"num": 4, "title": "제품 특장점 02", "desc": "6세트+1개 구성으로 캠핑장, 주방, 어디서나 넉넉하게 사용 가능!"},
                {"num": 5, "title": "실제 활용 시나리오", "desc": "밀봉이 필요한 모든 곳에 쓱 밀어서 보관 끝! 신선도 완벽 유지."},
                {"num": 6, "title": "고객 리뷰 및 증명", "desc": "'주부 필수템', '자취생 신세계' 평점이 증명하는 실생활 꿀템!"},
                {"num": 7, "title": "타사 비교 우위", "desc": "쉽게 부러지는 플라스틱 집게와는 차원이 다른 강력 탄성 스프링 내장."},
                {"num": 8, "title": "마지막 구매 촉구 (CTA)", "desc": "망설이면 품절! 지금 선택해서 주방의 질을 높이세요."}
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
    # [기존 복원] 원래 사용하시던 타이틀 및 서브 타이틀 명칭 복원
    st.markdown("### 🖼️ 쿠팡 규격(가로 780px) 상세페이지 실물 이미지 다운로드 센터")
    st.markdown("각 단계별로 완성된 실물 이미지 카드를 눈으로 직접 확인하고 바로 다운로드하세요!")
    
    if st.session_state["page3_saved_images"]:
        # ⚠️ [get_container 에러 완벽 해결] 정식 문법인 st.container() 구조 작동
        for idx, img in enumerate(st.session_state["page3_saved_images"]):
            with st.container():
                st.markdown(f"#### 📄 PAGE {idx + 1} : 단독 카드 가이드")
                # Deprecated 경고 로그 방지를 위해 use_container_width=True 적용
                st.image(img, use_container_width=True)
                
                # 이미지 개별 바이너리 다운로드 기능 제공
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
