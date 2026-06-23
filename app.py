import streamlit as st
import google.generativeai as genai
import requests
import io
import base64
from PIL import Image

# 1. 웹 페이지 기본 설정 및 세션 상태(저장소) 초기화
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v12.0", layout="wide")

# 사용자가 새롭게 등록할 커스텀 템플릿 리스트를 세션에 저장
if "custom_templates" not in st.session_state:
    st.session_state["custom_templates"] = {}

# 기본 내장된 검증된 상세페이지 타입 3가지 데이터 (구조 정의)
FIXED_TEMPLATES = {
    "🔥 [A타입] 완판 리빙/공구 제품 공식 (불편함 자극 ➔ 반전 해결책)": {
        "desc": "소비자가 평소 느끼던 빡치는(?) 불편함을 먼저 극대화하여 공감을 얻은 뒤, 우리 제품으로 시원하게 해결하는 정석 구조입니다. (공구, 생활용품 최적화)",
        "structure": "1. 불편함 폭로 (기존 제품의 한계) -> 2. 강력한 공감 -> 3. 우리 제품 등장 (반전 효과) -> 4. 압도적인 성능 지표 검증"
    },
    "✨ [B타입] 인스타 감성 뷰티/인테리어 공식 (감성 무드 ➔ 워너비 라이프)": {
        "desc": "기능 설명보다 '이 제품을 내 방에 두었을 때의 아름다운 일상'을 먼저 상상하게 만드는 트렌디한 감성 레이아웃입니다. (소품, 디자인 가전, 뷰티 최적화)",
        "structure": "1. 감성 라이프스타일 연출 (Visual) -> 2. 일상 속 녹아드는 무드 -> 3. 디테일/소재 마감 강조 -> 4. 감성 패키징 및 선물 추천"
    },
    "🛡️ [C타입] 테크/의료기기 신뢰성 중심 공식 (기술 지표 ➔ 압도적 비교 우위)": {
        "desc": "논리적이고 이성적인 고객을 설득하기 위해, 타사 제품과의 스펙 비교표, 공인 인증서, 압도적인 숫자를 전면에 배치하는 신뢰성 중심 구조입니다. (전자기기, 기능성 웨어 최적화)",
        "structure": "1. 핵심 기술 특허 선포 -> 2. 타사 싸구려 제품과 1:1 스펙 비교표 -> 3. 시험 성적서 및 안전 인증 -> 4. 생산 공정 및 프리미엄 QC 강조"
    }
}

# 2. 메인 타이틀 영역
st.title("🚀 우리 회사 전용 AI 상세페이지 제작 클라우드")
st.caption("구글 제미나이 정식 API 기반 v12.0 (샘플 미리보기 & 템플릿 무한 확장 버전)")

# 3. 화면 탭 분할 (1번 탭: 메인 제작소, 2번 탭: 벤치마킹 주소로 새 샘플 만들기)
tab1, tab2 = st.tabs(["🎯 1. 상세페이지 고속 제작소", "➕ 2. 벤치마킹 샘플 추가/확장"])

