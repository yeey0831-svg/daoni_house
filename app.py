import streamlit as st

# 1. 페이지 레이아웃 및 780px 세로형 상세페이지 전용 CSS 설정
st.set_page_config(layout="wide", page_title="다온이네 하우스 마스터 스튜디오")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #f8f9fa;
    }
    
    /* 🔴 PPT처럼 늘어나는 버그 해결: 쿠팡 공식 규격 780px 고정 스크롤 도화지 */
    .detail-container {
        width: 780px !important;
        max-width: 780px !important;
        margin: 0 auto !important;
        background-color: #ffffff;
        border: 1px solid #e1e4e6;
        box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.08);
        padding: 0px !important;
    }
    
    /* 섹션 간 경계 및 간격 제어 */
    .page-section {
        width: 100%;
        box-sizing: border-box;
        padding: 60px 50px;
        background-color: #ffffff;
        border-bottom: 8px solid #f1f3f5;
    }
    
    /* 레퍼런스 스타일의 딥블루 하이라이트 배너 */
    .blue-banner {
        background-color: #102a43;
        color: #ffffff;
        padding: 40px;
        text-align: center;
        border-radius: 4px;
        margin-bottom: 30px;
    }
    
    /* 포인트 번호 스타일 */
    .point-badge {
        background-color: #004494;
        color: white;
        padding: 4px 12px;
        font-size: 14px;
        font-weight: 700;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 실행 상태 관리를 위한 세션 초기화
if "build_complete" not in st.session_state:
    st.session_state.build_complete = False

# 3. 20년 차 기획자의 자석밀봉집게 맞춤형 8단계 상세페이지 기획안 정의
def get_magnetic_clip_spec(name, info):
    return [
        {
            "step": "01. 오프닝 메인 비주얼",
            "badge": "LAUNCHING",
            "title": "주방의 모든 밀봉을 스타일리시하게\n🌈 다온이네 하우스 멀티 자석집게",
            "sub": "남은 과자부터 식빵, 캠핑 소스까지 빈틈없이 꽉! 붙여서 보관하는 스마트 리빙 공식을 만나보세요.",
            "img_url": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=780&q=80", # 주방 소품/집게 무드
            "prompt": "Premium commercial studio setup of 7 different pastel colored magnetic sealing clips, neatly holding organized food snack pouches on a clean modern kitchen counter, crisp details, 8k, architectural lighting --ar 4:5"
        },
        {
            "step": "02. 고질적 불편함 자극 (Pain Point)",
            "badge": "CHECK POINT",
            "title": "매번 쓰고 나면 사라지는 집게,\n대충 묶어 눅눅해진 식감에 스트레스 받으셨죠?",
            "sub": "어디 뒀는지 기억 안 나는 소품들과 밀봉되지 않아 버려지는 식재료, 이제 완벽하게 차단할 때입니다.",
            "img_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=780&q=80", # 어질러진 주방
            "prompt": "A realistic chaotic kitchen pantry with open stale snack bags, messy unorganized drawers, frustrated household atmosphere, professional photography --ar 4:5"
        },
        {
            "step": "03. 감성적 솔루션 제안 (Solution)",
            "badge": "SOLUTION",
            "title": "공간을 바꾸는 단 하나의 선택\n접고, 집고, 붙이면 주방 정리 끝!",
            "sub": "다온이네 하우스가 제안하는 7가지 감성 컬러 웨이로 복잡했던 주방에 완벽한 칼각 질서가 시작됩니다.",
            "img_url": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=780&q=80", # 깔끔 정돈된 수납
            "prompt": "Beautifully minimalist organized modern white kitchen, interior styling showing functional elegance, lifestyle layout, warm morning sun rays --ar 4:5"
        },
        {
            "step": "04. 압도적 핵심 가치 01 (자석 기능)",
            "badge": "POINT 01",
            "title": "잃어버릴 걱정 제로!\n붙여놓고 툭- 꺼내 쓰는 초강력 마그네틱",
            "sub": "후면에 내장된 네오디움 자석으로 냉장고, 조리대, 자석 보드판 어디든 착! 붙여 보관하고 간편하게 찾으세요.",
            "img_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=780&q=80", # 냉장고/철제 부착 무드
            "prompt": "Extreme macro close-up of a sleek minimal magnetic clip firmly attached to a clean white refrigerator door surface, holding a beautiful postcard, soft luxury shadow, professional commercial catalog --ar 4:5"
        },
        {
            "step": "05. 압도적 핵심 가치 02 (밀봉/활용성)",
            "badge": "POINT 02",
            "title": "공기 차단 100% 밀폐 스펙\n식빵부터 캠핑장 소스까지 올인원 케어",
            "sub": "강력한 스프링 장력과 내부 논슬립 패드가 흐르는 소스나 밀가루 봉지까지 단 1mm의 틈새도 없이 꽉 잡아줍니다.",
            "img_url": "https://images.unsplash.com/photo-1528740561666-bd2479da0845?w=780&q=80", # 실사용 라이프스타일
            "prompt": "A close up look of a person's hands sealing a fresh loaf of bread neatly with a stylish pastel-colored grip clip, warm atmospheric lighting, cinematic interior style --ar 4:5"
        },
        {
            "step": "06. 마감 퀄리티 체크 (Zoom-in)",
            "badge": "DETAIL CHECK",
            "title": "손끝이 안전한 라운딩 마감 공정\n오래도록 변함없는 견고한 내구성",
            "sub": "매일 수십 번 열고 닫는 제품이기에 상처를 주지 않는 안전한 곡선 설계와 유광 고급 ABS 소재를 채택했습니다.",
            "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=780&q=80", # 스튜디오 대칭 컷
            "prompt": "Frontal product shot of seven premium plastic sealing clips displayed symmetrically, smooth round corners, studio product lighting, highly detailed surface texture --ar 4:5"
        },
        {
            "step": "07. 독점 패키지 및 구매 혜택",
            "badge": "SPECIAL GIFT",
            "title": "오직 다온이네 하우스 고객 단독 특가\n6세트 구매 시 1개 더! (+1) 특별 증정",
            "sub": "가장 활용도가 높은 패키지 구성에 보너스 혜택까지 더했습니다. 한정 수량 소진 전 지금 선택하세요.",
            "img_url": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=780&q=80", # 선물상자/패키지
            "prompt": "Top-down flatlay shot of a modern clean box packaging labeled premium home kit, surrounding pastel colors, luxury brand presentation --ar 4:5"
        },
        {
            "step": "08. 신뢰 안심 보증 (Outro)",
            "badge": "WARRANTY",
            "title": "품질에 대한 절대적 자신감\n100% 안심 책임 보상 약속",
            "sub": "다온이네 하우스는 고객님의 만족을 최우선으로 생각합니다. 완벽한 불량 검수를 거쳐 안전하게 배송됩니다.",
            "img_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=780&q=80", # 신뢰 보증 무드
            "prompt": "Elegant corporate quality certificate background layout, blurred modern bright background, conveying ultimate consumer trust and high prestige --ar 4:5"
        }
    ]

# 4. 왼쪽 입력 / 오른쪽 고정 뷰어 컬럼 매칭
left_panel, right_canvas = st.columns([1, 1.1])

# --- [좌측 제어 패널] ---
with left_panel:
    st.header("🎯 다온이네 하우스 기획 스튜디오")
    st.caption("20년 차 상세페이지 전문가의 논리로 상품 맞춤형 빌드를 진행합니다.")
    
    prod_name = st.text_input("📦 상품명 입력", 
                             value="다온이네 하우스 밀봉 자석집게 6세트+1개 남은과자 식빵 캠핑 소스 보관 다용도 주방 밀폐 봉지집게")
    
    prod_info = st.text_area("📝 핵심 상품 정보 / 소재 / 특장점", 
                             value="총 7가지 색상으로 구성된 아름다운 색상의 자석 집게. 자석으로 되어 있어서 자석이 붙는곳이면 어디든 부착 보관가능 분실률이 작고 간편하게 찾아서 쓸수있어요. 인테리어 효과 및 사진도 부착하여 볼수 있고 다양한 활용성 음식물 봉투 밀가루 봉투 과자 등 접어서 간편하게 자석집게로 집어서 보관합니다.")
    
    st.subheader("📸 소스 데이터 확인")
    st.file_uploader("원본 제품 사진 첨부 완료 (4장)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="done_p", disabled=True)
    st.file_uploader("벤치마킹 디자인 레퍼런스 첨부 완료 (8장)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="done_r", disabled=True)
    
    st.markdown("---")
    
    # 생성 버튼 누르면 상태 변경
    if st.button("🚀 780px 정품 규격 상세페이지 8장 즉시 빌드", type="primary", use_container_width=True):
        st.session_state.build_complete = True
        st.rerun()

    # 나노바나나/미드저니 전용 프롬프트 리스트 추출
    if st.session_state.build_complete:
        st.subheader("📋 나노바나나 / 미드저니 입력용 프롬프트")
        sections = get_magnetic_clip_spec(prod_name, prod_info)
        for s in sections:
            with st.expander(f"🔍 {s['step']} 최적화 프롬프트 복사하기"):
                st.code(s['prompt'], language="text")

# --- [우측 캔버스] 가로로 안 늘어나는 진짜 780px 상세페이지 시뮬레이터 ---
with right_canvas:
    st.subheader("📱 쿠팡 전용 세로형 스크롤 미리보기")
    
    if not st.session_state.build_complete:
        st.info("💡 왼쪽의 [🚀 780px 정품 규격 상세페이지 8장 즉시 빌드] 버튼을 클릭하시면 레퍼런스 무드의 일체형 상세페이지가 생성됩니다.")
    else:
        # 데이터 로드
        final_sections = get_magnetic_clip_spec(prod_name, prod_info)
        
        # 🔴 가로 늘어남을 방지하는 외부 컨테이너 시작
        st.markdown('<div class="detail-container">', unsafe_allow_html=True)
        
        for i, section in enumerate(final_sections):
            
            # 레퍼런스 이미지 스타일을 차용한 타이틀 마크다운 출력
            if i == 0:
                # 메인 오프닝 전용 블루 배너 스타일
                st.markdown(f"""
                <div class="blue-banner">
                    <span style="font-size:12px; font-weight:800; letter-spacing:3px; color:#9fb3c8;">{section['badge']}</span>
                    <h1 style="font-size:30px; font-weight:900; line-height:1.4; color:#ffffff; margin-top:10px; margin-bottom:5px;">{section['title']}</h1>
                    <p style="font-size:14px; color:#cbd5e1; font-weight:400; line-height:1.5;">{section['sub']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # 일반 포인트 및 스펙 섹션 텍스트 구성
                title_color = "#d9383a" if i == 1 else "#102a43" # 불편함 유도는 붉은색 포인트
                st.markdown(f"""
                <div style="padding: 45px 40px 10px 40px;">
                    <span class="point-badge">{section['badge']}</span>
                    <h2 style="font-size:24px; font-weight:800; line-height:1.4; color:{title_color}; margin-top:5px; margin-bottom:12px;">{section['title']}</h2>
                    <p style="font-size:15px; color:#486581; font-weight:400; line-height:1.6; margin-bottom:20px;">{section['sub']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 🌟 이미지 강제 780px 폭 홀딩 및 세로 매칭 출력
            # 가로로 과도하게 터지지 않도록 width=780 매개변수를 직접 명시합니다.
            st.image(section['img_url'], width=780)
            
            # 구분을 위한 하단 실선 데코레이션
            st.markdown('<div style="height:20px; background-color:#ffffff; border-bottom:1px solid #e1e4e6;"></div>', unsafe_allow_html=True)
            
        # 가로 늘어남 방지 외부 컨테이너 종료
        st.markdown('</div>', unsafe_allow_html=True)
