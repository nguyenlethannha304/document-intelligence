from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import pytesseract
import io

app = FastAPI(title="Tesseract OCR Service", version="1.1.0")


@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ocr")
async def ocr(
    file: UploadFile = File(...),
    lang: str = "eng",
    config: str = "--oem 3 --psm 6",
    include_words: bool = False
):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")

        # OCR text
        text = pytesseract.image_to_string(image, lang=lang, config=config)

        # OCR detailed data (includes confidence)
        data = pytesseract.image_to_data(
            image,
            lang=lang,
            config=config,
            output_type=pytesseract.Output.DICT
        )

        words = []
        confidences = []

        n = len(data.get("text", []))
        for i in range(n):
            w = (data["text"][i] or "").strip()
            conf_raw = str(data["conf"][i]).strip()

            # Tesseract uses -1 for non-word / invalid confidence
            try:
                conf = float(conf_raw)
            except Exception:
                continue

            if conf >= 0 and w:
                confidences.append(conf)
                if include_words:
                    words.append({
                        "text": w,
                        "confidence": round(conf, 2),
                        "bbox": {
                            "left": int(data["left"][i]),
                            "top": int(data["top"][i]),
                            "width": int(data["width"][i]),
                            "height": int(data["height"][i]),
                        }
                    })

        avg_conf = round(sum(confidences) / len(confidences), 2) if confidences else None

        resp = {
            "filename": file.filename,
            "lang": lang,
            "text": text,
            "avg_confidence": avg_conf,
            "word_count": len(confidences),
        }

        if include_words:
            resp["words"] = words

        return resp

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {e}")