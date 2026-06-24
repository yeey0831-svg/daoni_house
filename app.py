import streamlit as st
import requests
import time
import os
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v20.0", layout="wide")

# ==========================================
# 🔤 한글 폰트 자동 세팅 (이미지/GIF 깨짐 방지)
# ==========================================
FONT_PATH = "NanumGothic-Bold.ttf"
if not os.path.exists(FONT_PATH):
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
        urllib.request.urlretrieve(font_url, FONT_PATH)
    except:
        pass

# ==========================================
# 🖼️ 1. 780px 쿠팡 규격 이미지 생성 엔진
# ==========================================
def create_coupang_image(step_num, step_title, main_copy, sub_copy, guide_copy, uploaded_photo=None):
    width = 780
    height = 1400 
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    try:
        font_title = ImageFont.truetype(FONT_PATH, 26)
        font_main = ImageFont.truetype(FONT_PATH, 30)
        font_sub = ImageFont.truetype(FONT_PATH, 18)
        font_guide = ImageFont.truetype(FONT_PATH, 15)
    except:
        font_title = font_main = font_sub = font_guide = ImageFont.load_default()

    # 상단 인디케이터 바 (상위 1% 브랜드 테마 컬러)
    draw.rectangle([0, 0, width, 90], fill=(23, 28, 36))
    draw.text((40, 32), f"🔥 SUCCESS PATTERN PAGE {step_num} : {step_title}", font=font_title, fill=(255, 215, 0))
    
    def draw_text_wrap(text, font, color, start_y, max_w, line_spacing=12, align="center"):
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
            if align == "center":
                draw.text(((width - line_w) // 2, y), line, font=font, fill=color)
            else:
                draw.text((40, y), line, font=font, fill=color)
            y += (bbox[3] - bbox[1]) + line_spacing
        return y

    # 카피라이팅 영역 출력
    next_y = 140
    draw.text((40, next_y), "⚡ BENCHMARK HOOKING COPY", font=font_sub, fill=(255, 51, 102))
    next_y = draw_text_wrap(main_copy.replace("-", "").strip(), font=font_main, color=(17, 17, 17), start_y=next_y+35, max_w=700)
    
    next_y += 40
    draw.text((40, next_y), "📝 SELLING SOLUTION", font=font_sub, fill=(73, 80, 87))
    next_y = draw_text_wrap(sub_copy.strip(), font=font_sub, color=(52, 58, 64), start_y=next_y+35, max_w=700, line_spacing=10)
    
    # 이미지 합성 영역
    next_y += 40
    frame_y1 = next_y
    frame_y2 = frame_y1 + 400
    draw.rectangle([40, frame_y1, width-40, frame_y2], fill=(248, 249, 250), outline=(222, 226, 230), width=2)
    
    if uploaded_photo is not None:
        try:
            uploaded_photo.seek(0)
            prod_img = Image.open(uploaded_photo)
            prod_img.thumbnail((640, 360))
            p_w, p_h = prod_img.size
            image.paste(prod_img, ((width - p_w) // 2, frame_y1 + (400 - p_h) // 2))
        except:
            draw.text((60, frame_y1 + 20), "📸 이미지 결합 중 연산 에러", font=font_guide, fill=(255, 0, 0))
    else:
        draw.text((60, frame_y1 + 180), "🛒 [기본 배치 존] 우측에서 제작한 마케팅 GIF 움짤이 이 자리에 결합됩니다.", font=font_guide, fill=(140, 140, 140))
        
    # 디자인 연출 지시서 영역
    next_y = frame_y2 + 40
    draw.text((40, next_y), "🎨 HIGH-CONVERSION DESIGN VIBE", font=font_sub, fill=(0, 116, 233))
    next_y = draw_text_wrap(guide_copy.strip(), font=font_guide, color=(108, 117, 125), start_y=next_y+35, max_w=700, line_spacing=8, align="left")
    
    draw.rectangle([0, height-50, width, height], fill=(241, 243, 245))
    draw.text((40, height-33), "SUCCESS BENCHMARKING MASTER STANDARD (780px Width)", font=font_guide, fill=(134, 142, 150))
    
    return image

# ==========================================
# 🎬 2. 이커머스 매출최적화 GIF(움짤) 생성 엔진
# ==========================================
def create_marketing_gif(uploaded_files, badge_text):
    if not uploaded_files:
        return None
    frames = []
    for f in uploaded_files:
        try:
            f.seek(0)
            img = Image.open(f).convert("RGBA")
            img = img.resize((500, 500)) # 움짤용 최적 규격화
            
            # 오버레이 캔버스 생성 (반투명 마케팅 배지 레이어)
            overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            try:
                font_badge = ImageFont.truetype(FONT_PATH, 24)
            except:
                font_badge = ImageFont.load_default()
            
            # 하단 강력 셀링 배지 바 배치 (대박 상품들의 주요 특징)
            draw.rectangle([20, 430, 480, 480], fill=(255, 30, 84, 230)) # 쿠팡 경고형 레드배지
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            w = bbox[2] - bbox[0]
            draw.text(((500 - w) // 2, 442), badge_text, font=font_badge, fill=(255, 255, 255, 255))
            
            combined = Image.alpha_composite(img, overlay).convert("RGB")
            frames.append(combined)
        except:
            continue
            
    if frames:
        gif_buffer = io.BytesIO()
        # 1번 프레임을 필두로 나머지 사진 순차 연결 (0.4초 간격 무한 반복)
        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=400, loop=0)
        return gif_buffer.getvalue()
    return None


# ==========================================
# 🖥️ 3. 스트림릿 UI 시스템 빌드
# ==========================================
st.title("🎯 대박 상품 4종을 학습한 쿠팡형 AI 마스터 v20.0")
st.markdown("---")

if "step_results" not in st.session_state:
    st.session_state["step_results"] = None

# 📋 사이드바 마케팅 제어판
st.sidebar.header("📋 필수 정보 및 사진 등록")
api_key_input = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("상품명 (예: 다온 프리미엄 다용도 거치대)")
target_user = st.sidebar.text_input("타겟 고객 (예: 깔끔한 정리를 원하는 3040 주부)")

# 상품 이미지 다중 업로드 영역
uploaded_photos = st.sidebar.file_uploader("📂 [필수] 상품 실물 이미지 등록 (여러 장 가능)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_photos:
    st.sidebar.success(f"✅ 총 {len(uploaded_photos)}장의 상품 사진이 대기 중입니다.")

# 4대 억대매출 상품군 레이아웃 분석이 이식된 8단계 배치 매커니즘
STEPS = [
    ("1", "초강력 카오스 문제제기", "랄라 정리함/루시아이처럼 정리 안 된 집구석, 스톤힐처럼 목 디스크 걸릴 것 같은 모니터 환경의 극심한 비포 스트레스 자극"),
    ("2", "감정 과몰입 공감 유도", "무타공 선반 떨어져서 타일 깨진 경험 등 소비자가 돈 버리고 시간 날린 포인트 짚어주기"),
    ("3", "해결책 선언 및 스펙 등판", "모든 불만족을 한 번에 끝낼 최종 무기 등장. 가장 심플하고 견고한 실물 실루엣 오픈"),
    ("4", "압도적 기능 디테일 검증", "루시아이 슬라이딩처럼 부드러운 전개, 스톤힐처럼 뒤틀림 없는 하중 내구성의 핵심 스펙 수치화"),
    ("5", "싸구려 유사품과의 격차 폭로", "한 번 쓰고 부러지는 저가형 플라스틱/철판 제품과 두께 및 소재 단위의 투명한 스펙 비교 데이터 표 설계"),
    ("6", "실제 상황별 커스터마이징", "욕실, 주방, 거실, 팬트리 등 어디에 두어도 인테리어를 해치지 않는 실용적 배치 컷 연출"),
    ("7", "단독 패키지 혜택 제안", "지금 구매 시 한정 사은품 증정 및 무료 배송 콤보 구성으로 이탈 차단"),
    ("8", "마감 임박 및 리스크 제로", "품질 불만족 시 100% 환불 보장 제도 선언 및 당일 출고 수량 매진 임박 압박")
]

if st.button("🚀 4대 대박상품 패턴 적용 상세페이지 8장 추출 시작", type="primary"):
    if not api_key_input:
        st.error("🚨 왼쪽 사이드바에서 구글 API Key를 필수로 입력해 주세요.")
    elif not product_name:
        st.error("🚨 왼쪽 사이드바에서 상품명을 명확히 입력해 주세요.")
    else:
        api_key = api_key_input.strip()
        progress_bar = st.progress(0)
        loading_ui = st.empty()
        loading_ui.info("⚙️ 랄라/스톤힐/무타공선반/루시아이의 카피라이팅 배열 빅데이터를 기반으로 생성 중...")
        
        results = []
        
        for i, (num, title, core_concept) in enumerate(STEPS):
            step_full_title = f"{num}단계: {title}"
            
            # 상위 1% 벤치마킹 데이터 셋을 프롬프트 주입식 학습 데이터로 전환
            prompt = f"""
            당신은 대한민국 억대 매출 4대 주방/생활 수납 브랜드(랄라 정리함, 스톤힐 받침대, 무타공 욕실선반, 루시아이 팬트리)의 메인 마케팅 디렉터입니다.
            제시된 벤치마킹 상품들의 공통점인 [극적인 비포애프터, 단단한 내구성 강조, 움짤 유도형 기능 카피, 타사 깎아내리기 기법]을 조합해 [{step_full_title}]을 작성하세요.
            
            - 맥락 가이드: {core_concept}
            - 내 상품명: {product_name}
            - 명확한 타겟: {target_user if target_user else '생활 속 불편함을 해결하고픈 이커머스 유저'}

            [출력 규칙: 반드시 아래 대괄호 태그 구조로만 출력하세요]
            [MAIN] (소비자의 통증을 찌르거나 구매욕을 폭발시킬 한 줄 헤드라인 카피)
            [SUB] (움직이는 GIF 배지와 완벽히 연동되는 3줄 이내의 치명적인 설득 문구)
            [DESIGN] (가로 780px 기준 배치, 텍스트 가독성, 시선 이동 동선, 강조 그래픽 요소를 포함한 초정밀 디자이너 지시서)
            """
            
            raw_text = ""
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                res = requests.post(url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if res.status_code == 200:
                    raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
            except:
                pass
                
            if not raw_text:
                try:
                    url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    res = requests.post(url_v1, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                    if res.status_code == 200:
                        raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                except:
                    raw_text = "기획 데이터 추출 실패 가상 데이터로 대체합니다."

            main_c = f"아직도 무너지고 좁은 공간 때문에 스트레스 받으시나요? {product_name}"
            sub_c = "단 3초 만에 완벽하게 정돈되는 놀라운 변화를 눈앞에서 직접 확인해 보세요."
            guide_c = "상단에 붉은색 포인트 폰트로 불편 수치를 극대화하고 하단에 넓어진 수납 누끼 컷을 매칭합니다."
            
            if "[MAIN]" in raw_text and "[SUB]" in raw_text and "[DESIGN]" in raw_text:
                parts_main = raw_text.split("[MAIN]")[1].split("[SUB]")
                main_c = parts_main[0].strip()
                parts_sub = parts_main[1].split("[DESIGN]")
                sub_c = parts_sub[0].strip()
                guide_c = parts_sub[1].strip()

            results.append({
                "num": num,
                "title": title,
                "main": main_c,
                "sub": sub_c,
                "guide": guide_c
            })
            
            progress_bar.progress((i + 1) / len(STEPS))
            time.sleep(0.1)
            
        st.session_state["step_results"] = results
        loading_ui.empty()
        st.balloons()
        st.success("🎉 대박 상품들의 공통 레이아웃이 적용된 8단계 마스터 기획안이 생성되었습니다!")

# ==========================================
# 🖼️ 4. 출력 및 GIF 실시간 생성 보드 
# ==========================================
if st.session_state["step_results"]:
    st.markdown("---")
    st.header("🖼️ 쿠팡 표준 규격 이미지 & 고전환율 GIF 움짤 통합 제작 센터")
    st.info("💡 각 단계 우측에서 [🎬 마케팅 GIF 생성하기] 버튼을 누르면 업로드한 사진들로 즉시 역동적인 움짤 파일이 제작됩니다.")
    
    for i, item in enumerate(st.session_state["step_results"]):
        with st.container():
            st.markdown(f"### 📦 PAGE {item['num']} : {item['title']}")
            
            # 업로드 사진 순차 분배 분기점
            current_photo = None
            if uploaded_photos:
                current_photo = uploaded_photos[i % len(uploaded_photos)]
            
            # 이미지 연산 엔진 가동
            generated_img = create_coupang_image(
                step_num=item['num'], step_title=item['title'],
                main_copy=item['main'], sub_copy=item['sub'], guide_copy=item['guide'],
                uploaded_photo=current_photo
            )
            
            # 3단 파티션 레이아웃 (좌측: 쿠팡 등록용 사진, 중앙: 카피라이팅 데이터, 우측: GIF 메이커 장치)
            col_img, col_txt, col_gif = st.columns([1.1, 0.9, 1.0])
            
            with col_img:
                st.subheader("🖼️ 완성형 상세페이지 컷")
                st.image(generated_img, use_container_width=True)
                
                img_buffer = io.BytesIO()
                generated_img.save(img_buffer, format="PNG")
                byte_im = img_buffer.getvalue()
                
                st.download_button(
                    label=f"💾 PAGE {item['num']} 정적 이미지(PNG) 저장",
                    data=byte_im, file_name=f"coupang_layout_{item['num']}.png", mime="image/png",
                    use_container_width=True, key=f"dl_img_{item['num']}"
                )
                
            with col_txt:
                st.subheader("📋 실전 배치 카피라이팅")
                st.markdown(f"**📢 훅 메인 헤드라인:**\n{item['main']}")
                st.markdown(f"**✍️ 스토리 본문 문구:**\n{item['sub']}")
                st.markdown(f"**🎨 디자이너 그래픽 가이드:**\n{item['guide']}")
                
            with col_gif:
                st.subheader("🎬 움직이는 GIF(움짤) 메이커")
                
                # 대박 상품들의 소구 포인트를 반영한 한 줄 배지 텍스트 유저가 직접 수정 가능하도록 제공
                gif_badge_text = st.text_input(
                    "🔥 움짤 하단 강조 배지 문구 수정", 
                    value=f"★실제가동★ {item['main'][:12]}...", 
                    key=f"gif_text_in_{item['num']}"
                )
                
                if st.button(f"🎬 {item['num']}단계 맞춤형 움짤(GIF) 즉시 생성", key=f"make_gif_btn_{item['num']}", use_container_width=True):
                    if not uploaded_photos:
                        st.warning("⚠️ 왼쪽 사이드바에 먼저 상품 사진들을 업로드하셔야 움짤 변환이 가능합니다.")
                    else:
                        with st.spinner("🚀 고해상도 프레임 애니메이션 결합 중..."):
                            gif_bytes = create_marketing_gif(uploaded_photos, gif_badge_text)
                            if gif_bytes:
                                st.image(gif_bytes, caption="🔥 생성된 쿠팡형 마케팅 움짤 예시", use_container_width=True)
                                
                                st.download_button(
                                    label=f"💾 PAGE {item['num']} 움짤(GIF) 파일 저장하기",
                                    data=gif_bytes,
                                    file_name=f"coupang_moving_asset_{item['num']}.gif",
                                    mime="image/gif",
                                    use_container_width=True,
                                    key=f"dl_gif_btn_{item['num']}"
                                )
                            else:
                                st.error("🚨 GIF 파일 생성 중 원인 모를 오류 발생")
                                
            st.markdown("<br><hr style='border:1px solid #e9ecef;'><br>", unsafe_allow_html=True)
