from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
from PIL import Image

OUT_DIR = Path("data/synthetic")
IMG_DIR = OUT_DIR / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)


def make_image(size: int, difficulty: str) -> Image.Image:
    arr = np.random.randint(40, 180, size=(size, size), dtype=np.uint8)
    if difficulty == "good":
        arr[16:24, 16:24] = 220
    elif difficulty == "bad":
        arr = np.random.randint(100, 120, size=(size, size), dtype=np.uint8)
    return Image.fromarray(arr, mode="L")


def main(n: int = 200):
    rows = []
    for i in range(n):
        quality_good = 1 if random.random() > 0.2 else 0
        symptom_score = random.randint(0, 10)
        age = random.randint(45, 85)

        if symptom_score >= 8:
            disease_label = "glaucoma"
        elif symptom_score >= 5:
            disease_label = "diabetic_retinopathy"
        else:
            disease_label = "normal"

        img = make_image(64, "good" if quality_good else "bad")
        img_path = IMG_DIR / f"sample_{i:04d}.png"
        img.save(img_path)

        row = {
            "image_path": str(img_path),
            "quality_label": quality_good,
            "disease_label": disease_label,
            "age": age,
            "symptom_score": symptom_score,
        }
        rows.append(row)

    labels_path = OUT_DIR / "labels.jsonl"
    with labels_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    print(f"Wrote {labels_path} with {len(rows)} rows")


if __name__ == "__main__":
    main()
