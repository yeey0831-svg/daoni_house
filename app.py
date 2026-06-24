import asyncio
import os
import subprocess
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
# [3번째 요구사항] 마스터 저장소 시스템 (Master Repository DB 시뮬레이션)
# =================================================================
MASTER_REPOSITORY = {
    "template_premium_01": {
        "title": "루시아이 슬라이딩 정리함 프리미엄형",
        "description": "강력한 후킹 문구, 1페이지 이미지 연동 및 4페이지 실물 크롭 컷이 포함된 완벽형 템플릿",
        "blocks": [
            {
                "type": "p1_hooking",  # [1번째 요구사항] 1페이지 이미지 추가 공간 반영
                "sub_title": "PREMIUM HOUSEHOLD SOLUTIONS",
                "main_title": "공간의 가치를 바꾸는 단 하나의 선택\n루시아이 스택 슬라이딩 팬트리 정리함",
                "product_image": "https://picsum.photos/720/450", 
                "bg_color": "#ffffff",
                "text_color": "#111827"
            },
            {
                "type": "p2_problem",
                "title": "아직도 좁은 주방 싱크대 아래,\n지저분하게 방치하고 계신가요?",
                "desc": "적층이 불가능한 일반 바구니는 위쪽 공간을 모두 낭비하게 만듭니다.",
                "bg_color": "#f9fafb"
            },
            {
                "type": "p4_real_image", # [2번째 요구사항] 4페이지 실물 이미지화 영역
                "section_title": "넣고 빼기 편리한 슬라이딩 레일 시스템",
                "detail_image": "https://picsum.photos/720/600", 
                "bg_color": "#ffffff"
            }
        ]
    },
    "template_economy_02": {
        "title": "실속 가성비형 기본 레이아웃",
        "description": "복잡한 설명 없이 깔끔하게 제품 스펙 위주로 소구하는 템플릿",
        "blocks": [
            {
                "type": "p1_hooking",
                "sub_title": "ESSENTIAL LINE",
                "main_title": "주방 혁명! 초간단 조립식 정리함 출시",
                "product_image": "https://picsum.photos/720/400",
                "bg_color": "#f3f4f6",
                "text_color": "#374151"
            }
        ]
    }
}


