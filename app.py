import streamlit as st
import json
import base64
import os
from weasyprint import HTML, CSS

# 1. 페이지 초기 설정 (와이드 레이아웃 및 앱 타이틀)
st.set_page_config(page_title="쿠팡형 넥스트 AI 상세페이지 빌더 v22.0", layout="wide")

# 2. 고화질 렌더링 엔진 (HTML/CSS -> 이미지/PDF 변환)
def render_json_to_image(json_data):
    """
    JSON 데이터를 세련된 HTML/CSS 템플릿으로 변환한 뒤,
    WeasyPrint를 사용하여 쿠팡 규격(가로 780px)의 고화질 바이너리로 렌더링합니다.
    """
    # 기본 스타일 및 웹폰트 주입 (나눔고딕 적용)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
            @page {{
                size: 780px auto;
                margin: 0;
            }}
            body {{
                width: 780px;
                margin: 0;
                padding: 0;
                font-family: 'Nanum Gothic', sans-serif;
                background-color: #ffffff;
                color: #333333;
                -webkit-print-color-adjust: exact;
            }}
            .block {{
                width: 780px;
                box-sizing: border-box;
                padding: 60px 50px;
                text-align: center;
                overflow: hidden;
            }}
            /* 블록 타입별 스타일 시트 */
            .header_hero {{
                background-color: #1a233a;
                color: #ffffff;
                padding: 80px 50px;
            }}
            .header_hero .badge {{
                color: #ffb703;
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 2px;
                margin-bottom: 15px;
                display: block;
            }}
            .header_hero .sub_title {{
                color: #cbd5e1;
                font-size: 24px;
                margin-bottom: 20px;
                font-weight: 400;
            }}
            .header_hero .main_title {{
                font-size: 42px;
                font-weight: 800;
                line-height: 1.3;
                color: #ffffff;
                word-break: keep-all;
            }}
            
            .pain_point {{
                background-color: #111111;
                color: #ffffff;
            }}
            .pain_point .warning_icon {{
                color: #ef4444;
                font-size: 40px;
                margin-bottom: 15px;
            }}
            .pain_point .title {{
                font-size: 32px;
                font-weight: 700;
                color: #f3f4f6;
                margin-bottom: 30px;
                line-height: 1.4;
            }}
            .pain_point .quote_box {{
                background-color: #222222;
                border-left: 5px solid #ef4444;
                padding: 20px;
                font-size: 20px;
                color: #dc2626;
                font-weight: 700;
                text-align: left;
                margin: 0 auto;
                max-width: 600px;
            }}

            .feature_grid_2x2 {{
                background-color: #ffffff;
            }}
            .feature_grid_2x2 .section_title {{
                font-size: 28px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 40px;
            }}
            .grid_container {{
                display: block;
                text-align: left;
            }}
            .grid_item {{
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 25px;
                margin-bottom: 20px;
            }}
            .grid_item .item_title {{
                font-size: 22px;
                font-weight: 700;
                color: #1e40af;
                margin-bottom: 10px;
            }}
            .grid_item .item_desc {{
                font-size: 16px;
                color: #475569;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
    """

    # JSON 데이터를 순회하며 HTML 마크업 동적 생성
    for block in json_data.get("blocks", []):
        b_type = block.get("type")
        content = block.get("content", {})
        
        if b_type == "header_hero":
            html_content += f"""
            <div class="block header_hero">
                <span class="badge">PREMIUM SELECTION</span>
                <div class="sub_title">{content.get('sub_title', '')}</div>
                <div class="main_title">{content.get('main_title', '')}</div>
            </div>
            """
        elif b_type == "pain_point":
            html_content += f"""
            <div class="block pain_point">
                <div class="warning_icon">🚨</div>
                <div class="title">{content.get('title', '')}</div>
                <div class="quote_box">“ {content.get('quote', '')} ”</div>
            </div>
            """
        elif b_type == "feature_grid_2x2":
            html_content += f"""
            <div class="block feature_grid_2x2">
                <div class="section_title">{content.get('title', '')}</div>
                <div class="grid_container">
            """
            for item in content.get("items", []):
                html_content += f"""
                    <div class="grid_item">
                        <div class="item_title">✔ {item.get('title', '')}</div>
                        <div class="item_desc">{item.get('desc', '')}</div>
                    </div>
                """
            html_content += """
                </div>
            </div>
            """
            
    html_content += "</body></html>"
    
    # WeasyPrint를 통한 컴파일 후 PDF/이미지 바이너리 반환
    return HTML(string=html_content).write_pdf()

# 3. 세션 상태 고도화 및 기본 가상 데이터베이스(JSON 데이터) 정의
if "detail_json" not in st.session_state:
    st.session_state["detail_json"] = {
        "template_id": "bench_001",
        "template_name": "쿠팡 상위 1% 슬라이딩 정리함 구조",
        "blocks": [
            {
                "id": "block_1",
                "type": "header_hero",
                "content": {
                    "sub_title": "공간의 가치를 바꾸는 단 하나의 선택",
                    "main_title": "[당일출고] 루시아이 스택 슬라이딩 팬트리 정리함"
                }
            },
            {
                "id": "block_2",
                "type": "pain_point",
                "content": {
                    "title": "아직도 깊숙한 싱크대 하부장에 물건을 무조건 쌓아두기만 하십니까?",
                    "quote": "안쪽 물건 한번 꺼내려다가 위에 쌓인 가구들이 다 쏟아져 내렸어요..."
                }
            },
            {
                "id": "block_3",
                "type": "feature_grid_2x2",
                "content": {
                    "title": "생활의 질을 높이는 루시아이만의 2대 핵심 혁신",
                    "items": [
                        {"title": "볼베어링 내장식 프리미엄 레일 슬라이딩", "desc": "손가락 하나로도 스르륵, 안쪽 깊숙이 숨어있는 무거운 냄비까지 부드럽고 안전하게 꺼낼 수 있습니다."},
                        {"title": "흔들림 없는 고하중 모듈러 스택 시스템", "desc": "상하단 적층 결합 홈 설계로 다단으로 높이 쌓아도 쓰러지거나 휘어짐 없이 완벽하게 데드스페이스를 제거합니다."}
                    ]
                }
            }
        ]
    }

# 4. 메인 대시보드 UI 설계
st.title("🎯 쿠팡형 차세대 AI 상세페이지 엔진 v22.0")
st.caption("고정 좌표 방식(PIL)을 폐기하고, 확장 가능한 [JSON 구조화 데이터 ➔ HTML 컴포넌트 ➔ 고화질 렌더러] 아키텍처를 채택했습니다.")
st.markdown("---")

col_edit, col_preview = st.columns([1, 1])

# =========================================================================
# 🛠️ [모듈 3. 데이터 매핑 & 편집 UI 영역] - 왼쪽 화면
# =========================================================================
with col_edit:
    st.header("📝 3단계: 내 상품 정보 및 카피라이팅 편집")
    st.write("벤치마킹 데이터(JSON) 구조에 맞춰 텍스트 데이터를 즉시 수정 및 매핑합니다.")
    
    # 세션에 기록된 JSON 객체를 참조하여 폼 필드 동적 바인딩
    updated_blocks = []
    
    for idx, block in enumerate(st.session_state["detail_json"]["blocks"]):
        b_type = block["type"]
        b_id = block["id"]
        
        with st.expander(f"📦 블록 {idx+1} : {b_type.upper()} 레이아웃 컴포넌트", expanded=True):
            if b_type == "header_hero":
                sub_t = st.text_input(f"상단 감성 서브타이틀 ({b_id})", value=block["content"]["sub_title"])
                main_t = st.text_area(f"메인 셀링 상품명 ({b_id})", value=block["content"]["main_title"])
                updated_blocks.append({
                    "id": b_id, "type": b_type, 
                    "content": {"sub_title": sub_t, "main_title": main_t}
                })
                
            elif b_type == "pain_point":
                p_title = st.text_area(f"고객 문제 제기 헤드라인 ({b_id})", value=block["content"]["title"])
                p_quote = st.text_input(f"리얼 고객 인용구 ({b_id})", value=block["content"]["quote"])
                updated_blocks.append({
                    "id": b_id, "type": b_type, 
                    "content": {"title": p_title, "quote": p_quote}
                })
                
            elif b_type == "feature_grid_2x2":
                g_title = st.text_input(f"기능 블록 대타이틀 ({b_id})", value=block["content"]["title"])
                items = []
                for j, item in enumerate(block["content"]["items"]):
                    st.markdown(f"**🔹 기능 포인트 0{j+1}**")
                    i_title = st.text_input(f"특징 제목 {j+1}", value=item["title"], key=f"it_{b_id}_{j}")
                    i_desc = st.text_area(f"특징 상세 설명 {j+1}", value=item["desc"], key=f"id_{b_id}_{j}")
                    items.append({"title": i_title, "desc": i_desc})
                updated_blocks.append({
                    "id": b_id, "type": b_type, 
                    "content": {"title": g_title, "items": items}
                })

    # 동기화 버튼 클릭 시 세션 스테이트 반영
    if st.button("🔄 매핑 데이터 최종 동기화 및 적용"):
        st.session_state["detail_json"]["blocks"] = updated_blocks
        st.success("JSON 구조화 템플릿에 데이터가 성공적으로 매핑되었습니다!")

    st.markdown("### 🗂️ 현재 세션 템플릿 데이터 구조화 상태 (JSON Schema)")
    st.json(st.session_state["detail_json"])

# =========================================================================
# 🖼️ [모듈 4. 최종 고화질 렌더링 & 다운로드 영역] - 오른쪽 화면
# =========================================================================
with col_preview:
    st.header("🖼️ 4단계: 쿠팡 가로 780px 정밀 프리뷰")
    st.write("아래 화면은 HTML/CSS 컴포넌트로 완벽하게 구조화되어 렌더링된 실시간 미리보기입니다.")
    
    # 렌더링 가동
    try:
        pdf_bytes = render_json_to_image(st.session_state["detail_json"])
        
        # 브라우저에 임베딩하여 사용자에게 화면 출력 시각화
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900px" style="border:1px solid #cbd5e1; border-radius:8px;"></iframe>'
        
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("💾 최종 고화질 마스터 파일 다운로드 센터")
        
        st.download_button(
            label="🚀 쿠팡 등록용 고화질 원본 파일 다운로드",
            data=pdf_bytes,
            file_name=f"coupang_master_page_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"렌더링 엔진 내부 컴파일 에러: {e}")
        st.info("Tip: 백엔드 환경에 `weasyprint` 라이브러리가 올바르게 구성되었는지 확인하십시오.")
