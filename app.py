import asyncio
import os
import subprocess
import base64
import requests
from bs4 import BeautifulSoup
import streamlit as st
from playwright.async_api import async_playwright

# =================================================================
# [안전장치] 스트림릿 클라우드 전용 플레이라이트 브라우저 자동 설치
# =================================================================
@st.cache_resource
def install_playwright_browser():
    try:
        # 스트림릿 서버가 켜질 때 크롬(Chromium) 브라우저를 백그라운드에 자동 다운로드합니다.
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"브라우저 보조 엔진 설치 중 오류 발생: {e}")

# 앱 시작 시 브라우저 자동 설치 로직 실행
install_playwright_browser()


# =================================================================
# [세션 상태 초기화] 사용자가 입력한 데이터를 전역 보관
# =================================================================
if "sub_title" not in st.session_state:
    st.session_state["sub_title"] = "PREMIUM HOUSEHOLD SOLUTIONS"
if "main_title" not in st.session_state:
    st.session_state["main_title"] = "공간의 가치를 바꾸는 단 하나의 선택\n루시아이 스택 슬라이딩 팬트리 정리함"
if "product_image_url" not in st.session_state:
    st.session_state["product_image_url"] = "https://picsum.photos/720/450"
if "p2_title" not in st.session_state:
    st.session_state["p2_title"] = "아직도 좁은 주방 싱크대 아래,\n지저분하게 방치하고 계신가요?"
if "p2_desc" not in st.session_state:
    st.session_state["p2_desc"] = "적층이 불가능한 일반 바구니는 위쪽 공간을 모두 낭비하게 만듭니다."
if "p4_title" not in st.session_state:
    st.session_state["p4_title"] = "넣고 빼기 편리한 슬라이딩 레일 시스템"
if "p4_image_url" not in st.session_state:
    st.session_state["p4_image_url"] = "https://picsum.photos/720/600"


# =================================================================
# [기능 엔진] 인터넷 주소(URL) 크롤링 및 데이터화 로직
# =================================================================
def fetch_url_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            
            # 타이틀 정보 추출 (og:title 또는 기본 title)
            title = soup.find("meta", property="og:title")
            title_text = title["content"] if title else (soup.title.string if soup.title else "추출된 상품명 없음")
            
            # 설명 정보 추출 (og:description 또는 기본 description)
            desc = soup.find("meta", property="og:description")
            desc_text = desc["content"] if desc else "인터넷 주소 분석을 통해 자동으로 수집된 상세 데이터 기반 레이아웃입니다."
            
            return {"title": title_text.strip(), "desc": desc_text.strip()}
        else:
            return None
    except Exception as e:
        return None