# =================================================================
# [TEMPLATE] 선택된 마스터 저장소 데이터를 쿠팡 규격 HTML로 빌드
# =================================================================
def compile_to_html(template_data):
    html_content = ""
    
    for block in template_data["blocks"]:
        # 1페이지: 후킹 + 상품 이미지 추가 공간
        if block["type"] == "p1_hooking":
            title_html = block["main_title"].replace("\n", "<br>")
            html_content += f"""
            <div style="background-color: {block['bg_color']}; color: {block['text_color']};" class="py-12 px-8 text-center border-b border-gray-100">
                <p class="text-blue-600 font-bold text-sm tracking-widest uppercase mb-3">{block['sub_title']}</p>
                <h1 class="text-3xl font-black leading-tight tracking-tight mb-8">{title_html}</h1>
                
                <div class="mx-auto max-w-[720px] rounded-2xl overflow-hidden shadow-lg border border-gray-100">
                    <img src="{block['product_image']}" class="w-full h-auto object-cover" alt="메인 상품 이미지">
                </div>
            </div>
            """
            
        # 2페이지: 문제제기 블록
        elif block["type"] == "p2_problem":
            title_html = block["title"].replace("\n", "<br>")
            html_content += f"""
            <div style="background-color: {block['bg_color']};" class="py-16 px-8 text-center border-b border-gray-100">
                <h2 class="text-2xl font-bold text-red-500 mb-4 leading-snug">{title_html}</h2>
                <p class="text-gray-600 text-base max-w-[600px] mx-auto">{block['desc']}</p>
            </div>
            """
            
        # 4페이지: 실물 이미지화 상세 영역
        elif block["type"] == "p4_real_image":
            html_content += f"""
            <div style="background-color: {block['bg_color']};" class="py-12 px-8 border-b border-gray-100">
                <h2 class="text-2xl font-bold text-gray-800 text-center mb-6">{block['section_title']}</h2>
                
                <div class="rounded-2xl overflow-hidden shadow-xl border border-gray-200">
                    <img src="{block['detail_image']}" class="w-full h-auto" alt="실물 연출 이미지">
                </div>
            </div>
            """
            
    # 최종 쿠팡 가로 780px 고정 캔버스 조립
    full_html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Noto Sans KR', sans-serif; }}</style>
    </head>
    <body class="bg-gray-800 flex justify-center items-start min-h-screen m-0 p-0">
        <div id="coupang-canvas" class="w-[780px] bg-white shadow-2xl overflow-hidden">
            {html_content}
        </div>
    </body>
    </html>
    """
    return full_html


# =================================================================
# [RENDERER] 브라우저 엔진으로 고화질 쿠팡 이미지(.png)로 최종 변환
# =================================================================
async def render_image(html_str, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # 세로 길이는 전체 컴포넌트가 다 나오도록 여유 있게 설정
        await page.set_viewport_size({"width": 780, "height": 3000})
        await page.set_content(html_str)
        
        # 웹용 이미지가 렌더링 캔버스에 완전히 로드될 때까지 2.5초 대기
        await page.wait_for_timeout(2500) 
        
        element = await page.query_selector("#coupang-canvas")
        if element:
            await element.screenshot(path=output_path, type="png")
        await browser.close()


# =================================================================
# [Streamlit WEB UI] 마스터 저장소 선택 및 웹 다운로드 인터페이스
# =================================================================
def main():
    st.set_page_config(page_title="쿠팡형 AI 상세페이지 마스터 v2.5", layout="centered")
    
    st.title("📦 쿠팡 상세페이지 자동화 시스템 v2")
    st.subheader("마스터 저장소 연동 및 고화질 통이미지 컴파일러")
    st.write("저장소에 보관된 기획 레이아웃을 불러와 쿠팡 공식 규격(가로 780px) 이미지로 굽습니다.")
    st.markdown("---")
    
    # 1. 템플릿 선택 UI (기존 CLI input 우회)
    template_options = {MASTER_REPOSITORY[k]["title"]: k for k in MASTER_REPOSITORY.keys()}
    selected_title = st.selectbox("🔮 마스터 저장소에서 불러올 템플릿을 선택하세요:", list(template_options.keys()))
    
    selected_key = template_options[selected_title]
    selected_template = MASTER_REPOSITORY[selected_key]
    output_filename = f"{selected_key}_result.png"
    
    # 템플릿 상세 설명 표시
    st.info(f"**선택된 템플릿 요약:** {selected_template['description']}")
    
    # 2. 이미지 빌드 버튼
    if st.button("🔥 완성형 상세페이지 8장 그룹화 및 마스터 이미지 빌드"):
        with st.spinner("플레이라이트 브라우저 엔진 구동 중... 약 3~5초 정도 소요됩니다."):
            # HTML 컴파일
            compiled_html = compile_to_html(selected_template)
            # 비동기 이미지 크롤러 엔진 작동
            asyncio.run(render_image(compiled_html, output_filename))
            
        # 3. 결과 확인 및 다운로드 창구 개설
        if os.path.exists(output_filename):
            st.success("🎉 쿠팡 규격 통상세페이지 이미지 변환에 성공했습니다!")
            
            # 생성된 이미지 파일 웹 화면에 즉시 피드백
            st.image(output_filename, caption="최종 렌더링 결과물 (가로 780px 정밀 매칭)", use_container_width=True)
            
            # 실물 파일 로컬 다운로드 다운로드 버튼 추가
            with open(output_filename, "rb") as file:
                st.download_button(
                    label="💾 고화질 실물 통이미지 다운로드 (.png)",
                    data=file,
                    file_name=output_filename,
                    mime="image/png"
                )
        else:
            st.error("❌ 이미지 파일 렌더링에 실패했습니다. 캔버스 영역 설정을 확인하세요.")

if __name__ == "__main__":
    main()
