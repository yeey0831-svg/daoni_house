import streamlit as st

# 1. 페이지 레이아웃 및 환경 설정
st.set_page_config(layout="wide", page_title="다오니하우스 쿠팡 마스터 스튜디오")

# 쿠팡 전용 780px 고정 스타일 및 디자이너 폰트 인젝션
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    /* 메인 컨텐츠 영역 폰트 지정 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 780px 고정형 쿠팡 상세페이지 시뮬레이터 스타일 */
    .coupang-canvas {
        width: 780px !important;
        max-width: 780px !important;
        margin: 0 auto;
        background-color: #ffffff;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
        border: 1px solid #e1e1e1;
        padding: 0px;
    }
    
    /* 각 섹션별 세로 최소 800px~1000px 느낌을 주기 위한 가상 높이 설정 */
    .section-block {
        width: 780px;
        min-height: auto;
        padding: 80px 45px;
        box-sizing: border-box;
        border-bottom: 1px dashed #ddd;
        position: relative;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 20년 차 기획자의 8단계 동적 템플릿 엔진 데이터 구조
def generate_expert_framework(prod_name, prod_info):
    return [
        {
            "step": "01. 인트로 브랜드 헤더",
            "concept": "구매 전환을 결정짓는 3초 후킹 스튜디오 컷",
            "copy_title": f"비교할 수 없는 압도적 차이\n{prod_name}의 시작",
            "copy_sub": f"그동안 찾으셨던 완벽한 퀄리티, 다오니하우스가 증명합니다.",
            "prompt": f"Premium high-end commercial product photography of {prod_name}. Placed elegantly on a clean luxury modern marble table, cinematic dramatic studio lighting from the side, soft background focus, 8k resolution, photorealistic, sharp focus --ar 4:5"
        },
        {
            "step": "02. 고질적 불편함 자극 (Pain Point)",
            "concept": "소비자가 기존에 겪던 스트레스와 문제점 시각화",
            "copy_title": "아직도 번거롭고 불편한\n옛날 방식을 고집하시나요?",
            "copy_sub": f"매번 반복되는 귀찮음과 품질 저하, 이제는 바꾸셔야 할 때입니다.",
            "prompt": f"A realistic messy and cluttered scene showing the problem of traditional methods. Disorganized environment, dim and frustrating atmosphere, high-end editorial style showing user dissatisfaction --ar 4:5"
        },
        {
            "step": "03. 대안 제시 (Solution)",
            "concept": "다오니하우스가 제시하는 가장 완벽한 해답",
            "copy_title": f"단 하나로 일상이 바뀝니다\n오직 {prod_name}만 가능한 혁신",
            "copy_sub": "비우고, 채우고, 완성하는 완벽한 라이프스타일의 시작.",
            "prompt": f"A clean, bright, and highly organized modern space featuring {prod_name}. A sense of relief, minimalist aesthetics, refreshing natural sunlight pouring through a window, professional interior photography --ar 4:5"
        },
        {
            "step": "04. 핵심 기술력 및 소재 강조",
            "concept": "20년 차 기획자가 뽑은 가장 강력한 디테일 스펙",
            "copy_title": f"보이지 않는 곳까지 완벽하게\n독보적인 프리미엄 스펙",
            "copy_sub": f"{prod_info if prod_info else '최상급 엄선된 소재'}로 내구성과 안전성을 모두 잡았습니다.",
            "prompt": f"Macro extreme close-up shot of {prod_name}, showcasing ultra-premium material textures and high-tech craftsmanship. Studio clean background, scientific and precise lighting, highlighting absolute durability, 8k --ar 4:5"
        },
        {
            "step": "05. 리얼 사용 씬 (Practical Use)",
            "concept": "소비자가 대입할 수 있는 실제 일상 속 감성 컷",
            "copy_title": "어떤 공간이든 자연스럽게\n감성을 더하는 디자인",
            "copy_sub": "실제 배치하는 순간 공간의 가치가 달라지는 것을 경험하세요.",
            "prompt": f"A lifestyle product photography of {prod_name} being naturally used in a luxury Korean apartment interior. Warm, inviting, and cozy atmosphere, captured with a professional 50mm lens, architectural digest style --ar 4:5"
        },
        {
            "step": "06. 디테일 및 특장점 팩트 체크",
            "concept": "기능적 장점을 꼼꼼하게 짚어주는 클로즈업 레이아웃",
            "copy_title": "타협하지 않는 디테일\n품질로 압도합니다",
            "copy_sub": "작은 마감 하나까지 수많은 테스트를 거쳐 완성되었습니다.",
            "prompt": f"Multi-angle studio product presentation of {prod_name}. Clean white background, perfect symmetry, soft shadows, balanced soft commercial lighting, showing precise design details --ar 4:5"
        },
        {
            "step": "07. 독점 패키지 및 혜택 (Value Stack)",
            "concept": "사은품 및 구성품을 보여주어 지금 사야 하는 이유 제공",
            "copy_title": "다오니하우스 단독 혜택\n풍성한 특별 패키지 구성",
            "copy_sub": "지금 구매하시는 모든 고객님께 특별 전용 사은품을 함께 보냅니다.",
            "prompt": f"A top-down flat lay photography of {prod_name} beautifully packaged with its premium gift box and accessories. Elegant arrangement, clean soft pastel background, professional commercial catalog style --ar 4:5"
        },
        {
            "step": "08. 품질 보증 및 신뢰 (Outro CTA)",
            "concept": "마지막 의심을 없애주는 평생 안심 보증 및 종결",
            "copy_title": "품질에 자신 있기에\n100% 안심 보증 시스템",
            "copy_sub": "다오니하우스는 철저한 사후 관리와 신속한 A/S를 약속드립니다.",
            "prompt": f"An authoritative and trust-inspiring product portrait of {prod_name} next to a subtle elegant gold warranty emblem icon. Dark sophisticated studio background, premium lighting, corporate trust and confidence --ar 4:5"
        }
    ]

# 3. 세션 상태 관리 초기화
if "prod_name" not in st.session_state:
    st.session_state.prod_name = "리빙 프리미엄 펜트리 정리함"
if "prod_info" not in st.session_state:
    st.session_state.prod_info = "친환경 고강도 투명 아크릴 소재, 적층 가능한 모듈러 설계"

# 4. 레이아웃 설계 (좌측 제어 패널 / 우측 고정형 캔버스)
left_panel, right_canvas = st.columns([1, 1.3])

# --- [좌측 제어 패널] 기획자의 입력 창 ---
with left_panel:
    st.header("🎯 20년 차 기획자 AI 엔진")
    st.write("상품 정보를 입력하면 판매용 카피라이팅과 이미지 프롬프트 8장이 자동으로 빌드됩니다.")
    
    # 데이터 입력
    input_name = st.text_input("📦 상품명 입력", value=st.session_state.prod_name)
    input_info = st.text_area("📝 핵심 상품 정보 / 소재 / 특징", value=st.session_state.prod_info, placeholder="예: 무독성 실리콘, 특허받은 밀폐 기술 등")
    
    st.session_state.prod_name = input_name
    st.session_state.prod_info = input_info
    
    st.subheader("📸 소스 이미지 데이터 제공")
    product_files = st.file_uploader("원본 제품 사진 다중 첨부 (AI 학습용)", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    ref_files = st.file_uploader("쿠팡 벤치마킹 디자인 참고 자료 첨부", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    st.divider()
    st.subheader("🛠️ 단계별 개별 문구 실시간 편집기")
    
    # 프레임워크 실시간 생성
    current_framework = generate_expert_framework(st.session_state.prod_name, st.session_state.prod_info)
    
    # 사이드바 형태로 복잡하지 않게 아코디언 배치
    for i, s in enumerate(current_framework):
        with st.expander(f"✏️ {s['step']} 문구 수정"):
            s['copy_title'] = st.text_area(f"[{i+1}] 메인 타이틀", value=s['copy_title'], key=f"title_{i}")
            s['copy_sub'] = st.text_area(f"[{i+1}] 서브 카피", value=s['copy_sub'], key=f"sub_{i}")
            st.info("💡 나노바나나 복사용 이미지 프롬프트:")
            st.code(s['prompt'], language="text")

# --- [우측 캔버스] 쿠팡 가로 780px 고정형 리얼 시뮬레이터 ---
with right_canvas:
    st.subheader("📱 쿠팡 규격(780px) 고정 실시간 프리뷰")
    st.caption("아래 영역은 실제 쿠팡 가로사이즈 780px과 동일하게 강제 고정된 화면입니다.")
    
    # 쿠팡 스크롤 도화지 시작
    html_buffer = '<div class="coupang-canvas">'
    
    for i, data in enumerate(current_framework):
        # 디자인 템플릿 색상 분기 (시각적 리듬감을 위해 섹션별 배경색 변화)
        bg_color = "#ffffff" if i % 2 == 0 else "#f8f9fa"
        title_color = "#111111" if i != 1 else "#c0392b" # 문제제기는 붉은 톤 강조
        accent_bar = "#0073e6" if i % 2 == 0 else "#1a2a4e"
        
        html_buffer += f"""
        <div class="section-block" style="background-color: {bg_color};">
            <span style="font-size: 11px; font-weight: 700; color: {accent_bar}; letter-spacing: 2px; display: block; margin-bottom: 15px;">
                {data['step'].upper()}
            </span>
            
            <h2 style="font-size: 34px; font-weight: 900; line-height: 1.3; color: {title_color}; white-space: pre-wrap; margin-bottom: 12px;">
                {data['copy_title']}
            </h2>
            <p style="font-size: 16px; font-weight: 400; color: #555555; line-height: 1.6; white-space: pre-wrap; margin-bottom: 40px;">
                {data['copy_sub']}
            </p>
            
            <div style="width: 100%; height: 500px; background: linear-gradient(135deg, #eef2f3 0%, #8e9eab 100%); border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 30px; text-align: center; box-sizing: border-box; color: #ffffff;">
                <div style="background: rgba(0,0,0,0.6); padding: 15px 20px; border-radius: 4px; max-width: 90%;">
                    <span style="font-size: 12px; font-weight: 700; color: #ffce00; display: block; margin-bottom: 5px;">📸 GENERATION PROMPT ACTIVE</span>
                    <p style="font-size: 13px; font-family: monospace; margin: 0; text-align: left; line-height: 1.4; color: #eee;">
                        {data['prompt']}
                    </p>
                </div>
                <span style="font-size: 13px; margin-top: 20px; font-weight: 500; color: #222;">
                    [나노바나나 생성 이미지가 780px × 1000px 비율로 합성되는 영역]
                </span>
            </div>
            
            <div style="margin-top: 50px; width: 60px; height: 3px; background-color: {accent_bar};"></div>
        </div>
        """
        
    html_buffer += '</div>'
    
    # 캔버스 빌드 실행
    st.markdown(html_buffer, unsafe_allow_html=True)
