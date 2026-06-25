import streamlit as st

# 1. 페이지 레이아웃 및 쿠팡 전용 CSS 설정
st.set_page_config(layout="wide", page_title="다오니하우스 쿠팡 마스터 스튜디오")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 쿠팡 최적화 가로 780px 고정 도화지 */
    .coupang-canvas {
        width: 780px !important;
        max-width: 780px !important;
        margin: 0 auto;
        background-color: #ffffff;
        box-shadow: 0px 4px 30px rgba(0,0,0,0.15);
        border: 1px solid #e1e1e1;
        padding: 0px;
    }
    
    /* 상세페이지 세로형 스크롤 섹션 */
    .section-block {
        width: 780px;
        padding: 60px 45px;
        box-sizing: border-box;
        border-bottom: 2px solid #f0f0f0;
        background-color: #ffffff;
    }
    
    /* 이미지 스타일 자동 최적화 */
    .detail-img {
        width: 100%;
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin-top: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 실행 상태 관리를 위한 세션 초기화
if "generate_active" not in st.session_state:
    st.session_state.generate_active = False

# 3. 20년 차 기획자의 8단계 상세페이지 컨셉 및 프롬프트 정의 함수
def get_detail_page_data(prod_name, prod_info):
    # 각 단계별 기획에 맞는 고화질 스튜디오급 프리미엄 이미지 매칭
    return [
        {
            "step": "01. 오프닝 메인 헤더",
            "title": f"기존의 한계를 뛰어넘다\n🔥 프리미엄 {prod_name}",
            "sub": "다오니하우스가 제안하는 완벽한 라이프스타일 시그니처.",
            "img_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=780&q=80",
            "prompt": f"Premium high-end commercial product photography of {prod_name}, luxury modern studio lighting, sharp focus, 8k resolution."
        },
        {
            "step": "02. 문제 제기 (Pain Point)",
            "title": "아직도 무겁고 파손되는\n저가형 제품에 스트레스 받으시나요?",
            "sub": "뒤틀리고 깨지는 일상 속 불편함, 이제 끝내야 합니다.",
            "img_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=780&q=80",
            "prompt": f"A messy and broken traditional product scene, realistic frustrated atmosphere, dramatic shadows."
        },
        {
            "step": "03. 혁신적 대안 제시 (Solution)",
            "title": "공간을 바꾸는 단 하나의 선택\n마침내 완전히 새로워진 구조",
            "sub": "비우는 순간 채워지는 놀라운 정돈의 마법을 느껴보세요.",
            "img_url": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=780&q=80",
            "prompt": f"A beautifully organized, bright minimalist space featuring {prod_name}, soft morning sunlight, architectural aesthetic."
        },
        {
            "step": "04. 압도적인 기술력 (Spec)",
            "title": "타협 없는 품질의 기준\n독보적인 초정밀 마감 공정",
            "sub": f"{prod_info if prod_info else '최상급 내구성 소재'} 채택으로 변형 없이 평생 견고하게.",
            "img_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=780&q=80",
            "prompt": f"Macro extreme close-up shot of {prod_name}, highlighting raw luxury textures, commercial product detail showcase."
        },
        {
            "step": "05. 리얼 라이프 스타일 (Lifestyle)",
            "title": "어디에 두어도 예술이 되는\n모던 감성 인테리어 완성",
            "sub": "거실, 주방, 서재 어떤 공간이든 가치를 더해주는 오브제 디자인.",
            "img_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=780&q=80",
            "prompt": f"{prod_name} naturally integrated into a high-end luxury modern apartment room, cozy atmospheric interior photography."
        },
        {
            "step": "06. 디테일 팩트 체크 (Zoom-in)",
            "title": "1mm의 오차도 허용하지 않는\n완벽한 디테일을 확인하세요",
            "sub": "작은 고리 하나, 숨은 마감까지 사용자를 배려하여 설계했습니다.",
            "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=780&q=80",
            "prompt": f"Symmetrical crisp product shot of {prod_name}, clean isolated background, professional studio catalog style."
        },
        {
            "step": "07. 독점 패키지 및 증정 혜택",
            "title": "오직 다오니하우스에서만\n구매 고객 전원 특별 기프트 증정",
            "sub": "지금 구매하시면 한정판 전용 케이스와 패키지를 함께 전해드립니다.",
            "img_url": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=780&q=80",
            "prompt": f"Top-down flatlay photography of {prod_name} box packaging with luxury premium gift wrap, pastel clean background."
        },
        {
            "step": "08. 품질 안심 보증 (Outro)",
            "title": "품질에 대한 절대적 자신감\n100% 평생 책임 보증제",
            "sub": "고객 만족을 최우선으로 생각하는 다오니하우스가 끝까지 책임집니다.",
            "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=780&q=80",
            "prompt": f"Authoritative clean product portrait next to a soft elegant background, inspiring corporate trust and absolute quality."
        }
    ]

# 4. 화면 분할 (좌측: 데이터 입력창 / 우측: 쿠팡 고정 스크롤 도화지)
left_panel, right_canvas = st.columns([1, 1.2])

# --- [좌측 제어 패널] 이미지 넣고 상품설명 넣는 공간 ---
with left_panel:
    st.header("🎯 기획자 입력 폼")
    st.write("아래 정보를 채운 뒤 '생성하기' 버튼을 누르면 우측에 상세페이지 8장이 즉시 완성됩니다.")
    
    prod_name = st.text_input("📦 상품명 입력", value="오가닉 뱀부 멀티 정리함")
    prod_info = st.text_area("📝 핵심 상품 정보 / 소재 / 특장점", 
                             value="100% 천연 대나무 원목 사용, 친환경 방수 코팅, 공간 맞춤형 슬라이딩 조절 구조",
                             placeholder="예: 친환경 아크릴, 특허받은 밀폐 구조 등")
    
    st.subheader("📸 소스 이미지 업로드")
    uploaded_products = st.file_uploader("제품 원본 사진 첨부 (여러 장 가능)", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    uploaded_refs = st.file_uploader("디자인 벤치마킹 참고 자료 첨부", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    st.markdown("---")
    
    # 🌟 드디어 추가된 메인 실행 버튼!
    if st.button("🚀 20년차 기획 스타일로 상세페이지 8장 즉시 생성", type="primary", use_container_width=True):
        if prod_name and prod_info:
            st.session_state.generate_active = True
            st.balloons() # 성공 축하 효과
        else:
            st.error("상품명과 상품 정보를 입력해야 상세페이지 생성이 가능합니다!")

    # 실시간 프롬프트 백업 데이터 노출
    if st.session_state.generate_active:
        st.subheader("📋 나노바나나/미드저니용 프롬프트 리스트")
        data_list = get_detail_page_data(prod_name, prod_info)
        for d in data_list:
            with st.expander(f"🔍 {d['step']} 이미지 프롬프트 복사"):
                st.code(d['prompt'], language="text")

# --- [우측 캔버스] 모든 작업이 완료된 완성본 상세페이지 8장 즉시 출력 ---
with right_canvas:
    st.subheader("📱 쿠팡 규격(780px) 고정형 완성 상세페이지")
    
    # 버튼을 누르기 전 초기 상태 화면
    if not st.session_state.generate_active:
        st.info("💡 왼쪽 패널에서 상품 정보를 입력하고 [🚀 상세페이지 8장 즉시 생성] 버튼을 클릭하시면 이곳에 완성된 빌드 결과물이 나타납니다.")
    
    # 버튼 클릭 시 8장의 고화질 완성형 페이지 연속 출력
    else:
        # 데이터 빌드
        sections_data = get_detail_page_data(prod_name, prod_info)
        
        # 780px 도화지 HTML 시작
        html_buffer = '<div class="coupang-canvas">'
        
        for i, section in enumerate(sections_data):
            # 시각적 리듬감을 주기 위해 홀수/짝수 섹션 배경색 교차 적용
            bg_color = "#ffffff" if i % 2 == 0 else "#f9fbfd"
            title_color = "#111111" if i != 1 else "#d9534f" # 문제제기는 경고 레드톤 적용
            accent_bar = "#0056b3" if i % 2 == 0 else "#1c2d42"
            
            html_buffer += f"""
            <div class="section-block" style="background-color: {bg_color};">
                <span style="font-size: 11px; font-weight: 700; color: {accent_bar}; letter-spacing: 2px; display: block; margin-bottom: 15px;">
                    {section['step'].upper()}
                </span>
                
                <h2 style="font-size: 32px; font-weight: 900; line-height: 1.35; color: {title_color}; white-space: pre-wrap; margin-bottom: 12px; letter-spacing: -0.5px;">
                    {section['title']}
                </h2>
                <p style="font-size: 16px; font-weight: 400; color: #555555; line-height: 1.6; white-space: pre-wrap; margin-bottom: 25px;">
                    {section['sub']}
                </p>
                
                <img src="{section['img_url']}" class="detail-img" alt="{section['step']}" />
                
                <div style="margin-top: 40px; width: 40px; height: 3px; background-color: {accent_bar};"></div>
            </div>
            """
            
        html_buffer += '</div>'
        
        # 화면에 빌드된 쿠팡 상세페이지 전장 렌더링
        st.markdown(html_buffer, unsafe_allow_html=True)
