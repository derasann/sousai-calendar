# recover_texts_final.py
import os

folder = "texts"
output_folder = "texts_recovered_final"
os.makedirs(output_folder, exist_ok=True)

for fn in os.listdir(folder):
    if not fn.endswith(".txt"):
        continue
    src = os.path.join(folder, fn)
    dst = os.path.join(output_folder, fn)
    print(f"▶️ {fn} 再復元中...")

    try:
        # ① UTF-8として文字列を読み込み
        with open(src, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        # ② 文字列を再び「バイト列」に戻す（UTF-8文字をそのまま1バイトとして扱う）
        data = txt.encode("cp932", errors="ignore")
        # ③ それをUTF-8として再解釈
        fixed = data.decode("utf-8", errors="ignore")

        with open(dst, "w", encoding="utf-8") as f:
            f.write(fixed)

        print(f"🎉 {fn} を再復元して texts_recovered_final に保存しました\n")

    except Exception as e:
        print(f"⚠️ {fn} の復元に失敗しました: {e}\n")
