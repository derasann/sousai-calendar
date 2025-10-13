import os

# texts フォルダを対象にする
folder = "texts"

# フォルダ内の全 .txt ファイルを処理
for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        path = os.path.join(folder, filename)
        try:
            # Shift-JIS で読み込んで UTF-8 で書き直す
            with open(path, "r", encoding="shift_jis", errors="ignore") as f:
                content = f.read()
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Converted: {filename}")
        except Exception as e:
            print(f"⚠️ Skipped {filename}: {e}")

print("🎉 すべてのtxtファイルをUTF-8に変換しました。")
