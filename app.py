import asyncio
import os
from playwright.async_api import async_playwright

# =================================================================
# [3번째 요구사항] 마스터 저장소 시스템 (Master Repository DB 시뮬레이션)
# =================================================================
# 나중에 진짜 DB(MySQL, MongoDB 등)나 JSON 파일 저장소로 대체될 영역입니다.
MASTER_REPOSITORY = {
    "template_premium_01": {
        "title": "루시아이 슬라이딩 정리함 프리미엄형",
        "description": "강력한 후킹 문구, 1페이지 이미지 연동 및 4페이지 실물 크롭 컷이 포함된 완벽형 템플릿",
        "blocks": [
            {
                "type": "p1_hooking",  # [1번째 요구사항] 1페이지 이미지 추가 공간 반영
                "sub_title": "PREMIUM HOUSEHOLD SOLUTIONS",
                "main_title": "공간의 가치를 바꾸는 단 하나의 선택\n루시아이 스택 슬라이딩 팬트리 정리함",
                "product_image": "https://picsum.photos/720/450", # 실제 내 상품 이미지 주소 입력 가능
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
                "detail_image": "https://picsum.photos/720/600", # 실제 상세페이지용 연출 컷
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
            
        # 4페이지: 실물 이미지화 상세 영역 (이미지 중심 설계)
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
        # 세로 길이는 전체 컴포넌트가 다 나오도록 충분히 길게 설정 (3000px)
        await page.set_viewport_size({"width": 780, "height": 3000})
        await page.set_content(html_str)
        
        # 외부 이미지(Picsum 등)가 브라우저에 완전히 로드될 때까지 2.5초간 충분히 대기
        await page.wait_for_timeout(2500) 
        
        element = await page.query_selector("#coupang-canvas")
        if element:
            await element.screenshot(path=output_path, type="png")
            print(f"\n🎉 [성공] 상세페이지 이미지 변환 완료! 파일 저장경로: '{output_path}'")
        else:
            print("\n❌ [에러] 렌더링 캔버스를 찾을 수 없습니다.")
            
        await browser.close()

# =================================================================
# [MAIN CLI] 마스터 저장소 선택 및 실행 인터페이스
# =================================================================
def main():
    print("="*60)
    print(" 📦 쿠팡 상세페이지 자동화 프로그램 v2 (마스터 저장소 시스템)")
    print("="*60)
    print("저장소에서 불러올 수 있는 템플릿 목록입니다:\n")
    
    keys = list(MASTER_REPOSITORY.keys())
    for idx, key in enumerate(keys):
        print(f"[{idx + 1}] {MASTER_REPOSITORY[key]['title']}")
        print(f"    - 설명: {MASTER_REPOSITORY[key]['description']}\n")
        
    try:
        choice = int(input(" 불러올 마스터 저장소 번호를 선택하세요 (숫자 입력): ")) - 1
        if choice < 0 or choice >= len(keys):
            print("❌ 잘못된 번호입니다. 프로그램을 종료합니다.")
            return
        
        selected_key = keys[choice]
        selected_template = MASTER_REPOSITORY[selected_key]
        output_filename = f"{selected_key}_result.png"
        
        print(f"\n▶ 選択: '{selected_template['title']}' 저장소를 로드했습니다.")
        print("▶ 변형 및 이미지 빌드를 시작합니다 (약 3~5초 소요)...")
        
        # 1. 템플릿 컴파일 (HTML 생성)
        compiled_html = compile_to_html(selected_template)
        
        # 2. 이미지 굽기 (비동기 Playwright 실행)
        asyncio.run(render_image(compiled_html, output_filename))
        
    except ValueError:
        print("❌ 숫자로 정확히 입력해 주세요.")

if __name__ == "__main__":
    main()
