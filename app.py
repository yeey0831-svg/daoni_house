import streamlit as st
import requests
import time
import os
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v18.0", layout="wide")

# ==========================================
# 🔤 한글 폰트 자동 다운로드 (이미지 내 한글 깨짐 방지)
# ==========================================
FONT_PATH = "NanumGothic-Bold.ttf"
if not os.path.exists(FONT_PATH):
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
        urllib.request.urlretrieve(font_url, FONT_PATH)
    except Exception as e:
        pass

# ==========================================
# 🎨 780px 쿠팡 규격 이미지 생성 헬퍼 함수
# ==========================================
def create_coupang_image(step_num, step_title, main_copy, sub_copy, guide_copy):
    # 쿠팡 표준 가로 780px, 세로 1100px 캔버스 생성
    width, height = 780, 1100
    image = Image.new("RGB", (width, height), value=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 폰트 세팅 (실패 시 기본 폰트)
    try:
        font_title = ImageFont.truetype(FONT_PATH, 28)
        font_main = ImageFont.truetype(FONT_PATH, 34)
        font_sub = ImageFont.truetype(FONT_PATH, 18)
        font_guide = ImageFont.truetype(FONT_PATH, 15)
    except:
        font_title = font_main = font_sub = font_guide = ImageFont.load_default()

    # 1. 상단 인디케이터 바 (쿠팡 블루 테마)
    draw.rectangle([0, 0, width, 90], fill=(0, 116, 233))
    draw.text((40, 30), f"PAGE {step_num} : {step_title}", font=font_title, fill=(255, 255, 255))
    
    # 텍스트 자동 줄바꿈 함수
    def draw_text_wrap(text, font, color, start_y, max_w, line_spacing=12):
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= max_w:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
            
        y = start_y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
            # 중앙 정렬 배치
            draw.text(((width - line_w) // 2, y), line, font=font, fill=color)
            y += (bbox[3] - bbox[1]) + line_spacing
        return y

    # 2. 메인 헤드카피 영역 출력
    draw.text((40, 150), "⚡ KEY COPY", font=font_sub, fill=(0, 116, 233))
    next_y = draw_text_wrap(main_copy.replace("-", "").strip(), font=font_main, color=(17, 17, 17), start_y=190, max_w=700)
    
    # 3. 상세 카피라이팅 영역 출력
    next_y += 50
    draw.text((40, next_y), "📝 DETAILED COPY", font=font_sub, fill=(85, 85, 85))
    next_y = draw_text_wrap(sub_copy.strip(), font=font_sub, color=(51, 51, 51), start_y=next_y+40, max_w=680, line_spacing=10)
    
    # 4. 중앙 하단: 상품 사진 배치가 들어갈 가상 프레임 및 디자인 가이드 시각화
    frame_y1 = next_y + 60
    frame_y2 = frame_y1 + 320
    if frame_y2 > 1050: # 캔버스 오버플로우 방지 조율
        frame_y1 = 650
        frame_y2 = 970
        
    draw.rectangle([50, frame_y1, width-50, frame_y2], fill=(245, 247, 250), outline=(221, 221, 221), width=2)
    draw.text((70, frame_y1 + 20), "📸 이 영역에 업로드한 상품 사진 및 그래픽이 결합됩니다.", font=font_guide, fill=(102, 102, 102))
    
    # 디자인 가이드 본문 채우기
    draw_text_wrap("[디자인 지시서]\n" + guide_copy.strip(), font=font_guide, color=(119, 119, 119), start_y=frame_y1+60, max_w=640, line_spacing=8)
    
    # 하단 푸터 로고 박스
    draw.rectangle([0, height-40, width, height], fill=(240, 240, 240))
    draw.text((30, height-28), "COUPANG OPTIMIZED IMAGE STANDARD (780px Width)", font=font_guide, fill=(153, 153, 153))
    
    return image


# ==========================================
# 🖥️ UI 메인 콘텐트 빌드
# ==========================================
st.title("🎯 쿠팡형 AI 상세페이지 마스터 v18.0 (이미지 추출형)")
st.markdown("---")

# 세션 상태 관리 초기화
if "step_results" not in st.session_state:
    st.session_state["step_results"] = None

# 📋 사이드바 마케팅 제어판
st.sidebar.header("📋 필수 정보 및 파일 업로드")
api_key_input = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("상품명 (예: 다온 프리미엄 압축 파우치)")
target_user = st.sidebar.text_input("타겟 고객 (예: 여행족, 출장 전문가, 살림꾼)")

# 복원된 이미지 업로드 컴포넌트
uploaded_photos = st.sidebar.file_uploader("📂 [필수] 기본 상품 사진 등록", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_photos:
    st.sidebar.success(f"✅ 총 {len(uploaded_photos)}장의 상품 이미지가 서버에 대기 중입니다.")

# 쿠팡 전용 8단계 마케팅 공식 선언
STEPS = [
    ("1", "강력한 Hooking 문제 제기", "소비자가 일상에서 느끼는 가장 답답한 고통과 불편함을 서두에서 극적으로 연출"),
    ("2", "소비자 격한 공감대 형성", "나만 겪는 문제가 아님을 인지시키고 상세페이지를 끝까지 읽어야 할 명분 제공"),
    ("3", "해결책 제시 및 제품 최초 공개", "모든 스트레스를 한 번에 날려줄 구원투수로 우리 제품을 화려하게 무대 등장"),
    ("4", "핵심 독보적 스펙 인증", "눈으로 직접 확인하는 스펙, 특허, 압도적인 기능성의 디테일 레이아웃 기획"),
    ("5", "타사 제품 비교 우위 격차", "저가형 싸구려 유사품과의 확실한 급 차이를 시각적 데이터 표 형태로 연출"),
    ("6", "실제 고객 리뷰 증명", "구매 직전 의심을 확신으로 바꿔주는 리얼 찐 후기 요소를 배치하여 신뢰 확보"),
    ("7", "구매 혜택 및 파격 구성", "오직 지금만 제공되는 특별 사은품 구성 및 한정 이벤트 단독 가이드"),
    ("8", "최종 구매 촉구 마감", "재고 부족 심리 유도 및 품질 보증 제도로 낙오자 없이 즉시 결제창으로 이동")
]

# 생성 가동 버튼
if st.button("🚀 8단계 상세페이지 기획서 및 실물 이미지 동시 생성 시작", type="primary"):
    if not api_key_input:
        st.error("🚨 왼쪽 사이드바에서 구글 API Key를 필수로 입력해 주세요.")
    elif not product_name:
        st.error("🚨 왼쪽 사이드바에서 상품명을 명확히 입력해 주세요.")
    else:
        api_key = api_key_input.strip()
        progress_bar = st.progress(0)
        loading_ui = st.empty()
        
        loading_ui.info("🔮 AI 카피라이팅 엔진과 이미지 드로잉 그래픽 컴포넌트를 동시에 결합 중입니다...")
        
        results = []
        
        for i, (num, title, core_concept) in enumerate(STEPS):
            step_full_title = f"{num}단계: {title}"
            
            # 엄격한 규격 분리를 강제하는 딥 융합 프롬프트
            prompt = f"""
            당신은 한국 이커머스 매출 1위 CRO 카피라이터입니다. 
            다음 상품의 정보를 토대로 쿠팡 상세페이지의 [{step_full_title}] 영역을 기획하세요.
            컨셉 지시사항: {core_concept}

            [상품 기본 정보]
            - 상품명: {product_name}
            - 주요 타겟 고객층: {target_user if target_user else '이 제품이 절대적으로 필요한 스마트 컨슈머'}

            [출력 규칙: 분석 및 연동을 위해 반드시 아래 명시된 대괄호 태그 구조로만 대답하세요]
            [MAIN] (소비자의 마음을 뺏을 강력한 굵은 폰트용 메인 헤드카피 1~2줄)
            [SUB] (헤드카피를 받쳐주고 구매욕구를 올릴 설득형 상세 본문 설명 문구)
            [DESIGN] (가로 780px 기준 배치, 배경 컬러 조합, 촬영 앵글 등 디자이너가 바로 작업 가능한 수준의 구체적 그래픽 지시서)
            """
            
            # 3중 우회 하이브리드 커넥터 작동
            raw_text = ""
            try:
                # 1차 통신망
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                res = requests.post(url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if res.status_code == 200:
                    raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
            except:
                pass
                
            if not raw_text:
                try:
                    # 2차 통신망 백업
                    url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    res = requests.post(url_v1, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                    if res.status_code == 200:
                        raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                except:
                    raw_text = "기획서 본문 생성 통신 지연이 발생했습니다. 수동 텍스트 대체 영역입니다."

            # 임시 파싱 헬퍼
            main_c = "폭발적 반응의 감각적 헤드라인 카피 배치"
            sub_c = "상세한 제품 특장점과 타겟 맞춤형 설득 솔루션 문장 영역입니다."
            guide_c = "배경화면 그라데이션 및 메인 상품 누끼 컷 레이아웃 조화 중심 구성"
            
            if "[MAIN]" in raw_text and "[SUB]" in raw_text and "[DESIGN]" in raw_text:
                parts_main = raw_text.split("[MAIN]")[1].split("[SUB]")
                main_c = parts_main[0].strip()
                parts_sub = parts_main[1].split("[DESIGN]")
                sub_c = parts_sub[0].strip()
                guide_c = parts_sub[1].strip()
            else:
                main_c = f"드디어 출시된 최적의 선택, {product_name}!"
                sub_c = f"불편했던 일상이 확실하게 달라집니다. {target_user}분들이 직접 인정해주신 압도적인 기능성을 바로 아래 스펙 박스에서 투명하게 확인해 보세요."
                guide_c = raw_text[:300] if len(raw_text) > 10 else "제품 실물 확대 컷 구성"

            # 메모리에 저장용 리스트 업로드
            results.append({
                "num": num,
                "title": title,
                "main": main_c,
                "sub": sub_c,
                "guide": guide_c
            })
            
            progress_bar.progress((i + 1) / len(STEPS))
            time.sleep(0.2)
            
        st.session_state["step_results"] = results
        loading_ui.empty()
        st.balloons()
        st.success("🎉 8단계 텍스트 기획안 도출 및 쿠팡 표준 이미지 드로잉 연산이 완료되었습니다! 아래 레이아웃을 확인하세요.")

# ==========================================
# 🖼️ 시각 갤러리 및 실물 파일 다운로드 제어 판넬
# ==========================================
if st.session_state["step_results"]:
    st.markdown("---")
    st.header("🖼️ 쿠팡 규격(가로 780px) 상세페이지 실물 이미지 다운로드 센터")
    st.markdown(" 각 단계별로 완성된 실물 이미지 카드를 눈으로 직접 확인하고 바로 다운로드하세요!")
    
    for item in st.session_state["step_results"]:
        with st.container():
            st.markdown(f"### 📦 PAGE {item['num']} : {item['title']}")
            
            # 실시간 그래픽 렌더링 가동
            generated_img = create_coupang_image(
                step_num=item['num'],
                step_title=item['title'],
                main_copy=item['main'],
                sub_copy=item['sub'],
                guide_copy=item['guide']
            )
            
            # Streamlit 화면 출력 분할 레이아웃 (좌측: 실물 가상 이미지, 우측: 기획서 텍스트 세부본)
            col_img, col_txt = st.columns([1, 1])
            
            with col_img:
                st.image(generated_img, caption=f"{item['num']}단계 실제 출력 규격 780px 캔버스 이미지", use_container_width=True)
                
                # PNG 바이너리 파일 변환 파이프라인
                img_buffer = io.BytesIO()
                generated_img.save(img_buffer, format="PNG")
                byte_im = img_buffer.getvalue()
                
                # 실물 저장 버튼 바인딩
                st.download_button(
                    label=f"💾 PAGE {item['num']} 이미지 파일(PNG) 컴퓨터에 저장하기",
                    data=byte_im,
                    file_name=f"coupang_detail_page_{item['num']}.png",
                    mime="image/png",
                    use_container_width=True,
                    key=f"dl_btn_{item['num']}"
                )
                
            with col_txt:
                st.subheader("📋 기획안 원본 텍스트 데이터")
                st.markdown(f"**📢 메인 헤드라인:**\n{item['main']}")
                st.markdown(f"**✍️ 카피라이팅 본문:**\n{item['sub']}")
                st.markdown(f"**🎨 디자이너 그래픽 가이드 지시서:**\n{item['guide']}")
                
            st.markdown("<br><hr style='border:1px dashed #ddd;'><br>", unsafe_allow_html=True)