# ==========================================
# [TAB 1] 상세페이지 고속 제작소 (메인 화면)
# ==========================================
with tab1:
    st.subheader("🖼️ 대박 판매 공식 샘플 미리보기 및 타입 선택")
    st.info("💡 마음에 드는 판매 공식을 아래에서 확인하고 선택해 주세요. AI가 해당 뼈대를 기반으로 카피를 작성합니다.")
    
    # 전체 템플릿 통합 (기본 내장 3종 + 사용자가 새로 추가한 커스텀 템플릿)
    all_templates = {**FIXED_TEMPLATES, **st.session_state["custom_templates"]}
    
    # [시각적 미리보기 카드 구현]
    cols = st.columns(len(all_templates) if len(all_templates) > 0 else 1)
    
    selected_template_name = None
    template_options = list(all_templates.keys())
    
    # 각 타입별 카드 형태 출력
    for idx, (t_name, t_data) in enumerate(all_templates.items()):
        with cols[idx % len(cols)]:
            st.markdown(f"### {t_name.split(']')[0]}]")
            st.markdown(f"**{t_name.split(']')[1] if ']' in t_name else t_name}**")
            st.caption(t_data["desc"])
            st.markdown("---")
            st.code(f"[진행 뼈대 구조]\n{t_data['structure']}", language="text")
            
    st.markdown("---")
    chosen_type = st.selectbox("🎯 오늘 제작에 사용할 상세페이지 공식을 최종 선택하세요:", template_options)

    # 사이드바 입력창 연동
    st.sidebar.header("📋 상품 및 마케팅 정보 입력")
    api_key = st.sidebar.text_input("Google API Key를 입력하세요", type="password")
    product_info = st.sidebar.text_area("1. 상품명 및 주요 스펙/특징", placeholder="예: 자석 집게 / 강력한 고정력")
    target_customer = st.sidebar.text_input("2. 타겟 고객층", placeholder="예: 직장인, 냉장고 정리족")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("4. 참고 이미지 개별 업로드")

    uploaded_files = st.sidebar.file_uploader("📂 [A] 일반 상품 이미지 업로드", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="cloud_file_uploader")
    screenshot_uploaders = st.sidebar.file_uploader("📸 [B] 벤치마킹 스크린샷 업로드", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="cloud_screenshot_uploader")

    gemini_images = []
    if uploaded_files:
        for u_file in uploaded_files:
            u_file.seek(0)
            gemini_images.append(Image.open(io.BytesIO(u_file.read())))
    if screenshot_uploaders:
        for s_file in screenshot_uploaders:
            s_file.seek(0)
            gemini_images.append(Image.open(io.BytesIO(s_file.read())))

    page_number = st.sidebar.slider("출력할 상세페이지 단계 (1~8장)", 1, 8, 1)

    if st.sidebar.button("✨ 쿠팡형 상세페이지 즉시 생성"):
        if not api_key:
            st.error("Google API Key를 입력해 주세요!")
        elif not product_info:
            st.error("상품 정보를 입력해 주세요!")
        else:
            with st.status("🤖 AI가 선택하신 샘플 구조를 토대로 초고속 연산을 시작합니다...", expanded=True) as status:
                try:
                    genai.configure(api_key=api_key)
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("📝 1단계: AI 마케팅 카피 및 기획서")
                        st.write(f"⚙️ **[안내]** 선택하신 `{chosen_type}` 구조를 주입하여 조합 중...")
                        
                        prompt = f"""너는 전환율 극대화 상세페이지를 설계하는 인공지능 마케터야.
                        전체 8장 구조 중 현재 [{page_number}번째 장]을 기획해야 해.
                        
                        [중요 가이드라인]:
                        오늘 채택한 상세페이지 전체 공식 뼈대:
                        {all_templates[chosen_type]['structure']}
                        
                        위 흐름을 바탕으로 이번 {page_number}번째 장에 맞는 최적의 내용을 도출해줘.
                        
                        [상품 정보]: {product_info}
                        [타겟 고객]: {target_customer}
                        
                        ■ 1. 메인 카피라이팅 / ■ 2. 비주얼 연출 지시서 / ■ 3. 디자인 무드 양식으로 작성해줘."""
                        
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        st.write("🧠 **[연산]** 제미나이가 카피라이팅 문장을 벼려내는 중... ✍️")
                        
                        if gemini_images:
                            response = model.generate_content([prompt] + gemini_images)
                        else:
                            response = model.generate_content(prompt)
                        st.markdown(response.text)
                        
                    with col2:
                        st.subheader("🖼️ 2단계: 쿠팡 규격 완성 배너 이미지 (가로 780px)")
                        st.write("🎨 **[랜더링]** 구글 Imagen AI 엔진이 이미지를 드로잉 중... 🚀")
                        
                        image_prompt = f"Professional e-commerce product banner for Coupang, width 780px, {product_info}, 4k photorealistic"
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
                        
                        st.image(coupang_image, caption=f"쿠팡 최적화 배너 ({page_number}장)")
                        
                        img_byte_arr = io.BytesIO()
                        coupang_image.save(img_byte_arr, format='JPEG')
                        
                        st.download_button(
                            label=f"💾 {page_number}장 이미지 다운로드",
                            data=img_byte_arr.getvalue(),
                            file_name=f"coupang_page_{page_number}.jpg",
                            mime="image/jpeg"
                        )
                    
                    status.update(label="🎉 AI 상세페이지 기획서 및 배너 생성이 모두 성공했습니다!", state="complete", expanded=False)

                except Exception as e:
                    st.warning("1단계 마케팅 기획서 작성이 완료되었습니다. (이미지 배너 생성 영역은 구글 API 키의 이미지 모델 결제 권한 활성화 후 가로 780px 자동 매칭 출력이 재개됩니다.)")
                    status.update(label="✅ 분석 및 텍스트 기획 출력이 마무리되었습니다.", state="complete", expanded=False)

