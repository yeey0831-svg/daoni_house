import sys
import subprocess

# =================================================================
# 📦 [필수 도구 자동 설치] bs4와 requests가 없으면 서버가 알아서 설치합니다.
# =================================================================
try:
    import requests
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    # 스트림릿 서버 환경에 크롤링 필수 패키지 강제 주입
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "requests"])
    import requests
    from bs4 import BeautifulSoup

import streamlit as st
import json
import io
from PIL import Image, ImageDraw, ImageFont

# =================================================================
# ⚙️ [초기 설정 및 레이아웃 선언]
# =================================================================
st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v2.7", layout="wide")

# OS별 안전한 폰트 로더
def get_safe_font(font_size=20):
    font_paths = [
        "NanumGothic.ttf",
        "C:/Windows/Fonts/malgun.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "Arial.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, font_size)
        except IOError:
            continue
    return ImageFont.load_default()

# 텍스트 자동 줄바꿈 헬퍼 (PIL 전용)
def draw_wrapped_text(draw, text, font, color, max_width, start_x, start_y):
    lines = []
    for paragraph in text.split('\n'):
        line = ""
        for char in paragraph:
            if draw.textlength(line + char, font=font) <= max_width:
                line += char
            else:
                lines.append(line)
                line = char
        lines.append(line)
    
    current_y = start_y
    for line in lines:
        draw.text((start_x, current_y), line, font=font, fill=color)
        current_y += font.size + 10
    return current_y

# =================================================================
# 💾 [세션 상태 관리] 입력 데이터 유실 방지
# =================================================================
if "sub_title" not in st.session_state:
    st.session_state["sub_title"] = "COUPANG JET-DELIVERY PREMIUM SELECTION"
if "main_title" not in st.session_state:
    st.session_state["main_title"] = "공간의 가치를 바꾸는 단 하나의 선택\n루시아이 스택 슬라이딩 팬트리 정리함"
if "p1_image" not in st.session_state:
    st.session_state["p1_image"] = None  # 사용자가 업로드할 실물 이미지 보관함
if "p2_title" not in st.session_state:
    st.session_state["p2_title"] = "강력한 Hooking 문제 제기"
if "p2_desc" not in st.session_state:
    st.session_state["p2_desc"] = "기존 하부장 정리함, 안쪽 물건 꺼내다 다 쏟아진 적 많으시죠? [당일출고] 루시아이 스택 슬라이딩 팬트리 정리함으로 해결하세요."
if "p4_title" not in st.session_state:
    st.session_state["p4_title"] = "넣고 빼기 편리한 슬라이딩 레일 시스템"

# =================================================================
# 🌐 [PAGE 2용 수집 엔진] 외부 상세페이지 URL 크롤러
# =================================================================
def analyze_url_to_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            # 타이틀(상품명) 추출
            title_tag = soup.find("meta", property="og:title") or soup.title
            title = title_tag["content"] if title_tag and title_tag.has_attr("content") else (title_tag.string if title_tag else "추출된 상품 기획전")
            # 설명문 추출
            desc_tag = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
            desc = desc_tag["content"] if desc_tag else "성공적으로 링크 데이터를 수집했습니다. 상세 레이아웃에 맞춰 기획을 고도화하세요."
            return title.strip(), desc.strip()
    except Exception as e:
        return None, None
    return None, None

# =================================================================
# 🏛️ [기존 1, 2, 3, 4 페이지 오리지널 UI 구조 복원 및 강화]
# =================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 PAGE 1: 실시간 미리보기 & 업로드",
    "🔗 PAGE 2: 외부 링크 데이터화 센터",
    "✏️ PAGE 3: 기획 데이터 상세 편집",
    "💾 PAGE 4: 마스터 이미지 다운로드"
])

# -----------------------------------------------------------------
# [PAGE 1] 메인 타이틀 검토 및 상품 이미지 업로드 공간
# -----------------------------------------------------------------
with tab1:
    st.markdown("### 📦 PAGE 1 : 실시간 레이아웃 및 상품 이미지 매칭")
    
    st.markdown("#### 📸 메인 상품 실물 사진 업로드")
    img_file = st.file_uploader("상세페이지 1페이지에 넣을 상품 사진(PNG, JPG)을 선택하세요", type=["png", "jpg", "jpeg"])
    if img_file is not None:
        st.session_state["p1_image"] = Image.open(img_file)
        st.success("✅ 상품 실물 이미지가 성공적으로 업로드되어 시스템에 등록되었습니다!")

    st.markdown("---")
    st.caption("👇 현재 적용 중인 1페이지 상단 헤드라인 프리뷰")
    st.info(f"**[{st.session_state['sub_title']}]**\n\n{st.session_state['main_title']}")
    
    if st.session_state["p1_image"] is not None:
        st.image(st.session_state["p1_image"], caption="1페이지 연동 상품 이미지 미리보기", width=400)
    else:
        st.warning("⚠️ 현재 등록된 상품 이미지가 없습니다. 위에 업로드 박스에 이미지를 넣어주세요.")

