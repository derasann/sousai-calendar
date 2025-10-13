from PIL import Image
from pathlib import Path

# === 設定 ===
SOURCE_DIR = Path("photos")             # 元画像フォルダ
OUTPUT_DIR = Path("photos_resized")     # 出力先フォルダ
TARGET_SIZE = (1276, 798)               # 幅×高さ(px)
TARGET_DPI = (72, 72)                   # 解像度(dpi)

# 出力フォルダを作成
OUTPUT_DIR.mkdir(exist_ok=True)

# 対象ファイルを取得
image_files = list(SOURCE_DIR.glob("*.jpg")) + list(SOURCE_DIR.glob("*.jpeg")) + list(SOURCE_DIR.glob("*.png"))

print(f"📷 {len(image_files)} 枚の画像を処理します...")

def resize_and_crop(img: Image.Image, size):
    """アスペクト比を維持して中央トリミング"""
    target_w, target_h = size
    orig_w, orig_h = img.size
    orig_ratio = orig_w / orig_h
    target_ratio = target_w / target_h

    # まずアスペクト比を保ったまま最小辺がフィットするようにリサイズ
    if orig_ratio > target_ratio:
        # 横長 → 高さを合わせる
        new_h = target_h
        new_w = int(new_h * orig_ratio)
    else:
        # 縦長 → 幅を合わせる
        new_w = target_w
        new_h = int(new_w / orig_ratio)

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # 中央をトリミング
    left = (new_w - target_w) / 2
    top = (new_h - target_h) / 2
    right = left + target_w
    bottom = top + target_h

    return img_resized.crop((left, top, right, bottom))

for img_path in image_files:
    try:
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            result = resize_and_crop(img, TARGET_SIZE)

            out_path = OUTPUT_DIR / img_path.with_suffix(".jpg").name
            result.save(out_path, "JPEG", dpi=TARGET_DPI, quality=95)
            print(f"✅ {img_path.name} → {out_path.name}")
    except Exception as e:
        print(f"⚠️ {img_path.name} の処理中にエラー: {e}")

print("🎉 すべての画像をリサイズ＆中央トリミングして photos_resized に保存しました。")
