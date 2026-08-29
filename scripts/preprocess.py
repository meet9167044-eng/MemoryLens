from PIL import Image, ImageEnhance, ImageFilter
import os

def preprocess_screenshot(input_path: str, output_dir: str) -> dict:
    """
    PHASE 4 — MemoryLens Image Preprocessing Pipeline
    
    Takes a raw screenshot and produces:
    1. A normalized version (RGB, resized)
    2. An OCR-ready version (grayscale, enhanced contrast)
    
    Args:
        input_path : Path to the original raw screenshot
        output_dir : Folder where processed images will be saved
    
    Returns:
        A dictionary with paths to all generated assets
    """
    
    # --- Setup ---
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(input_path))[0]
    
    result = {
        "original_path": input_path,
        "normalized_path": None,
        "ocr_ready_path": None,
        "width": None,
        "height": None,
        "success": False,
        "error": None
    }
    
    try:
        # ── STAGE 1: Load & Validate ──────────────────────────
        print(f"[Phase 4] Loading: {input_path}")
        img = Image.open(input_path)
        print(f"[Phase 4] Original size: {img.size}, Mode: {img.mode}")
        
        # ── STAGE 2: Normalize ────────────────────────────────
        # Convert to RGB (removes transparency from PNGs)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (cap at 1920px width)
        MAX_WIDTH = 1920
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / float(img.width)
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
        
        result["width"] = img.width
        result["height"] = img.height
        
        # Save normalized image
        normalized_path = os.path.join(output_dir, f"{filename}_normalized.jpg")
        img.save(normalized_path, format="JPEG", quality=95)
        result["normalized_path"] = normalized_path
        print(f"[Phase 4] Normalized saved: {normalized_path}")
        
        # ── STAGE 3: Enhance for OCR ──────────────────────────
        # Convert to grayscale
        img_ocr = img.convert("L")
        
        # Increase sharpness
        img_ocr = ImageEnhance.Sharpness(img_ocr).enhance(2.0)
        
        # Increase contrast
        img_ocr = ImageEnhance.Contrast(img_ocr).enhance(1.5)
        
        # Final sharpen filter
        img_ocr = img_ocr.filter(ImageFilter.SHARPEN)
        
        # Save OCR-ready image
        ocr_ready_path = os.path.join(output_dir, f"{filename}_ocr_ready.jpg")
        img_ocr.save(ocr_ready_path, format="JPEG", quality=95)
        result["ocr_ready_path"] = ocr_ready_path
        print(f"[Phase 4] OCR-ready saved: {ocr_ready_path}")
        
        result["success"] = True
        print(f"[Phase 4] ✅ Preprocessing complete!")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"[Phase 4] ❌ Error: {e}")
    
    return result


# --- Test the pipeline ---
if __name__ == "__main__":
    input_file  = "test_screenshot.png"
    output_dir  = "output"
    
    if os.path.exists(input_file):
        result = preprocess_screenshot(input_file, output_dir)
        
        print("\n── RESULT ──────────────────────────")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print(f"Please put '{input_file}' in this folder first!")