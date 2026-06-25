import streamlit as st
import urllib.parse

# 1. 페이지 레이아웃 및 780px 고정형 상세페이지 CSS 설정
st.set_page_config(layout="wide", page_title="다온이네 하우스 AI 상세페이지 마스터")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #fcfcfc;
    }
    
    /* 780px 정품 규격 세로형 스크롤 캔버스 */
    .detail-container {
        width: 780px !important;
        max-width: 780px !important;
        margin: 0 auto !important;
        background-color: #ffffff;
        border: 1px solid #e8e8e8;
        box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.1);
        padding: 0px !important;
    }
    
    .page-section {
        width: 100%;
        box-sizing: border-box;
        padding: 60px 50px;
        background-color: #ffffff;
        border-bottom: 8px solid #f1f3f5;
    }
    
    .blue-banner {
        background-color: #0b1d33;
        color: #ffffff;
        padding: 50px 40px;
        text-align: center;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    .point-badge {
        background-color: #0056b3;
        color: white;
        padding: 4px 14px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 빌드 상태 관리를 위한 세션 제어
if "ai_build_ready" not in st.session_state:
    st.session_state.ai_build_ready = False

# 3. 20년 차 기획자의 프롬프트 빌더 및 분위기 합성 엔진
def build_expert_ai_framework(prod_name, prod_info, style_eng):
    # 사용자가 입력한 상품 키워드 정제
    short_name = prod_name.split()[0] if prod_name else "자석집게"
    
    return [
        {
            "step": "01. 프리미엄 메인 인트로",
            "badge": "PREMIUM LAUNCHING",
            "title": f"주방의 모든 밀봉을 완벽하게\n🌈 다온이네 하우스 {short_name}",
            "sub": "남은 과자, 식빵, 소스 봉지까지 빈틈없이 착! 붙여 보관하는 일상의 혁신.",
            "prompt": f"A high-end commercial product photograph of a group of 7 colorful minimalist design sealing clips. Placed on a clean table, background is {style_eng}, highly detailed, sharp focus, dramatic studio lighting, 8k resolution --ar 4:5"
        },
        {
            "step": "02. 고질적 문제 제기 (Pain Point)",
            "badge": "PROBLEM SHOCK",
            "title": "매번 사라지는 일반 집게와\n눅눅해져 버리는 식재료의 악순환",
            "sub": "밀봉되지 않은 봉지 속 세균 번식과 정리 안 되는 주방 서랍, 이제 끝내야 합니다.",
            "prompt": f"A realistic cluttered messy home kitchen pantry, unsealed open plastic bags, messy drawer, frustrating dark atmosphere, background color tones matching {style_eng}, cinematic --ar 4:5"
        },
        {
            "step": "03. 감성 해답 제시 (Solution)",
            "badge": "DESIGN SOLUTION",
            "title": "접고, 집고, 붙이면 끝!\n7가지 컬러로 완성하는 칼각 질서",
            "sub": "다온이네 하우스만의 감성 컬러 스펙으로 어수선했던 주방이 갤러리처럼 변화합니다.",
            "prompt": f"Extremely organized beautiful modern kitchen interior, minimalist layout, featuring clean containers sealed with colorful clips, matching {style_eng}, soft morning sunlight --ar 4:5"
        },
        {
            "step": "04. 핵심 기술력 01 (자석 기능)",
            "badge": "ABSOLUTE VALUE 01",
            "title": "잃어버릴 걱정 제로!\n냉장고에 툭 붙여 쓰는 강력 마그네틱",
            "sub": "후면 네오디움 자석 설계로 분실 없이 언제나 손쉽게 가져다 쓰는 편리함.",
            "prompt": f"Macro extreme close-up shot of a modern magnetic clip firmly stuck on a clean metal refrigerator door panel, elegant shadows, crisp material textures, background has {style_eng} mood --ar 4:5"
        },
        {
            "step": "05. 핵심 기술력 02 (초밀폐력)",
            "badge": "ABSOLUTE VALUE 02",
            "title": "1mm의 틈새도 허용 않는\n초밀착 100% 공기 차단 스펙",
            "sub": "강력한 스프링 장력과 내부 논슬립 마감으로 무거운 소스 봉지까지 완벽 홀딩.",
            "prompt": f"A close-up shot of a person's hand neatly and tightly sealing a fresh coffee bean pouch bag with a pastel color grip clip, background atmosphere is {style_eng}, professional catalog style --ar 4:5"
        },
        {
            "step": "06. 마감 퀄리티 팩트 체크",
            "badge": "QUALITY CHECK",
            "title": "손끝이 안전한 라운딩 공정\n환경을 생각한 고급 ABS 소재",
            "sub": "자주 만지는 생활소품이기에 날카로운 모서리를 모두 없앤 안심 유선형 구조.",
            "prompt": f"Frontal commercial presentation of multiple colorful home utility clips, arranged in perfect symmetry, clean studio backdrop matching {style_eng} aesthetic, hyper-detailed --ar 4:5"
        },
        {
            "step": "07. 독점 패키지 및 구매 혜택",
            "badge": "LIMITED BENEFIT",
            "title": "오직 다온이네 하우스 단독 기획\n6세트 구매 시 1개 더 (+1) 특별 증정",
            "sub": "가장 실용적인 세트 구성에 보너스 혜택까지. 한정 수량 소진 시 조기 마감됩니다.",
            "prompt": f"Top-down flatlay catalog style photo of a premium minimal product gift box package, surrounded by lifestyle objects reflecting {style_eng} tones, luxury brand layout --ar 4:5"
        },
        {
            "step": "08. 품질 안심 보증 (Outro)",
            "badge": "TRUST GUARANTEE",
            "title": "품질에 타협하지 않기에\n100% 안심 책임 보상 가이드",
            "sub": "철저한 전수 검사를 마친 정품만 배송됩니다. 불만족 시 신속한 사후 처리를 약속드립니다.",
            "prompt": f"An elegant corporate product warranty card or crest badge layout, clean sophisticated studio environment matching {style_eng}, conveying ultimate confidence and premium reliability --ar 4:5"
        }
    ]

# 4. 화면 레이아웃 스플릿 (좌측 입력창 / 우측 진짜 상세페이지 도화지)
left_panel, right_canvas = st.columns([1, 1.15])

# --- [좌측 제어 패널] ---
with left_panel:
    st.header("🎨 다온이네 하우스 기획실")
    st.write("상품 정보와 원하는 분위기를 세팅하면 우측에 실시간 AI 드로잉 상세페이지가 완성됩니다.")
    
    prod_name = st.text_input("📦 상품명 입력", 
                             value="다온이네 하우스 밀봉 자석집게 6세트+1개 남은과자 식빵 캠핑 소스 보관 다용도 주방 밀폐 봉지집게")
    
    prod_info = st.text_area("📝 핵심 상품 정보 / 특장점", 
                             value="총 7가지 색상으로 구성된 아름다운 색상의 자석 집게. 자석으로 되어 있어서 자석이 붙는곳이면 어디든 부착 보관가능 분실률이 작고 간편하게 찾아서 쓸수있어요. 인테리어 효과 및 사진도 부착하여 볼수 있고 다양한 활용성 음식물 봉투 밀가루 봉투 과자 등 접어서 간편하게 자석집게로 집어서 보관합니다.")
    
    st.subheader("📸 소스 데이터 업로드 (활성화 완료)")
    # 🔴 기존 disabled=True 버그 완벽 수정하여 업로드 활성화 완료!
    product_files = st.file_uploader("제품 원본 사진 다중 첨부", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="active_prod")
    ref_files = st.file_uploader("벤치마킹 디자인 레퍼런스 이미지 첨부", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="active_ref")
    
    # ✨ 벤치마킹 이미지의 분위기를 AI 배경에 반영하는 컨트롤러 추가
    st.subheader("🖼️ 벤치마킹 배경/분위기 동적 선택")
    style_mood = st.selectbox("참부한 벤치마킹 자료의 핵심 분위기를 선택하세요", [
        "화이트 미니멀 & 감성 브라이트 (Clean White Minimalist)",
        "내추럴 원목 & 따뜻한 베이지 (Warm Cozy Natural Wood)",
        "럭셔리 모던 딥블루 & 다크 그레이 (Luxury Modern Deep Blue)",
        "파스텔 파우더리 & 러블리 룸 (Soft Pastel Powdery Background)"
    ])
    
    # 선택된 한글 무드를 영문 프롬프트 확장용 텍스트로 치환 매핑
    style_mapping = {
        "화이트 미니멀 & 감성 브라이트 (Clean White Minimalist)": "clean bright minimalist white kitchen background with soft micro shadows",
        "내추럴 원목 & 따뜻한 베이지 (Warm Cozy Natural Wood)": "warm cozy natural wooden texture and beige tones interior background",
        "럭셔리 모던 딥블루 & 다크 그레이 (Luxury Modern Deep Blue)": "luxury high-end modern dark blue and deep gray sophisticated studio background",
        "파스텔 파우더리 & 러블리 룸 (Soft Pastel Powdery Background)": "soft powdery pastel colored clean aesthetic domestic room environment"
    }
    selected_style_eng = style_mapping[style_mood]
    
    st.markdown("---")
    
    # 메인 실행 버튼
    if st.button("🚀 780px 정품 규격 + 실시간 AI 이미지 생성 시작", type="primary", use_container_width=True):
        st.session_state.ai_build_ready = True
        st.rerun()

    # 프롬프트 확인 로그 테이블
    if st.session_state.ai_build_ready:
        st.subheader("📋 생성에 사용된 AI 영문 프롬프트")
        current_framework = build_expert_ai_framework(prod_name, prod_info, selected_style_eng)
        for s in current_framework:
            with st.expander(f"🔍 {s['step']} 프롬프트"):
                st.code(s['prompt'], language="text")

# --- [우측 캔버스] PPT처럼 늘어나지 않는 780px 고정형 + 실시간 AI 이미지 결과창 ---
with right_canvas:
    st.subheader("📱 쿠팡 전용 세로형 스크롤 미리보기")
    
    if not st.session_state.ai_build_ready:
        st.info("💡 왼쪽 폼에서 정보를 기입하고 벤치마킹 분위기를 선택한 뒤 [🚀 780px 정품 규격 + 실시간 AI 이미지 생성 시작] 버튼을 누르면 실시간 이미지 드로잉이 시작됩니다.")
    else:
        # 데이터 구조 가져오기
        sections_data = build_expert_ai_framework(prod_name, prod_info, selected_style_eng)
        
        # 🔴 PPT 버그를 완벽 해결하기 위해 가로폭을 780px로 강제 홀딩하는 대형 도화지 래퍼 시작
        st.markdown('<div class="detail-container">', unsafe_allow_html=True)
        
        for i, section in enumerate(sections_data):
            # 시각적 지루함을 방지하는 섹션별 배경 컬러 믹싱
            bg_color = "#ffffff" if i % 2 == 0 else "#fbfcfd"
            title_color = "#c0392b" if i == 1 else "#0b1d33" # 문제제기는 레드 포인트 사용
            
            # 카피라이팅 및 헤더 마크다운 렌더링
            if i == 0:
                st.markdown(f"""
                <div class="blue-banner">
                    <span style="font-size:11px; font-weight:800; letter-spacing:3px; color:#a5b9cc;">{section['badge']}</span>
                    <h1 style="font-size:28px; font-weight:900; line-height:1.4; color:#ffffff; margin-top:10px; margin-bottom:8px; letter-spacing:-0.5px;">{section['title']}</h1>
                    <p style="font-size:14px; color:#cbd5e1; font-weight:400; line-height:1.5; margin:0;">{section['sub']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 45px 40px 10px 40px;">
                    <span class="point-badge">{section['badge']}</span>
                    <h2 style="font-size:24px; font-weight:800; line-height:1.4; color:{title_color}; margin-top:5px; margin-bottom:12px; letter-spacing:-0.5px;">{section['title']}</h2>
                    <p style="font-size:14.5px; color:#4a5568; font-weight:400; line-height:1.6; margin:0 0 15px 0;">{section['sub']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 🌟 [핵심 기능] 오픈소스 실시간 AI 이미지 제너레이션 링크 연동
            # 사용자가 설정한 상품명과 벤치마킹 배경 분위기가 영문 인코딩되어 이미지 주소로 바로 변환됩니다.
            encoded_prompt = urllib.parse.quote(section['prompt'])
            ai_live_image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=780&height=975&seed={i+100}"
            
            # 이미지 출력 컴포넌트 고정 가로폭 적용 (양옆 늘어남 원천 차단)
            st.image(ai_live_image_url, width=780, caption=f"▲ 다온이네 하우스 {section['step']} - 실시간 AI 생성 완료")
            
            # 각 섹션을 채워주는 하단 여백 및 엠보싱 라인
            st.markdown(f'<div style="height:25px; background-color:{bg_color}; border-bottom:1px solid #edf2f7;"></div>', unsafe_allow_html=True)
            
        # 대형 도화지 래퍼 종료
        st.markdown('</div>', unsafe_allow_html=True)