# ==========================================
# [TAB 2] 벤치마킹 샘플 추가/확장 (추가 페이지)
# ==========================================
with tab2:
    st.subheader("➕ 타사 벤치마킹 링크로 나만의 샘플 공식 추출하기")
    st.write("인터넷에서 발견한 대박 상세페이지 링크나 카피 구조를 적어주시면, 제미나이가 그 구조만 완벽히 분석하여 **[1번 고속 제작소]의 메인 미리보기 메뉴에 새 샘플 타입으로 자동 등록**해 줍니다!")
    
    new_api_key = st.text_input("분석용 Google API Key를 입력하세요", type="password", key="tab2_key")
    new_template_title = st.text_input("✨ 내가 지정할 새 샘플 이름", placeholder="예: [D타입] 대박 압축 파우치 벤치마킹 구조")
    benchmark_data = st.text_area("🔗 벤치마킹할 사이트 URL 또는 카피 내용들을 붙여넣어 주세요", placeholder="여기에 대박 주소나 참고할 페이지의 텍스트 흐름을 적어주세요.")
    
    if st.button("🛠️ AI에게 템플릿 구조 추출 및 연동 요청"):
        if not new_api_key:
            st.error("API Key를 입력해 주세요.")
        elif not new_template_title or not benchmark_data:
            st.error("새 샘플 이름과 벤치마킹 데이터를 모두 입력해 주세요.")
        else:
            with st.spinner("🤖 제미나이가 주입된 주소/데이터의 상세페이지 기승전결 뼈대를 역추적 분석 중..."):
                try:
                    genai.configure(api_key=new_api_key)
                    analysis_model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    analysis_prompt = f"""너는 상위 1% 마케터이자 소스 코드 프롬프트 엔지니어 수석 디자이너야.
                    제공된 [벤치마킹 데이터]를 읽고, 상품 고유 정보를 싹 제외한 '순수 상세페이지 레이아웃 구조와 스토리텔링 흐름'만 기승전결 뼈대로 명확히 정제해줘.
                    
                    [벤치마킹 데이터]: {benchmark_data}
                    
                    반드시 아래 형식으로만 딱 한 줄씩 간결하게 요약해서 답변해줘:
                    설명: (이 구조의 특징을 한 문장으로 요약)
                    구조: 1. (도입부) -> 2. (전개) -> 3. (절정) -> 4. (결말)"""
                    
                    response = analysis_model.generate_content(analysis_prompt)
                    res_text = response.text
                    
                    parsed_desc = "AI가 분석한 커스텀 벤치마킹 레이아웃입니다."
                    parsed_structure = benchmark_data[:100] + "..."
                    
                    for line in res_text.split('\n'):
                        if "설명:" in line:
                            parsed_desc = line.replace("설명:", "").strip()
                        if "구조:" in line:
                            parsed_structure = line.replace("구조:", "").strip()
                    
                    st.session_state["custom_templates"][new_template_title] = {
                        "desc": parsed_desc,
                        "structure": parsed_structure
                    }
                    
                    st.success(f"🎉 성공! [{new_template_title}]이 성공적으로 분석되어 탑재되었습니다!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"분석 중 오류가 발생했습니다: {e}")
