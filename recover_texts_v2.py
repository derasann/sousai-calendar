# recover_texts_v2.py
import os

folder = "texts"
output_folder = "texts_recovered"
os.makedirs(output_folder, exist_ok=True)

for fn in os.listdir(folder):
    if not fn.endswith(".txt"):
        continue
    src = os.path.join(folder, fn)
    dst = os.path.join(output_folder, fn)
    print(f"▶️ {fn} 復元中...")

    with open(src, "rb") as f:
        raw = f.read()

    candidates = []
    # --- ① UTF-8 → Shift-JIS逆変換パターン ---
    try:
        recovered = raw.decode("utf-8", errors="ignore").encode("latin1").decode("cp932")
        candidates.append(recovered)
        print("✅ UTF-8→latin1→cp932 成功")
    except Exception:
        pass

    # --- ② UTF-8→EUC-JP逆変換パターン ---
    try:
        recovered = raw.decode("utf-8", errors="ignore").encode("latin1").decode("euc_jp")
        candidates.append(recovered)
        print("✅ UTF-8→latin1→euc_jp 成功")
    except Exception:
        pass

    # --- ③ Shift-JISファイルをUTF-8誤保存したパターン ---
    try:
        recovered = raw.decode("cp932", errors="ignore")
        candidates.append(recovered)
        print("✅ cp932直接読み 成功")
    except Exception:
        pass

    if candidates:
        # 最も長いテキストを採用（復元成功率が高い）
        text = max(candidates, key=len)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"🎉 {fn} を texts_recovered に保存しました\n")
    else:
        print(f"⚠️ {fn} の復元にすべて失敗しました\n")
