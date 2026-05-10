import os
import subprocess
import argparse
import base64
import requests
from pathlib import Path

def capture_screen(output_path):
    print(f"📸 Capturing screen to: {output_path}")
    subprocess.run(["scrot", "-z", output_path], check=True)

def analyze_image(image_path, prompt="What is on this screen? Describe the windows and content."):
    print(f"👁️  Aether Eye analyzing image with moondream...")
    
    with open(image_path, "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    payload = {
        "model": "moondream",
        "prompt": prompt,
        "stream": False,
        "images": [img_base64]
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
        result = response.json()
        return result.get("response", "No analysis returned.")
    except Exception as e:
        return f"❌ Analysis failed: {e}"

def main():
    parser = argparse.ArgumentParser(description="Aether Eye - Neural Vision")
    parser.add_argument("--prompt", default="Describe the current screen state.", help="Analysis prompt")
    args = parser.parse_args()
    
    img_path = Path.home() / ".aether" / "vision_capture.png"
    img_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        capture_screen(str(img_path))
        analysis = analyze_image(str(img_path), args.prompt)
        print("\n🧠 Neural Analysis:")
        print(analysis)
    except Exception as e:
        print(f"❌ Vision system error: {e}")

if __name__ == "__main__":
    main()
