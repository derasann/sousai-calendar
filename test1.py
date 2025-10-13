import streamlit as st
import calendar
import datetime
import os
import chardet
from pathlib import Path

# ===== 設定 =====
PHOTO_DIR = Path("photos")
TEXT_DIR = Path("texts_recovered_final")

st.set_page_config(page_title="高市新総裁の動静", layout="wide")


# ---- 日本語フォント指定 ----
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🗓️ 高市新総裁の動静")

# 今日の年月
today = datetime.date.today()
year = today.year
month = today.month

# ---- カレンダー風に日ごとに表示 ----
days = sorted(TEXT_DIR.glob("*.txt"))

for txt_file in days:
    date_label = txt_file.stem  # 例: 2025-10-04
    img_path = PHOTO_DIR / f"{date_label}.jpg"

    # 📦 カードの外枠コンテナ
    with st.container():
        st.markdown(
            """
            <style>
            .card {
                background-color: #f8f9fa;
                border-radius: 16px;
                padding: 16px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .card-date {
                font-weight: 600;
                color: #2b2b2b;
                font-size: 1.1rem;
                margin-bottom: 8px;
            }
            .card-img {
                width: 100%;
                border-radius: 10px;
                margin-bottom: 10px;
            }
            .card-text {
                font-size: 1rem;
                line-height: 1.6;
                color: #333;
                white-space: pre-wrap;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(f"<div class='card'>", unsafe_allow_html=True)

        # 🗓️ 日付
        st.markdown(f"<div class='card-date'>🗓️ {date_label}</div>", unsafe_allow_html=True)

        # 🖼️ 画像
        if img_path.exists():
            st.image(str(img_path), use_container_width=600)
        else:
            st.write("（画像なし）")

        # 📝 テキスト
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
        st.markdown(f"<div class='card-text'>{text}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)