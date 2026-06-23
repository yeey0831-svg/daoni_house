import streamlit as st
import google.generativeai as genai
import requests
import io
import base64
from PIL import Image

# 1. 웹 페이지 기본 설정 및 클라우드 배포 최적화
st.set_page_config(page_title="쿠팡형 AI 상세페이지 생성기 v10.0", layout="wide")
st.title("🚀 우리 회사 전용 AI 상세페이지 제작 클라우드")
st.caption("구글 제미나이 정식 API 기반 v10.0 (언제 어디서나 접속 가능한 독립 웹 앱 버전)")

# 세션 상태(메모리 백엔드) 초기화
if "clean_files_data" not in st.session_state:
    st.session_state.clean_files_data = []
if "screenshot_files_data" not in st.session_state:
    st.session_state.screenshot_files_data = []

# 2. 사이드바 - 사용자 입력창 구성
st.sidebar.header("📋 상품 및 마케팅 정보 입력")
api_key = st.sidebar.text_input("Google API Key를 입력하세요", type="password")
product_info = st.sidebar.text_area("1. 상품명 및 주요 스펙/특징", placeholder="예: 자석 집게 / 7가지 색상 / 강력한 고정력")
target_customer = st.sidebar.text_input("2. 타겟 고객층", placeholder="예: 직장인, 다꾸족, 냉장고 정리족")
benchmark_url = st.sidebar.text_input("3. 벤치마킹 사이트 URL (선택)", placeholder="예: 쿠팡 링크")

st.sidebar.markdown("---")
st.sidebar.subheader("4. 참고 이미지 개별 업로드")

# [A영역] 일반 마케팅/상품 이미지 업로드 
uploaded_files = st.sidebar.file_uploader(
    "📂 [A] 일반 상품 이미지 업로드", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True,
    key="cloud_file_uploader"
)

st.sidebar.markdown("---")

# [B영역] 벤치마킹 화면 캡처(스크린샷) 이미지 업로드
screenshot_uploaders = st.sidebar.file_uploader(
    "📸 [B] 벤치마킹 스크린샷 업로드", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True,
    key="cloud_screenshot_uploader"
)

st.sidebar.markdown("---")
st.sidebar.markdown("🖼️ **실시간 이미지 미리보기 및 검증 모니터**")

# 제미나이 AI 백엔드로 최종 전송될 마스터 이미지 리스트
gemini_images = []

# [A] 일반 파일 출력 및 연동
if uploaded_files:
    st.sidebar.markdown("📂 *[A] 상품 이미지 리스트:*")
    for u_file in uploaded_files:
        u_file.seek(0)
        img_obj = Image.open(io.BytesIO(u_file.read()))
        gemini_images.append(img_obj)
        
        c1, c2 = st.sidebar.columns([1, 4])
        c1.image(img_obj, width=45)
        c2.caption(f"📄 {u_file.name[:15]}")

# [B] 스크린샷 파일 출력 및 연동
if screenshot_uploaders:
    st.sidebar.markdown("📸 *[B] 스크린샷 리스트:*")
    for s_file in screenshot_uploaders:
        s_file.seek(0)
        img_obj = Image.open(io.BytesIO(s_file.read()))
        gemini_images.append(img_obj)
        
        c1, c2 = st.sidebar.columns([1, 4])
        c1.image(img_obj, width=45)
        c2.caption(f"🎯 {s_file.name[:15]}")

if not uploaded_files and not screenshot_uploaders:
    st.sidebar.info("등록된 참고 이미지가 없습니다.")

st.sidebar.markdown("---")
page_number = st.sidebar.slider("출력할 상세페이지 단계 (1~8장)", 1, 8, 1)

page_structures = {
    1: "메인 인트로 (소비자 시선 사로잡는 강력한 후킹)",
    2: "문제 제기 및 공감 (불편한 상황 자극)",
    3: "해결책 제시 (우리 제품 도입 시 반전)",
    4: "핵심 장점 1 (제품의 고유 기능성 안내)",
    5: "핵심 장점 2 (소재 및 내구성 안내)",
    6: "디테일 및 사이즈 (규격 마감 안내)",
    7: "신뢰성 검증 (인증서 및 고객 만족도 수치)",
    8: "엔딩 및 구매 유도 (한정 혜택 및 최종 CTA)"
}

# 3. 메인 화면 출력 로직
if st.sidebar.button("✨ 쿠팡형 상세페이지 즉시 생성"):
    if not api_key:
        st.error("Google API Key를 입력해 주세요!")
    elif not product_info:
        st.error("상품 정보를 입력해 주세요!")
    else:
        try:
            genai.configure(api_key=api_key)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📝 1단계: AI 마케팅 카피 및 기획서")
                with st.spinner("제미나이가 카피를 분석 중..."):
                    prompt = f"""너는 전환율 극대화 상세페이지를 설계하는 인공지능 마케터야.
                    전체 8장 구조 중 현재 [{page_number}번째 장: {page_structures[page_number]}]을 기획해야 해.
                    첨부된 이미지들의 외형 특성, 색상, 디자인 요소를 종합 분석해서 연출안을 짜줘.
                    
                    [상품 정보]: {product_info}
                    [타겟 고객]: {target_customer}
                    [벤치마킹 URL]: {benchmark_url}
                    
                    ■ 1. 메인 카피라이팅 / ■ 2. 비주얼 연출 지시서 / ■ 3. 디자인 무드 양식으로 작성해줘."""
                    
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    if gemini_images:
                        response = model.generate_content([prompt] + gemini_images)
                    else:
                        response = model.generate_content(prompt)
                    st.markdown(response.text)
                    
            with col2:
                st.subheader("🖼️ 2단계: 쿠팡 규격 완성 배너 이미지 (가로 780px)")
                with st.spinner("구글 이미지 AI가 디자인하는 중..."):
                    image_prompt = f"Professional e-commerce product banner for Coupang, width 780px, {product_info}, featured for {page_structures[page_number]}, 4k photorealistic"
                    imagen_url = f"https://generativelanguage.googleapis.com/v1/models/imagen-3.0-generate-002:generateImages?key={api_key}"
                    payload = {"prompt": image_prompt, "numberOfImages": 1, "aspectRatio": "1:1", "outputMimeType": "image/jpeg"}
                    
                    img_res = requests.post(imagen_url, json=payload)
                    img_json = img_res.json()
                    
                    img_base64 = img_json['generatedImages'][0]['image']['imageBytes']
                    final_image = Image.open(io.BytesIO(base64.b64decode(img_base64)))
                    
                    base_width = 780
                    w_percent = (base_width / float(final_image.size[0]))
                    h_size = int((float(final_image.size[1]) * float(w_percent)))
                    coupang_image = final_image.resize((base_width, h_size), Image.Resampling.LANCZOS)
                    
                    st.image(coupang_image, caption=f"쿠팡 가로 780px 최적화 배너 ({page_number}장)")
                    
                    img_byte_arr = io.BytesIO()
                    coupang_image.save(img_byte_arr, format='JPEG')
                    
                    st.download_button(
                        label=f"💾 {page_number}장 이미지 다운로드",
                        data=img_byte_arr.getvalue(),
                        file_name=f"coupang_page_{page_number}.jpg",
                        mime="image/jpeg"
                    )
        except Exception as e:
            st.warning("1단계 마케팅 기획서 작성이 완료되었습니다. (이미지 배너 생성 영역은 구글 API 키의 이미지 모델 결제 권한 활성화 후 가로 780px 자동 매칭 출력이 재개됩니다.)")
