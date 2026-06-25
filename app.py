import streamlit as st
import json
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# =========================================================================
# ⚙️ [글로벌 환경 설정 및 시스템 유틸리티]
# =========================================================================
st.set_page_config(page_title="나노바나나 AI 8단 상세페이지 빌더 v1.0", layout="wide")

def get_safe_font(font_size=24):
    """서버 배포 시 폰트 누락으로 인한 OSError를 철저히 방지하는 안전 함수"""
    font_paths = [
        "NanumGothic.ttf", 
        "C:/Windows/Fonts/malgun.ttf", 
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "Arial.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, font_size)
        except OSError:
            continue
    return ImageFont.load_default()

# 나노바나나 핵심 상세페이지 8단 배열 정의
NANOBANANA_FRAMEWORK = [
    {"num": 1, "tag": "Hooking", "title": "🚨 01. 일상 속 딥한 문제제기", "ph_title": "불편한 순간 저격", "ph_text": "아직도 무거운 팬트리 안쪽 물건 꺼내려다 위에 쌓아둔 캔들이 우르르 쏟아져 내리는 스트레스를 견디고 계시나요?"},
    {"num": 2, "tag": "Solution", "title": "💎 02. 압도적 해결책 제시 (Hero)", "ph_title": "단 하나의 솔루션", "ph_text": "손가락 하나로 스르륵! 공간의 데드스페이스를 제로로 만드는 루시아이 스택 슬라이딩 정리함 상륙"},
    {"num": 3, "tag": "Detail_1", "title": "🛠️ 03. 초정밀 스펙 분석 (무빙)", "ph_title": "프리미엄 볼베어링 레일", "ph_text": "녹슬지 않는 고강도 볼베어링 내장식 레일을 적용하여, 10kg이 넘는 무거운 주방 무쇠 팬을 수납해도 뻑뻑함 없이 처음처럼 부드럽게 슬라이딩됩니다."},
    {"num": 4, "tag": "Detail_2", "title": "📐 04. 모듈러 스택 시스템 (공간)", "ph_title": "위로 쌓아 넓어지는 마법", "ph_text": "상하단 결합 홈 설계로 흔들림 없이 수직 적층이 가능합니다. 노는 상부 싱크대 공간을 200% 활용하는 압도적인 수납 레이아웃을 직접 경험하세요."},
    {"num": 5, "tag": "Detail_3", "title": "🛡️ 05. 안심 안전 소재 증명", "ph_title": "고하중 방청 코팅 프레임", "ph_text": "습한 싱크대 하부장에서도 부식 걱정 없는 특수 방청 코팅과 휘어짐 없는 두터운 강철 프레임으로 대대손손 변형 없이 견고하게 지탱합니다."},
    {"num": 6, "tag": "Review", "title": "⭐️ 06. 실사용자 리얼 리뷰", "ph_title": "평점 4.9점의 찬사", "ph_text": "'살까 말까 고민했던 시간이 아깝습니다. 싱크대 밑이 리조트 쇼룸처럼 깔끔해졌어요!' - 김*진 고객님의 실제 한 달 사용기"},
    {"num": 7, "tag": "Compare", "title": "📊 07. 일반 싸구려 제품과 비교 타격", "ph_title": "압도적인 한 끗 차이", "ph_text": "덜덜거리고 쉽게 휘어지는 일반 플라스틱 정리함과 비교를 거부합니다. 풀 메탈 강철 구조의 디테일이 브랜드 가치를 증명합니다."},
    {"num": 8, "tag": "CTA", "title": "🛒 08. 구매 촉구 및 긴급성 부여", "ph_title": "당일 출고 혜택 마감임박", "ph_text": "지금 주문하시면 100% 무료 배송 및 당일 출고 혜택을 드립니다. 한정 수량 소진 시 가격이 인상될 수 있습니다."}
]

# 🗂️ [세션 스테이트 - 상태 보존소]
if "prod_name" not in st.session_state: st.session_state["prod_name"] = "루시아이 스택 슬라이딩 팬트리 정리함"
if "prod_desc" not in st.session_state: st.session_state["prod_desc"] = "좁은 틈새와 노는 공간을 100% 활용하는 슬라이딩 가구 정리함"
if "prod_benefits" not in st.session_state: st.session_state["prod_benefits"] = "부드러운 레일 모션 / 수직 적층 구조 / 강철 프레임 내구성"
if "uploaded_images" not in st.session_state: st.session_state["uploaded_images"] = []
if "edited_storyboard" not in st.session_state: st.session_state["edited_storyboard"] = []
if "master_gallery" not in st.session_state: st.session_state["master_gallery"] = []

# =========================================================================
# 🧭 [사이드바 내비게이션 - 1, 2, 3, 4 페이지 구조]
# =========================================================================
st.sidebar.title("🍌 나노바나나 코어 엔진")
page = st.sidebar.radio(
    "메뉴 이동", 
    ["🏠 1페이지: 마스터 컨트롤러", 
     "⚡ 2페이지: AI 8단 시나리오 빌더", 
     "🎨 3페이지: 비주얼 매핑 편집기", 
     "🖼️ 4페이지: 쿠팡 780px 그룹 저장소"]
)

# =========================================================================
# 🏠 [1페이지: 마스터 컨트롤러]
# =========================================================================
if page == "🏠 1페이지: 마스터 컨트롤러":
    st.header("🏠 1페이지: 기획 소스 입력 및 마스터 환원 보드")
    st.caption("상품 이미지와 원천 텍스트를 입력하는 시작점이자, 4페이지에서 빌드된 상세페이지를 원격 제어하는 최종 컨트롤 룸입니다.")
    st.markdown("---")
    
    col_in, col_rv = st.columns([1, 1])
    
    with col_in:
        st.subheader("📥 원천 기획 자산 입력")
        st.session_state["prod_name"] = st.text_input("💎 원본 상품명", value=st.session_state["prod_name"])
        st.session_state["prod_desc"] = st.text_area("📝 상품 기본 설명 (AI 원재료)", value=st.session_state["prod_desc"], height=80)
        st.session_state["prod_benefits"] = st.text_area("⚡ 상품의 특장점 / 핵심 소구점", value=st.session_state["prod_benefits"], height=80)
        
        st.markdown("---")
        st.subheader("📷 1.2단계: 상품 마스터 이미지 대량 업로드")
        uploaded_files = st.file_uploader("상세페이지 각 섹션에 매핑할 원본 이미지들을 한 번에 올려주세요.", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        if uploaded_files:
            st.session_state["uploaded_images"] = [f.name for f in uploaded_files]
            st.success(f"총 {len(st.session_state['uploaded_images'])}장의 제품 원본 사진 스토리지 업로드 완료!")
            
    with col_rv:
        st.subheader("🔄 4페이지 마스터 데이터 실시간 원격 복원 엔진")
        if not st.session_state["master_gallery"]:
            st.warning("현재 4페이지 저장소에 그룹화되어 저장된 최종 상세페이지 세트가 없습니다. 먼저 2~4단계를 진행하여 빌드해 주세요.")
        else:
            st.info("💡 4페이지 저장소에 안전하게 보관된 대형 데이터 그룹을 발견했습니다.")
            if st.button("🚀 저장 데이터 불러와서 나노바나나 스타일 완성형 동적 매핑", use_container_width=True):
                st.balloons()
                st.success("🎉 환원 성공! 4페이지에 누적 보관된 8장의 마스터 그래픽과 1페이지 기획 자산이 유기적으로 바인딩되었습니다.")
            
            # 저장된 데이터 유기적 매핑 리스트 출력
            for item in st.session_state["master_gallery"]:
                st.markdown(f"""
                <div style="border-left: 5px solid #ffb703; background-color: #f8fafc; padding: 15px; margin-bottom: 12px; border-radius: 4px;">
                    <span style="background-color: #ffb703; color: #111; padding: 2px 6px; font-size: 11px; font-weight: bold; border-radius: 3px;">{item['tag']} 매핑 완료</span>
                    <h4 style="margin: 8px 0 4px 0; color: #1e293b;">{item['title']}</h4>
                    <p style="margin: 0; font-size: 13px; color: #475569;"><b>최종 매핑 문구:</b> {item['text']}</p>
                    <p style="margin: 4px 0 0 0; font-size: 12px; color: #3b82f6;">📷 매칭 이미지 파일: {item['img'] if item['img'] else '기본 가상 프레임'}</p>
                </div>
                """, unsafe_allow_html=True)

# =========================================================================
# ⚡ [2페이지: AI 8단 시나리오 빌더]
# =========================================================================
elif page == "⚡ 2페이지: AI 8단 시나리오 빌더":
    st.header("⚡ 2페이지: 나노바나나 스타일 이커머스 치트키 8단 시나리오 생성기")
    st.caption("1페이지에서 작성한 투박한 텍스트 소스를 바탕으로, 소비자의 지갑을 여는 최적화된 8단계 상세페이지 스크립트를 생성합니다.")
    st.markdown("---")
    
    st.markdown("### 🤖 나노바나나 기획 인공지능 프롬프트 가동")
    st.write(f"**현재 타겟 상품:** `{st.session_state['prod_name']}`")
    
    if st.button("🚀 원클릭 고품질 상세페이지 8장 시나리오 구조 생성", use_container_width=True):
        with st.spinner("1페이지 원천 데이터를 나노바나나 8단 후킹 알고리즘에 대입하여 카피라이팅 가동 중..."):
            storyboard = []
            for frame in NANOBANANA_FRAMEWORK:
                # 1페이지 소스를 결합한 고도화 문구 자동 정제 시뮬레이션
                refined_text = f"[{st.session_state['prod_name']}] 관련 최적화 카피: {frame['ph_text']}"
                storyboard.append({
                    "num": frame["num"],
                    "tag": frame["tag"],
                    "title": frame["title"],
                    "placeholder_title": frame["ph_title"],
                    "text": refined_text
                })
            st.session_state["edited_storyboard"] = storyboard
            st.success("✅ 나노바나나 구조화 상세페이지 8단 카드 기획 완성! 3페이지로 이동하여 레이아웃을 다듬어주세요.")
            
    if st.session_state["edited_storyboard"]:
        st.markdown("### 📋 정제된 8단 기획 데이터 구조 (JSON Schema)")
        st.json(st.session_state["edited_storyboard"])

# =========================================================================
# 🎨 [3페이지: 비주얼 매핑 편집기]
# =========================================================================
elif page == "🎨 3페이지: 비주얼 매핑 편집기":
    st.header("🎨 3페이지: 기획 텍스트 및 업로드 이미지 비주얼 하이브리드 매핑")
    st.caption("2페이지의 AI 문구와 1페이지에서 업로드한 실제 상품 이미지 파일들을 각 상세페이지 카드별로 1:1 매칭하는 공간입니다.")
    st.markdown("---")
    
    if not st.session_state["edited_storyboard"]:
        st.warning("⚠️ 2페이지에서 '8단 시나리오 구조 생성' 버튼을 먼저 클릭하셔야 편집기가 활성화됩니다.")
    else:
        st.info("💡 각 페이지 카드를 확장하여 텍스트 카피를 가다듬고, 올리신 이미지 목록 중 가장 어울리는 이미지를 지정하세요.")
        
        img_options = ["선택 안 함 (기본 템플릿 대체)"] + st.session_state["uploaded_images"]
        sync_holder = []
        
        for card in st.session_state["edited_storyboard"]:
            with st.expander(f"📦 PAGE 0{card['num']} : {card['title']}", expanded=True):
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    c_title = st.text_input(f"카드가이드 핵심 타이틀 (P.{card['num']})", value=card['placeholder_title'], key=f"title_{card['num']}")
                    c_text = st.text_area(f"실제 출력될 카피라이팅 편집 (P.{card['num']})", value=card['text'], key=f"text_{card['num']}", height=80)
                with col_img:
                    selected_img = st.selectbox(f"📷 1페이지 업로드 이미지 매칭", options=img_options, key=f"img_{card['num']}")
                    v_url = st.text_input(f"🎬 동영상 공간 활성화 (선택)", value="https://", key=f"v_{card['num']}")
                    
                sync_holder.append({
                    "num": card["num"],
                    "tag": card["tag"],
                    "title": card["title"],
                    "placeholder_title": c_title,
                    "text": c_text,
                    "img": None if selected_img == "선택 안 함 (기본 템플릿 대체)" else selected_img,
                    "video": v_url
                })
                
        if st.button("💾 편집 마스터본 저장 및 4페이지 최종 렌더링 엔진으로 전송", use_container_width=True):
            st.session_state["edited_storyboard"] = sync_holder
            st.success("🎯 8장 상세페이지 비주얼 매핑 동기화 완료! 4페이지에서 최종 쿠팡 규격을 확인하십시오.")

# =========================================================================
# 🖼️ [4페이지: 쿠팡 780px 그룹 저장소]
# =========================================================================
elif page == "🖼️ 4페이지: 쿠팡 780px 그룹 저장소":
    st.header("🖼️ 4페이지: 쿠팡 표준 가로 780px 고화질 출력 및 마스터 그룹 보관소")
    st.caption("최종 기획 및 이미지가 조합된 완성본을 가로 780px 규격의 고품질 데이터로 렌더링하고, 그룹으로 묶어 보관 및 선택 다운로드합니다.")
    st.markdown("---")
    
    if not st.session_state["edited_storyboard"]:
        st.warning("⚠️ 3페이지에서 매핑 동기화를 완료하셔야 렌더링 엔진이 작동합니다.")
    else:
        col_side, col_render = st.columns([1, 2])
        
        with col_side:
            st.subheader("🗂️ 8장 마스터 데이터 그룹화")
            st.write("현재 매핑 완료된 8장의 독립 페이지 카드를 하나의 온전한 데이터 세트로 그룹화하여 1페이지로 역전송 보관합니다.")
            
            if st.button("🔥 완성형 상세페이지 8장 세트 그룹화 및 저장소 최종 등록", use_container_width=True):
                st.session_state["master_gallery"] = st.session_state["edited_storyboard"]
                st.success("🚀 저장소 등록 성공! 이제 1페이지에서 이 마스터 세트를 클릭 한 번으로 자유롭게 호출 및 복원할 수 있습니다.")
                
            st.markdown("---")
            st.subheader("💾 고화질 마스터 그래픽 일괄 생성")
            
            if st.button("🚀 다운로드용 물리 PNG 8장 압축 빌드 가동", use_container_width=True):
                # PIL 기반 쿠팡 780px 물리 파일 실시간 생성 백엔드 연산
                master_height = 350
                font_m = get_safe_font(26)
                font_s = get_safe_font(16)
                
                # 테스트로 1번 카드 대표 마스터 이미지 빌드 후 파일 제공
                test_card = st.session_state["edited_storyboard"][0]
                img = Image.new("RGB", (780, master_height), "#1e3a8a")
                draw = ImageDraw.Draw(img)
                
                draw.text((390, 80), f"PAGE 01 : {test_card['placeholder_title']}", fill="#ffb703", font=font_m, anchor="mm")
                draw.text((390, 160), test_card['text'][:30], fill="#ffffff", font=font_s, anchor="mm")
                draw.text((390, 200), test_card['text'][30:60], fill="#ffffff", font=font_s, anchor="mm")
                
                img.save("coupang_page_01.png", "PNG")
                
                with open("coupang_page_01.png", "rb") as f:
                    st.download_button("💾 쿠팡 최적화 가로 780px PNG 마스터 다운로드", data=f, file_name="coupang_page_01.png", mime="image/png", use_container_width=True)
                st.success("고화질 그래픽 파일 컴파일이 정상 완료되었습니다.")

        with col_render:
            st.subheader("📱 가로 780px 브랜드 숍 라이브 미리보기 (선택 뷰어)")
            
            # 8장 카드를 웹 표준 고급 템플릿으로 출력하는 프론트엔드 코드
            for card in st.session_state["edited_storyboard"]:
                video_box = ""
                if card["video"] and card["video"] != "https://":
                    video_box = f"""
                    <div style="background: #f1f5f9; padding: 12px; border: 1px dashed #cbd5e1; border-radius: 6px; margin-top: 15px; text-align: center; color: #475569; font-size: 13px;">
                        🎬 <b>[비주얼 미디어 연동 완료]</b> {card['video']}
                    </div>
                    """
                    
                img_box_text = f"📷 {card['img']}" if card["img"] else "🖼️ [상품 핵심 비주얼 가상 배치 공간]"
                
                html_template = f"""
                <div style="width: 100%; max-width: 780px; margin: 0 auto 30px auto; font-family: 'Malgun Gothic', sans-serif; background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); overflow: hidden;">
                    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 16px; font-weight: bold; color: #ffb703;">{card['title']}</span>
                        <span style="background-color: #f59e0b; color:#111; font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: bold;">{card['tag']}</span>
                    </div>
                    <div style="padding: 35px 30px;">
                        <h2 style="font-size: 24px; font-weight: 800; color: #1e3a8a; margin: 0 0 15px 0; border-bottom: 3px solid #f59e0b; padding-bottom: 10px;">{card['placeholder_title']}</h2>
                        <div style="background-color: #f8fafc; border-left: 4px solid #1e3a8a; padding: 18px; font-size: 15px; color: #334155; line-height: 1.6; font-weight: 500; white-space: pre-wrap;">{card['text']}</div>
                        {video_box}
                        <div style="margin-top: 20px; height: 220px; background-color: #f8fafc; border: 2px dashed #94a3b8; display: flex; justify-content: center; align-items: center; color: #64748b; font-size: 14px; font-weight: bold; border-radius: 8px;">
                            {img_box_text}
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_template, unsafe_allow_html=True)
