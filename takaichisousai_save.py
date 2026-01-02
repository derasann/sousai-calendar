#カレンダーは出る。画像が大きさまちまちを調整。

import streamlit as st
import calendar
import datetime
from pathlib import Path

PHOTO_DIR = Path("photos_resized")
TEXT_DIR = Path("texts_recovered_final")

st.set_page_config(page_title="高市総理の一日", layout="wide")

# ===== CSS =====
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", sans-serif;
}
.card {
    background-color: #f8f9fa;
    border-radius: 12px;
    padding: 10px;
    margin: 6px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    height: auto;
}
.card-date {
    font-weight: bold;
    margin-bottom: 4px;
}
.card-img {
    width: 100%;
    height: 220px;             /* 高さを統一 */
    object-fit: cover;         /* 中央トリミングでバランス */
    border-radius: 10px;
    margin-bottom: 8px;
    transition: transform 0.2s ease-in-out;
}
.card-img:hover {
    transform: scale(1.03);
}
.card-text {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #f9f9f9;
    background-color: #1e40af;
    padding: 10px;
    border-radius: 8px;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

st.title("🗞️ 高市総理の一日")

# ===== モード選択 =====
mode = st.radio("表示モードを選択：", ["カード表示", "カレンダー表示"])

days = sorted(TEXT_DIR.glob("*.txt"), reverse=True)

# ===== カード表示 =====
if mode == "カード表示":
    for txt_file in days:
        date_label = txt_file.stem

        # カード外枠
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-date'>🗓️ {date_label}</div>", unsafe_allow_html=True)

            # ✅ 同じ日付の複数画像に対応（Streamlitで確実に表示）
            img_files = sorted(PHOTO_DIR.glob(f"{date_label}*.jpg"))

            if img_files:
                cols = st.columns(min(3, len(img_files)))  # 最大3列
                for i, img in enumerate(img_files):
                    with cols[i % 3]:
                        st.image(str(img), width="stretch")
            else:
                st.caption("（画像なし）")

            # ✅ テキスト部分
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                st.markdown(f"<div class='card-text'>{text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"テキスト読込エラー: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

# ===== カレンダー表示 =====
elif mode == "カレンダー表示":
    # 初期化（セッション保持）
    if "current_year" not in st.session_state:
        today = datetime.date.today()
        st.session_state.current_year = today.year
        st.session_state.current_month = today.month

    # 前月・翌月ボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 前の月"):
            if st.session_state.current_month == 1:
                st.session_state.current_month = 12
                st.session_state.current_year -= 1
            else:
                st.session_state.current_month -= 1
    with col3:
        if st.button("次の月 ➡️"):
            if st.session_state.current_month == 12:
                st.session_state.current_month = 1
                st.session_state.current_year += 1
            else:
                st.session_state.current_month += 1

    year = st.session_state.current_year
    month = st.session_state.current_month

    # タイトル
    st.markdown(
        f"""
        <h2 style='text-align:center; background-color:#2563eb;
        color:white; 
        padding:10px; border-radius:6px; font-weight:600;letter-spacing:1px;'>
            🗓️ {year}年 {month}月 の予定
        </h2>
        """,
        unsafe_allow_html=True
    )

    # カレンダー生成
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdatescalendar(year, month)

    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            date_str = day.strftime("%Y-%m-%d")
            txt_path = TEXT_DIR / f"{date_str}.txt"
            img_files = sorted(PHOTO_DIR.glob(f"{date_str}*.jpg"))

            with cols[i]:
                if day.month == month:
                    st.markdown(f"<div class='card-date'>{day.day}</div>", unsafe_allow_html=True)
                 
                    # ✅ 画像（１枚のみ）
                    img_path = PHOTO_DIR / f"{date_str}.jpg"

                    if img_path.exists():
                            st.image(str(img_path), width="stretch")


                    # ✅ テキスト表示
                    if txt_path.exists():
                        with open(txt_path, "r", encoding="utf-8") as f:
                            text = f.read().strip()
                        st.caption(text[:40] + "..." if len(text) > 40 else text)
