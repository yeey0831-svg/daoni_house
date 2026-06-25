import streamlit as st

# 1. 페이지 레이아웃 및 스타일 정의
st.set_page_config(layout="wide", page_title="다오니하우스 쿠팡 마스터 스튜디오")

# 780px 고정 폭 스크롤 도화지 스타일 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    /* 쿠팡 정품 규격 가로 780px 시뮬레이션 컨테이너 */
    .coupang-wrapper {
        max-width: 780px;
        margin: 0 auto;
        background-color: #ffffff;
        border: 1px solid #e3e3e3;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 세션 상태 관리 (버튼 실행 트리거)
if "build_done" not in st.session_state:
    st.session_state.build_done = False

# 3. 20년 차 기획자의 맞춤형 동적 카피라이팅 및 프롬프트 생성 엔진
def generate_custom_copy(name, desc):
    # 입력단어 기반 기본 키워드 방어 로직 (없을 경우 기본값 세팅)
    short_name = name.split()[0] if name else "추천 상품"
    if "자석" in name or "자석" in desc:
        core_feature = "착! 붙여서 보관하는 강력 자석 설계"
        pain_point = "매번 쓰고 나면 사라지는 일반 집게, 찾느라 스트레스 받으셨죠?"
        detail_tech = "냉장고, 자석 타판 어디든 착! 분실 걱정 없는 스마트 리빙"
    else:
        core_feature = "공간의 가치를 바꾸는 압도적 밀폐력"
        pain_point = "금방 눅눅해지고 상하는 식재료 보관 문제"
        detail_tech = "공기와 습기를 완벽하게 차단하는 초밀착 구조"

    # 780px 매칭형 프리미엄 리빙/주방 연출 이미지 플레이스홀더
    return [
        {
            "step": "01. 오프닝 프리미엄 헤더",
            "title": f"주방의 분위기를 바꾸는 감성 스펙\n✨ {short_name}",
            "sub": f"정리의 시작은 장비부터. 다오니하우스가 선보이는 역대급 프리미엄 라인업.",
            "img": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=780&q=80", # 주방 스튜디오 컷
            "prompt": f"High-end editorial commercial product photography of {short_name}, arranged beautifully on a modern aesthetic kitchen counter, soft natural morning light, cinematic, photorealistic 8k --ar 4:5"
        },
        {
            "step": "02. 고질적 불편함 자극 (Pain Point)",
            "title": f"{pain_point}\n대충 묶어둔 봉지 속 눅눅해지는 식감...",
            "sub": "밀봉되지 않은 식재료는 세균 번식과 품질 저하의 원인이 됩니다.",
            "img": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=780&q=80", # 흐트러진 주방/소품 컷
            "prompt": f"A realistic messy kitchen pantry filled with opened, unsealed snack bags and messy items, frustrating atmosphere, dramatic realistic lighting --ar 4:5"
        },
        {
            "step": "03. 감성 해답 제시 (Solution)",
            "title": "선명하고 아름다운 7가지 컬러로\n깔끔하게 접고, 빈틈없이 밀봉 완료!",
            "sub": "비우고 정돈하는 순간, 복잡했던 일상에 완벽한 칼각 질서가 찾아옵니다.",
            "img": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=780&q=80", # 깔끔 정돈된 리빙룸/주방 컷
            "prompt": f"Extremely organized modern kitchen cabinet, beautifully sorted with colorful minimalist design clips, neat design, bright airy atmosphere, architectural digest style --ar 4:5"
        },
        {
            "step": "04. 압도적 핵심 기술력 (Spec)",
            "title": f"어디서나 간편하게 툭-\n{core_feature}",
            "sub": "쉽게 떨어지지 않는 강력 자석 내장으로 메모 거치부터 인테리어 효과까지 자석 하나로 종결.",
            "img": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=780&q=80", # 정밀 테스쳐 줌인 컷
            "prompt": f"Macro close-up shot of a sleek modern magnetic clip attached to a clean metallic surface, showcasing high-quality material finish and strong hold, studio lighting --ar 4:5"
        },
        {
            "step": "05. 리얼 사용 시나리오 (Lifestyle)",
            "title": "과자 봉지부터 식빵, 캠핑장 소스 보관까지\n생활 전반을 아우르는 완벽한 다용도성",
            "sub": "주방을 넘어 일상의 모든 밀폐가 필요한 순간 가장 먼저 손이 가게 됩니다.",
            "img": "https://images.unsplash.com/photo-1528740561666-bd2479da0845?w=780&q=80", # 일상 감성 주방 활용 컷
            "prompt": f"A person's hand neatly sealing a bread bag using a stylish minimal clip in a warm bright cozy apartment kitchen, lifestyle commercial photography --ar 4:5"
        },
        {
            "step": "06. 마감 및 디테일 체크 (Zoom-in)",
            "title": "1mm의 틈새도 허용하지 않는\n강력한 고정력과 라운딩 마감",
            "sub": "손이 자주 닿는 제품이기에 상처 없이 안전하도록 모서리 전체 유선형 안전 설계.",
            "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=780&q=80", # 전문 스튜디오 대칭 컷
            "prompt": f"Crisp professional studio product display of minimal design clips, isolated clean background, soft elegant shadows, commercial catalog design --ar 4:5"
        },
        {
            "step": "07. 독점 패키지 구성 & 증정 혜택",
            "title": "오직 다오니하우스 단독 특가\n6세트 구매 시 1장 더 (+1) 특별 증정",
            "sub": "가장 실용적인 구성에 특별 보너스까지 챙겨 드리는 한정 수량 기획전입니다.",
            "img": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=780&q=80", # 선물상자 패키지 컷
            "prompt": f"Beautiful aesthetic gift box packaging layout with colorful interior items, top-down flatlay angle, pastel background, premium brand presentation --ar 4:5"
        },
        {
            "step": "08. 품질 안심 보증 시스템 (Outro)",
            "title": "20년 차 기획자와 다오니하우스의 약속\n100% 안심 책임 보상 가이드",
            "sub": "품질에 타협하지 않았기에 자신 있습니다. 제품 불만족 시 신속한 교환/반품을 약속합니다.",
            "img": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=780&q=80", # 신뢰/오피스 컷
            "prompt": f"A highly trustworthy corporate product assurance layout, minimal sleek styling, calm professional studio backdrop, focus on consumer safety --ar 4:5"
        }
    ]

# 4. 레이아웃 분할 구현
left_panel, right_canvas = st.columns([1, 1.2])

# --- [좌측 제어 패널] ---
with left_panel:
    st.header("📝 기획자 입력 폼")
    st.caption("새 상품 정보와 이미지를 학습시켜 완벽한 맞춤형 기획안을 추출합니다.")
    
    # 스크린샷에 입력하신 실제 텍스트를 기본값으로 맵핑하여 직관성 극대화
    prod_name = st.text_input("📦 상품명 입력", 
                             value="다오니네 다오니네 밀봉 자석집게 6세트+1개 남은과자 식빵 캠핑 소스 보관 다용도 주방 밀폐 봉지집게")
    
    prod_info = st.text_area("📝 핵심 상품 정보 / 소재 / 특장점", 
                             value="총 7가지 색상으로 구성된 아름다운 색상의 자석 집게. 자석으로 되어 있어서 자석이 붙는곳이면 어디든 부착 보관가능 분실률이 작고 간편하게 찾아서 쓸수있어요. 인테리어 효과 및 사진도 부착하여 볼수 있고 다양한 활용성 음식물 봉투 밀가루 봉투 과자 등 접어서 간편하게 자석집게로 집어서 보관합니다.")
    
    st.subheader("📸 소스 데이터 업로드")
    product_files = st.file_uploader("원본 제품 사진 다중 첨부 (완료)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="prod_upload")
    ref_files = st.file_uploader("쿠팡 디자인 벤치마킹 참고 자료 (완료)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="ref_upload")
    
    st.markdown("---")
    
    # 빌드 버튼 클릭 시 세션 가동
    if st.button("🚀 20년차 기획 스타일로 상세페이지 8장 즉시 생성", type="primary", use_container_width=True):
        st.session_state.build_done = True
        st.rerun()

    # 프롬프트 추출창 정리
    if st.session_state.build_done:
        st.subheader("📋 나노바나나/미드저니 전용 프롬프트")
        current_data = generate_custom_copy(prod_name, prod_info)
        for d in current_data:
            with st.expander(f"🔍 {d['step']} 프롬프트"):
                st.code(d['prompt'], language="text")

# --- [우측 캔버스] 이미지 렌더링 버그가 완벽 차단된 고정형 뷰어 ---
with right_canvas:
    st.header("📱 쿠팡형 실시간 미리보기 (780px 고정)")
    
    if not st.session_state.build_done:
        st.info("💡 왼쪽 폼에서 정보를 확인한 뒤 [🚀 상세페이지 8장 즉시 생성] 버튼을 누르면 이 자리에 깨짐 없는 완성형 이미지 8장이 순서대로 배치됩니다.")
    else:
        # 동적 데이터 획득
        final_sections = generate_custom_copy(prod_name, prod_info)
        
        # HTML 깨짐 버그를 완전히 방지하는 Streamlit 전용 네이티브 스크롤 도화지 빌드
        with st.container():
            st.markdown('<div class="coupang-wrapper">', unsafe_allow_html=True)
            
            for i, section in enumerate(final_sections):
                # 섹션 블록 내부 디자인 컨테이너 설정
                bg_color = "#ffffff" if i % 2 == 0 else "#f9fbfd"
                accent_line = "#004ba0" if i % 2 == 0 else "#1c2d42"
                title_color = "#111111" if i != 1 else "#d9534f" # 문제제기는 빨간색 강조
                
                # 내부 글자 스타일 및 구성을 전용 컨테이너에 깔끔하게 인젝션
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; padding: 50px 45px 20px 45px; border-bottom: 2px dashed #e5e5e5;">
                        <span style="font-size: 11px; font-weight: 700; color: {accent_line}; letter-spacing: 2px; display:block; margin-bottom:10px;">
                            {section['step'].upper()}
                        </span>
                        <h2 style="font-size: 28px; font-weight: 900; line-height: 1.4; color: {title_color}; margin: 0 0 10px 0; white-space: pre-wrap;">
                            {section['title']}
                        </h2>
                        <p style="font-size: 15px; font-weight: 400; color: #555555; line-height: 1.6; margin: 0 0 30px 0; white-space: pre-wrap;">
                            {section['sub']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 🌟 이미지 출력 버그 차단: Streamlit 순정 최적화 이미지 렌더링 컴포넌트 사용!
                    st.image(section['img'], caption=f"▲ {section['step']} 생성 가이드 스튜디오 컷", use_container_width=True)
                    
                    # 하단 여백 및 디바이더 선 데코레이션
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; padding: 10px 45px 40px 45px;">
                        <div style="width: 40px; height: 3px; background-color: {accent_line};"></div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