# =================================================================
# [TEMPLATE] 선택된 데이터를 쿠팡 규격 HTML로 빌드
# =================================================================
def compile_to_html():
    main_title_br = st.session_state["main_title"].replace("\n", "<br>")
    p2_title_br = st.session_state["p2_title"].replace("\n", "<br>")
    
    html_content = f"""
    <div style="background-color: #ffffff; color: #111827;" class="py-12 px-8 text-center border-b border-gray-100">
        <p class="text-blue-600 font-bold text-sm tracking-widest uppercase mb-3">{st.session_state['sub_title']}</p>
        <h1 class="text-3xl font-black leading-tight tracking-tight mb-8">{main_title_br}</h1>
        <div class="mx-auto max-w-[720px] rounded-2xl overflow-hidden shadow-lg border border-gray-100">
            <img src="{st.session_state['product_image_url']}" class="w-full h-auto object-cover" alt="메인 상품 이미지">
        </div>
    </div>
    
    <div style="background-color: #f9fafb;" class="py-16 px-8 text-center border-b border-gray-100">
        <h2 class="text-2xl font-bold text-red-500 mb-4 leading-snug">{p2_title_br}</h2>
        <p class="text-gray-600 text-base max-w-[600px] mx-auto">{st.session_state['p2_desc']}</p>
    </div>
    
    <div style="background-color: #ffffff;" class="py-12 px-8 border-b border-gray-100">
        <h2 class="text-2xl font-bold text-gray-800 text-center mb-6">{st.session_state['p4_title']}</h2>
        <div class="rounded-2xl overflow-hidden shadow-xl border border-gray-200">
            <img src="{st.session_state['p4_image_url']}" class="w-full h-auto" alt="실물 연출 이미지">
        </div>
    </div>
    """
            
    full_html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
    </head>
    <body class="bg-gray-100 flex justify-center items-start min-h-screen m-0 p-0">
        <div id="coupang-canvas" class="w-[780px] bg-white shadow-md overflow-hidden">
            {html_content}
        </div>
    </body>
    </html>
    """
    return full_html


# =================================================================
# [RENDERER] TargetClosedError 방지 샌드박스 옵션이 추가된 렌더러
# =================================================================
async def render_image(html_str, output_path):
    async with async_playwright() as p:
        # 리눅스 클라우드 컨테이너 환경에서 크래시를 방지하는 3대 필수 옵션 추가
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        page = await browser.new_page()
        await page.set_viewport_size({"width": 780, "height": 3500})
        await page.set_content(html_str)
        
        # 네트워크 및 이미지 로딩 안전 대기
        await page.wait_for_timeout(3000) 
        
        element = await page.query_selector("#coupang-canvas")
        if element:
            await element.screenshot(path=output_path, type="png")
        await browser.close()


# =================================================================
# [Streamlit WEB UI] 메인 인터페이스
# =================================================================
def main():
    st.set_page_config(page_title="쿠팡형 AI 상세페이지 시스템 v2", layout="wide")
    
    st.title("📦 쿠팡 상세페이지 자동화 시스템 v2")
    st.subheader("마스터 저장소 데이터화 및 고화질 컴파일 허브")
    st.markdown("---")
    
    # 1.2.3.4 페이지 UI 구조를 탭(Tab) 시스템으로 직관적 유지
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 PAGE 1: 메인 설정 & 이미지 업로드", 
        "🔗 PAGE 2: 외부 링크 데이터화 센터", 
        "✏️ PAGE 3: 상세 레이아웃 편집", 
        "🖼️ PAGE 4: 고화질 렌더링 & 다운로드"
    ])
    
    # ---------------------------------------------------------
    # PAGE 1: 메인 설정 및 상품 이미지 직접 업로드
    # ---------------------------------------------------------
    with tab1:
        st.markdown("### 🗂️ PAGE 1 : 기획 헤드라인 및 상품 이미지 세팅")
        st.session_state["sub_title"] = st.text_input("상단 서브 타이틀 예시", st.session_state["sub_title"])
        st.session_state["main_title"] = st.text_area("메인 후킹 카피 문구 (줄바꿈 가능)", st.session_state["main_title"])
        
        st.markdown("#### 📸 메인 상품 실물 이미지 업로드")
        uploaded_file = st.file_uploader("여기에 내 상품의 썸네일이나 누끼 사진을 업로드하세요", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            # 업로드된 이미지를 베이스64 데이터 주소로 변환하여 실시간 브라우저 렌더링에 매칭
            bytes_data = uploaded_file.read()
            b64_encoded = base64.b64encode(bytes_data).decode()
            st.session_state["product_image_url"] = f"data:image/png;base64,{b64_encoded}"
            st.success("✅ 실물 상품 이미지가 바인딩되었습니다. 우측 프리뷰에서 확인하세요!")

    # ---------------------------------------------------------
    # PAGE 2: 인터넷 주소를 분석하여 기획전 데이터로 전환
    # ---------------------------------------------------------
    with tab2:
        st.markdown("### 🌐 PAGE 2 : 외부 상세페이지 링크 수집 데이터화 센터")
        st.write("경쟁사 스토어, 타사 몰 혹은 참고할 인터넷 주소를 넣으면 주요 키워드를 수집해 상세 기획에 자동 대입합니다.")
        
        target_url = st.text_input("데이터화 시킬 인터넷 주소(URL)를 입력하세요:", placeholder="https://example.com/products/123")
        
        if st.button("🔍 링크 주소 확인 및 상세페이지 데이터화 실행"):
            if target_url:
                with st.spinner("해당 인터넷 주소에서 핵심 기획 구조 분석 및 텍스트 데이터 추출 중..."):
                    scraped_data = fetch_url_data(target_url)
                    
                    if scraped_data:
                        st.success("🎉 외부 링크 정보 수집에 성공하여 기획 문구를 갱신했습니다!")
                        # 데이터 파싱 후 세션 상태에 강제 주입
                        st.session_state["main_title"] = f"[링크분석상품]\n{scraped_data['title']}"
                        st.session_state["p2_desc"] = scraped_data["desc"]
                        
                        st.info(f"**🤖 추출된 핵심 상품 타이틀:** {scraped_data['title']}")
                        st.info(f"**📝 추출된 기획 디스크립션:** {scraped_data['desc']}")
                    else:
                        st.warning("⚠️ 주소는 올바르나 사이트 보안정책으로 인해 텍스트 데이터 추출을 거부당했습니다. 기본 템플릿 정보를 유지합니다.")
            else:
                st.error("❌ 주소를 입력한 뒤 버튼을 눌러주세요.")

    # ---------------------------------------------------------
    # PAGE 3: 중단 상세 레이아웃 편집기
    # ---------------------------------------------------------
    with tab3:
        st.markdown("### ✏️ PAGE 3 : 상세 컴포넌트 세부 텍스트 편집기")
        st.session_state["p2_title"] = st.text_area("2페이지 문제제기 메인 타이틀", st.session_state["p2_title"])
        st.session_state["p2_desc"] = st.text_area("2페이지 설명 서브 카피", st.session_state["p2_desc"])
        st.markdown("---")
        st.session_state["p4_title"] = st.text_input("4페이지 실물 연출 정보 타이틀", st.session_state["p4_title"])

    # ---------------------------------------------------------
    # PAGE 4: 고화질 통이미지 굽기 및 다운로드 센터 (출력 화면 분할 복원)
    # ---------------------------------------------------------
    with tab4:
        st.markdown("### 🖼️ PAGE 4 : 쿠팡 규격(가로 780px) 통이미지 빌드 및 다운로드")
        
        col_ctrl, col_view = st.columns([1, 1.2])
        
        with col_ctrl:
            st.markdown("#### ⚡ 컴파일 컨트롤러")
            st.write("설정된 모든 1~4페이지 기획 카드를 한 장의 고화질 쿠팡 전용 세로 통이미지로 인쇄합니다.")
            
            output_filename = "coupang_master_result.png"
            
            # [버튼] 샌드박스가 우회된 마스터 이미지 빌드
            if st.button("🔥 완성형 상세페이지 그룹화 및 마스터 이미지 빌드"):
                with st.spinner("서버 내 독립 브라우저 컨테이너 개설 및 픽셀 렌더링 중 (약 3초)..."):
                    current_compiled_html = compile_to_html()
                    asyncio.run(render_image(current_compiled_html, output_filename))
                    
                if os.path.exists(output_filename):
                    st.success("🚀 TargetClosedError 우회 및 통상세페이지 빌드에 성공했습니다!")
                    
                    with open(output_filename, "rb") as file:
                        st.download_button(
                            label="💾 고화질 실물 통이미지 다운로드 (.png)",
                            data=file,
                            file_name=output_filename,
                            mime="image/png"
                        )
                else:
                    st.error("❌ 이미지 파일 인쇄 프로세스 도중 낙뢰 에러가 발생했습니다.")
                    
        with col_view:
            st.markdown("#### 🔮 쿠팡 가로 780px 실시간 마스터 프리뷰")
            st.caption("기획안 데이터가 변경되면 실시간으로 동적 컴포넌트 마운트가 일어납니다.")
            
            # 실시간으로 조립된 HTML을 웹 화면 우측에 고정 780px 너비 스타일로 미리보기 제공
            import streamlit.components.v1 as components
            live_html = compile_to_html()
            components.html(live_html, height=800, scrolling=True)

if __name__ == "__main__":
    main()