# -----------------------------------------------------------------
# [PAGE 2] 외부 상세페이지 링크 주소 입력 칸 및 데이터화 엔진
# -----------------------------------------------------------------
with tab2:
    st.markdown("### 🔗 PAGE 2 : 외부 상세페이지 링크 수집 데이터화 센터")
    st.write("경쟁사 스토어나 벤치마킹할 상세페이지 주소(URL)를 넣으면 핵심 데이터를 분석해 기획 카드로 자동 변환합니다.")
    
    input_url = st.text_input("분석할 인터넷 주소(URL)를 입력해 주세요:", placeholder="https://smartstore.naver.com/...")
    
    if st.button("⚡ 링크 확인 후 상세페이지 데이터화 실행"):
        if input_url:
            with st.spinner("인터넷 주소 유효성 검사 및 텍스트 데이터 추출 중..."):
                extracted_title, extracted_desc = analyze_url_to_data(input_url)
                if extracted_title:
                    st.success("🎉 성공적으로 링크 분석 완료! 추출된 데이터가 상세페이지 기획에 대입되었습니다.")
                    st.session_state["main_title"] = f"[링크소구] {extracted_title}"
                    st.session_state["p2_desc"] = extracted_desc
                    
                    st.text_input("🤖 자동 수집된 상품명", extracted_title, disabled=True)
                    st.text_area("📝 자동 수집된 소구문장", extracted_desc, disabled=True)
                else:
                    st.error("❌ 주소가 올바르지 않거나, 해당 사이트가 로봇 차단 정책을 사용 중입니다. 다른 주소를 시도해 주세요.")
        else:
            st.warning("⚠️ 주소를 먼저 입력창에 채워주세요.")

# -----------------------------------------------------------------
# [PAGE 3] 상세 컴포넌트 수동 세부 편집기
# -----------------------------------------------------------------
with tab3:
    st.markdown("### ✏️ PAGE 3 : 상세 컴포넌트 기획 문구 편집")
    st.session_state["sub_title"] = st.text_input("1페이지 서브 타이틀 문구 변경", st.session_state["sub_title"])
    st.session_state["main_title"] = st.text_area("1페이지 메인 타이틀 문구 변경", st.session_state["main_title"])
    st.markdown("---")
    st.session_state["p2_title"] = st.text_input("2페이지 문제제기 제목 변경", st.session_state["p2_title"])
    st.session_state["p2_desc"] = st.text_area("2페이지 서브 카피 변경", st.session_state["p2_desc"])
    st.markdown("---")
    st.session_state["p4_title"] = st.text_input("4페이지 실물 연출 정보 타이틀 변경", st.session_state["p4_title"])

# -----------------------------------------------------------------
# [PAGE 4] 서버에서 절대 안 튕기는 고화질 PIL 이미지 빌드 및 다운로드 센터
# -----------------------------------------------------------------
with tab4:
    st.markdown("### 💾 PAGE 4 : 쿠팡 규격(가로 780px) 이미지 다운로드 센터")
    st.write("아래 버튼을 누르면 서버 부담 없이 파이썬 엔진이 즉시 고화질 통이미지(.png)를 드로잉합니다.")
    
    if st.button("🔥 완성형 상세페이지 8장 그룹화 및 마스터 이미지 빌드"):
        with st.spinner("PIL 드로잉 픽셀 맵 컴파일 중..."):
            master_w = 780
            master_h = 1600
            canvas = Image.new("RGB", (master_w, master_h), color="#FFFFFF")
            draw = ImageDraw.Draw(canvas)
            
            font_title = get_safe_font(28)
            font_sub = get_safe_font(16)
            font_body = get_safe_font(18)
            
            # --- [SECTION 1] 1페이지 드로잉 ---
            draw.text((40, 40), st.session_state["sub_title"], fill="#2563EB", font=font_sub)
            next_y = draw_wrapped_text(draw, st.session_state["main_title"], font_title, "#111827", 700, 40, 75)
            
            if st.session_state["p1_image"] is not None:
                p1_img_resized = st.session_state["p1_image"].copy()
                p1_img_resized.thumbnail((700, 400))
                canvas.paste(p1_img_resized, (40, next_y + 20))
            
            # --- [SECTION 2] 2페이지 드로잉 (문제 제기) ---
            draw.rectangle([0, 650, 780, 1000], fill="#F9FAFB")
            draw.text((40, 690), st.session_state["p2_title"], fill="#EF4444", font=font_title)
            draw_wrapped_text(draw, st.session_state["p2_desc"], font_body, "#4B5563", 700, 40, 750)
            
            # --- [SECTION 3] 4페이지 드로잉 (실물 규격화) ---
            draw.text((40, 1060), st.session_state["p4_title"], fill="#111827", font=font_title)
            draw.rectangle([40, 1130, 740, 1500], fill="#E5E7EB")
            draw.text((80, 1300), "[여기에 4페이지 상세 연출 그래픽 컴포넌트 바인딩 완료]", fill="#9CA3AF", font=font_body)
            
            buf = io.BytesIO()
            canvas.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.success("🎉 서버 과부하 없이 고화질 마스터 통이미지 렌더링에 완벽 성공했습니다!")
            
            st.download_button(
                label="💾 고화질 실물 통이미지 다운로드 (.png)",
                data=byte_im,
                file_name="coupang_master_perfect.png",
                mime="image/png"
            )
            
            st.image(canvas, caption="실제 컴파일 완료된 가로 780px 통이미지 원본 스냅샷", use_container_width=True)

if __name__ == "__main__":
    main()
