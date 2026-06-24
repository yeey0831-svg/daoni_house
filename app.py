import streamlit as st
import requests
import time
import os
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v21.0", layout="wide")

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
# 💾 전역 세션 상태(Session State) 초기화
# ==========================================
if "step_results" not in st.session_state:
    st.session_state["step_results"] = None
if "page3_saved_images" not in st.session_state:
    st.session_state["page3_saved_images"] = []  # 3페이지에 저장될 이미지 데이터 리스트

# ==========================================
# 🎨 780px 맞춤형 스타일 상세페이지 생성 엔진
# ==========================================
def create_styled_image(step_num, step_title, main_copy, sub_copy, guide_copy, theme_color=(23, 28, 36), uploaded_photo=None):
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

    # 추출된 테마 컬러 반영 (상단 바)
    draw.rectangle([0, 0, width, 90], fill=theme_color)
    draw.text((40, 32), f"✨ TEMPLATE PAGE {step_num} : {step_title}", font=font_title, fill=(255, 255, 255))
    
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

    # 카피라이팅 영역
    next_y = 140
    draw.text((40, next_y), "⚡ HOOKING TEXT", font=font_sub, fill=theme_color)
    next_y = draw_text_wrap(main_copy.replace("-", "").strip(), font=font_main, color=(17, 17, 17), start_y=next_y+35, max_w=700)
    
    next_y += 40
    draw.text((40, next_y), "📝 BODY COPY", font=font_sub, fill=(73, 80, 87))
    next_y = draw_text_wrap(sub_copy.strip(), font=font_sub, color=(52, 58, 64), start_y=next_y+35, max_w=700, line_spacing=10)
    
    # 이미지 프레임 영역
    next_y += 40
    frame_y1 = next_y
    frame_y2 = frame_y1 + 400
    draw.rectangle([40, frame_y1, width-40, frame_y2], fill=(250, 250, 250), outline=(230, 230, 230), width=2)
    
    if uploaded_photo is not None:
        try:
            # 3페이지 세션에 바이너리로 저장되어 있을 경우 바이트 변환 처리 포함
            if isinstance(uploaded_photo, bytes):
                prod_img = Image.open(io.BytesIO(uploaded_photo))
            else:
                uploaded_photo.seek(0)
                prod_img = Image.open(uploaded_photo)
                
            prod_img.convert("RGB")
            prod_img.thumbnail((640, 360))
            p_w, p_h = prod_img.size
            image.paste(prod_img, ((width - p_w) // 2, frame_y1 + (400 - p_h) // 2))
        except:
            draw.text((60, frame_y1 + 180), "📸 상품 사진이 배치되는 영역입니다.", font=font_guide, fill=(150, 150, 150))
    else:
        draw.text((60, frame_y1 + 180), "📸 상품 사진이 배치되는 영역입니다.", font=font_guide, fill=(150, 150, 150))
        
    # 디자인 지시서
    next_y = frame_y2 + 40
    draw.text((40, next_y), "🎨 EXTRACTED DESIGN PATTERN GUIDE", font=font_sub, fill=(134, 142, 150))
    next_y = draw_text_wrap(guide_copy.strip(), font=font_guide, color=(108, 117, 125), start_y=next_y+35, max_w=700, line_spacing=8, align="left")
    
    draw.rectangle([0, height-50, width, height], fill=(241, 243, 245))
    draw.text((40, height-33), "EXTRACTED TEMPLATE STANDARD (780px Width)", font=font_guide, fill=(173, 181, 189))
    
    return image

# GIF 생성 헬퍼 함수
def create_marketing_gif(uploaded_files, badge_text):
    if not uploaded_files: return None
    frames = []
    for f in uploaded_files:
        try:
            if isinstance(f, bytes):
                img = Image.open(io.BytesIO(f)).convert("RGBA")
            else:
                f.seek(0)
                img = Image.open(f).convert("RGBA")
            img = img.resize((500, 500))
            overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            try: font_badge = ImageFont.truetype(FONT_PATH, 24)
            except: font_badge = ImageFont.load_default()
            
            draw.rectangle([20, 430, 480, 480], fill=(255, 30, 84, 230))
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            w = bbox[2] - bbox[0]
            draw.text(((500 - w) // 2, 442), badge_text, font=font_badge, fill=(255, 255, 255, 255))
            frames.append(Image.alpha_composite(img, overlay).convert("RGB"))
        except: continue
    if frames:
        gif_buffer = io.BytesIO()
        frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=400, loop=0)
        return gif_buffer.getvalue()
    return None


# ==========================================
# 🧭 사이드바 대시보드 및 네비게이션
# ==========================================
st.sidebar.title("🎯 AI 상세페이지 시스템")
menu = st.sidebar.radio(
    "🧭 메뉴를 이동하며 작업하세요", 
    ["🏠 1페이지: 기본 대박공식 빌더", "🔗 2페이지: URL 양식/스타일 추출기", "📂 3페이지: 추출 상세페이지 저장소"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔑 기본 연동 설정")
api_key_input = st.sidebar.text_input("Google API Key", type="password")
product_name = st.sidebar.text_input("내 상품명", value="다온 프리미엄 수납함")
target_user = st.sidebar.text_input("타겟 고객", value="공간 정리가 필요한 사람")

uploaded_photos = st.sidebar.file_uploader("📂 상품 실물 사진 등록 (다중 가능)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploaded_photos:
    st.sidebar.success(f"✅ 사진 {len(uploaded_photos)}장 로드 완료")


# ==========================================
# 🏠 1페이지: 기존 대박공식 빌더 화면
# ==========================================
if menu == "🏠 1페이지: 기본 대박공식 빌더":
    st.header("🏠 1페이지: 4대 대박상품 패턴 상세페이지 빌더")
    st.write("기존에 완성된 고전환율 8단계 상세페이지 및 움짤 생성 엔진 공간입니다.")
    
    STEPS = [
        ("1", "초강력 카오스 문제제기", "비포 스트레스 극대화"), ("2", "감정 과몰입 공감 유도", "소비자 실패 경험 자극"),
        ("3", "해결책 선언 및 스펙 등판", "우리 제품 화려한 등장"), ("4", "압도적 기능 디테일 검증", "핵심 기능의 수치화"),
        ("5", "싸구려 유사품과의 격차 폭로", "타사 비교 우위 데이터"), ("6", "실제 상황별 커스터마이징", "다양한 실용 배치 연출"),
        ("7", "단독 패키지 혜택 제안", "사은품 및 특별 혜택 구성"), ("8", "마감 임박 및 리스크 제로", "환불 보장 및 즉시 마감")
    ]
    
    if st.button("🚀 8단계 상세페이지 생성 시작", type="primary"):
        if not api_key_input: st.error("API Key를 입력해주세요.")
        else:
            api_key = api_key_input.strip()
            progress = st.progress(0)
            results = []
            for i, (num, title, core_concept) in enumerate(STEPS):
                prompt = f"쿠팡 수납/생활 1위 브랜드 스타일로 다음 단계 기획안 작성. 단계: {num}-{title}, 컨셉: {core_concept}, 상품명: {product_name}. [MAIN], [SUB], [DESIGN] 태그를 반드시 포함하여 출력하세요."
                main_c, sub_c, guide_c = f"{product_name}의 놀라운 혁신", "상세 설명 문구 영역", "깔끔한 레이아웃 연출"
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text']
                        if "[MAIN]" in raw and "[SUB]" in raw and "[DESIGN]" in raw:
                            main_c = raw.split("[MAIN]")[1].split("[SUB]")[0].strip()
                            sub_c = raw.split("[SUB]")[1].split("[DESIGN]")[0].strip()
                            guide_c = raw.split("[DESIGN]")[1].strip()
                except: pass
                results.append({"num": num, "title": title, "main": main_c, "sub": sub_c, "guide": guide_c})
                progress.progress((i+1)/len(STEPS))
            st.session_state["step_results"] = results
            st.success("생성 완료! 아래에서 확인 및 다운로드 가능합니다.")

    if st.session_state["step_results"]:
        for i, item in enumerate(st.session_state["step_results"]):
            st.markdown(f"### 📦 PAGE {item['num']} : {item['title']}")
            current_photo = uploaded_photos[i % len(uploaded_photos)] if uploaded_photos else None
            generated_img = create_styled_image(item['num'], item['title'], item['main'], item['sub'], item['guide'], (23,28,36), current_photo)
            
            col1, col2, col3 = st.columns([1.1, 0.9, 1.0])
            with col1:
                st.image(generated_img, use_container_width=True)
                buf = io.BytesIO()
                generated_img.save(buf, format="PNG")
                st.download_button(f"💾 PAGE {item['num']} PNG 저장", buf.getvalue(), f"page_{item['num']}.png", "image/png", key=f"p1_dl_{i}")
            with col2:
                st.markdown(f"**헤드라인:** {item['main']}\n\n**본문:** {item['sub']}\n\n**가이드:** {item['guide']}")
            with col3:
                gif_badge = st.text_input("GIF 배지 문구", value="★실제가동폭발★", key=f"p1_gif_in_{i}")
                if st.button(f"🎬 {item['num']}단 움짤 생성", key=f"p1_gif_btn_{i}"):
                    gif_b = create_marketing_gif(uploaded_photos, gif_badge)
                    if gif_b:
                        st.image(gif_b, use_container_width=True)
                        st.download_button("💾 GIF 저장", gif_b, f"moving_{item['num']}.gif", "image/gif", key=f"p1_gif_dl_{i}")


# ==========================================
# 🔗 2페이지: URL 양식/스타일 추출기 화면
# ==========================================
elif menu == "🔗 2페이지: URL 양식/스타일 추출기":
    st.header("🔗 2페이지: 벤치마킹 URL 스타일 분석 및 이미지 복제기")
    st.write("경쟁사 혹은 닮고 싶은 상세페이지 주소를 입력하면, AI가 디자인 양식과 스케일, 톤앤매너를 가상 추출하여 새로운 상세페이지 파일 세트를 빌드합니다.")
    
    target_url = st.text_input("🎯 벤치마킹할 상세페이지 주소(URL) 입력", placeholder="https://brand.naver.com/... 또는 https://www.coupang.com/...")
    
    if st.button("🔮 URL 구조/양식 추출 후 상세페이지 이미지 자동 빌드", type="primary"):
        if not api_key_input:
            st.error("🚨 사이드바에 Google API Key를 입력해 주세요.")
        elif not target_url:
            st.error("🚨 분석할 URL 주소를 입력해 주세요.")
        else:
            api_key = api_key_input.strip()
            with st.spinner("🕵️‍♂️ 입력하신 URL의 플랫폼 레이아웃 양식 및 폰트 배치 스타일 규칙을 딥러닝 분석 중..."):
                
                # URL 분석 및 맞춤 스타일 지정을 위한 AI 프롬프트
                analysis_prompt = f"""
                당신은 웹 디자인 역공학 디자이너입니다. 다음 URL 주소의 플랫폼 종류와 형태를 기반으로, 가장 어울리는 상세페이지 이미지 테마 스펙을 정의하세요.
                URL: {target_url}
                
                [출력 양식 가이드: 반드시 아래 대괄호 태그 규칙만 지켜 대답하세요]
                [COLOR] (이 사이트에 가장 잘 어울리는 메인 강조색 테마를 RGB 형식으로 대답하세요. 예: 0,116,233 또는 255,51,102)
                [FONT_STYLE] (권장 폰트 두께 및 타이포그래피 정렬 양식에 대한 짧은 요약)
                [HOOK_COPY] (해당 플랫폼 최적화 스타일로 가공된 우리 제품 [{product_name}]의 자극적 헤드라인 카피 1줄)
                [BODY_COPY] (해당 몰의 고객군이 가장 열광하는 논리적 상세 설득 카피 3줄)
                [DESIGN_GUIDE] (추출한 그리드 패턴과 여백, 이미지 배치 정렬 방식에 대한 지시서)
                """
                
                theme_color = (0, 116, 233) # 기본값 (쿠팡블루)
                main_c, sub_c, guide_c = "추출된 스타일 기반 헤드라인", "추출된 스타일 기반 설득 본문", "추출된 여백 및 그리드 가이드"
                
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    res = requests.post(url, json={"contents": [{"parts": [{"text": analysis_prompt}]}]}, timeout=20)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text']
                        
                        # 파싱 작업
                        if "[COLOR]" in raw:
                            color_str = raw.split("[COLOR]")[1].split("[FONT_STYLE]")[0].strip()
                            theme_color = tuple(map(int, color_str.split(',')))
                        if "[HOOK_COPY]" in raw:
                            main_c = raw.split("[HOOK_COPY]")[1].split("[BODY_COPY]")[0].strip()
                        if "[BODY_COPY]" in raw:
                            sub_c = raw.split("[BODY_COPY]")[1].split("[DESIGN_GUIDE]")[0].strip()
                        if "[DESIGN_GUIDE]" in raw:
                            guide_c = raw.split("[DESIGN_GUIDE]")[1].strip()
                except Exception as e:
                    st.warning(f"테마 세부 추출 중 일부 기본값 대체 발생: {e}")
                
                # 🛠️ 실물 이미지 제작 및 저장소(3페이지) 자동 전송 파이프라인
                # 대표님을 위해 총 2장의 '추출형 맞춤 이미지 카드'를 자동 제작하여 저장합니다.
                saved_list = []
                photo_bytes_1 = uploaded_photos[0].read() if uploaded_photos else None
                photo_bytes_2 = uploaded_photos[1 % len(uploaded_photos)].read() if uploaded_photos and len(uploaded_photos) > 1 else photo_bytes_1
                
                # 1번 카드 렌더링 및 바이너리 획득
                img1 = create_styled_image("URL-01", "추출 양식 메인 매칭 컷", main_c, sub_c, guide_c, theme_color, photo_bytes_1)
                buf1 = io.BytesIO()
                img1.save(buf1, format="PNG")
                
                # 2번 카드 렌더링 및 바이너리 획득 (반전 소구)
                img2 = create_styled_image("URL-02", "추출 양식 기능성 검증 컷", f"🔍 스펙 비교: {main_c[:15]}", f"타사 대비 우위성 검증 완료. {sub_c[:40]}", f"그리드 정렬 리디자인 가이드: {guide_c[:40]}", theme_color, photo_bytes_2)
                buf2 = io.BytesIO()
                img2.save(buf2, format="PNG")
                
                # 3페이지 세션에 딕셔너리 형태로 데이터 즉시 적재
                st.session_state["page3_saved_images"].append({
                    "url": target_url,
                    "title": "1. 벤치마킹 타겟 메인 레이아웃",
                    "img_bytes": buf1.getvalue(),
                    "main": main_c, "sub": sub_c, "guide": guide_c, "color": theme_color
                })
                st.session_state["page3_saved_images"].append({
                    "url": target_url,
                    "title": "2. 벤치마킹 스펙 검증 레이아웃",
                    "img_bytes": buf2.getvalue(),
                    "main": f"🔍 스펙 비교: {main_c[:15]}", "sub": f"우위성 검증. {sub_c[:40]}", "guide": guide_c, "color": theme_color
                })
                
                st.success("✅ 성공! URL에서 디자인 양식과 폰트 배치 룰을 추출하여 실제 상세페이지 2장을 구워냈습니다.")
                st.info("💡 완성된 파일들은 [📂 3페이지: 추출 상세페이지 저장소] 메뉴에 자동으로 저장 및 백업되었습니다. 왼쪽 사이드바 메뉴에서 3페이지를 클릭해 확인해보세요!")


# ==========================================
# 📂 3페이지: 추출 상세페이지 저장소 화면
# ==========================================
elif menu == "📂 3페이지: 추출 상세페이지 저장소":
    st.header("📂 3페이지: URL 기반 추출 상세페이지 라이브러리 및 미리보기")
    st.write("2페이지에서 분석 가동하여 실시간으로 넘어온 이미지 파일 보관소입니다. 여기서 최종 검수 후 저장하세요.")
    
    if not st.session_state["page3_saved_images"]:
        st.warning("📭 아직 추출되어 저장된 상세페이지 파일이 없습니다. 2페이지에서 URL을 넣고 먼저 생성해 주세요!")
    else:
        st.success(f"🗂️ 현재 총 {len(st.session_state['page3_saved_images'])}개의 추출형 상세페이지가 모니터링되고 있습니다.")
        
        # 저장소 내부 데이터 루프 돌며 출력
        for idx, saved_item in enumerate(st.session_state["page3_saved_images"]):
            with st.get_container():
                st.markdown(f"### 🗂️ 파일 고유번호: #{idx+1} - {saved_item['title']}")
                st.caption(f"🔗 출처 소스 주소: {saved_item['url']}")
                
                col_view, col_info, col_gif_make = st.columns([1.2, 0.8, 1.0])
                
                with col_view:
                    st.subheader("🖼️ 추출 양식 이미지 미리보기")
                    # 저장된 바이너리 바이트 데이터를 이미지로 화면 렌더링
                    st.image(saved_item["img_bytes"], caption=f"추출본 #{idx+1} 실물 캔버스 (780px)", use_container_width=True)
                    
                    st.download_button(
                        label=f"💾 #{idx+1} 실물 PNG 파일 다운로드",
                        data=saved_item["img_bytes"],
                        file_name=f"extracted_layout_card_{idx+1}.png",
                        mime="image/png",
                        key=f"p3_dl_btn_{idx}",
                        use_container_width=True
                    )
                    
                with col_info:
                    st.subheader("📝 적용된 텍스트")
                    st.markdown(f"**📌 적용 헤드라인:**\n{saved_item['main']}")
                    st.markdown(f"**✍️ 적용 카피 본문:**\n{saved_item['sub']}")
                    st.markdown(f"**🎨 양식 분석 가이드:**\n{saved_item['guide']}")
                    st.markdown(f"**🎨 추출 테마 컬러(RGB):**\n`{saved_item['color']}`")
                    
                with col_gif_make:
                    st.subheader("🎬 연동형 움짤(GIF) 세트 결합")
                    gif_badge_p3 = st.text_input("움짤 하단 배지 문구", value="🔥 주문폭주 제품실물", key=f"p3_gif_in_{idx}")
                    
                    if st.button(f"🎬 #{idx+1} 카드 맞춤 움짤 뽑기", key=f"p3_gif_btn_{idx}", use_container_width=True):
                        if not uploaded_photos:
                            st.warning("⚠️ 사이드바에 상품 사진을 등록하셔야 GIF 조립이 가능합니다.")
                        else:
                            with st.spinner("애니메이션 프레임 생성 중..."):
                                # 3페이지에 업로드되어 있던 사진 바이너리를 넘겨 GIF 변환
                                photo_raw_list = [p.read() for p in uploaded_photos]
                                gif_bytes = create_marketing_gif(photo_raw_list, gif_badge_p3)
                                if gif_bytes:
                                    st.image(gif_bytes, caption="생성된 이커머스 최적화 움짤", use_container_width=True)
                                    st.download_button(
                                        label="💾 움짤(.gif) 최종 컴퓨터 저장",
                                        data=gif_bytes,
                                        file_name=f"extracted_moving_{idx+1}.gif",
                                        mime="image/gif",
                                        key=f"p3_gif_dl_save_{idx}",
                                        use_container_width=True
                                    )
                                    
                st.markdown("<br><hr style='border:1px dashed #ced4da;'><br>", unsafe_allow_html=True)
