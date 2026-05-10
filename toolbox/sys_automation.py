import subprocess
import argparse
import time

def list_windows():
    print("🪟 Active Windows:")
    result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True)
    print(result.stdout)

def focus_window(title):
    print(f"🎯 Focusing window: {title}")
    subprocess.run(["wmctrl", "-a", title])

def minimize_all():
    print("📉 Minimizing all windows...")
    subprocess.run(["xdotool", "key", "super+d"])

def open_app(command):
    print(f"🚀 Opening: {command}")
    subprocess.Popen(command, shell=True)

def type_text(text):
    print(f"⌨️  Typing: {text}")
    subprocess.run(["xdotool", "type", text])
    subprocess.run(["xdotool", "key", "Return"])

def main():
    parser = argparse.ArgumentParser(description="Aether System Automation")
    parser.add_argument("--list", action="store_true", help="List active windows")
    parser.add_argument("--focus", help="Focus window by title")
    parser.add_argument("--open", help="Open application")
    parser.add_argument("--type", help="Type text into active window")
    args = parser.parse_args()
    
    if args.list:
        list_windows()
    elif args.focus:
        focus_window(args.focus)
    elif args.open:
        open_app(args.open)
    elif args.type:
        type_text(args.type)

if __name__ == "__main__":
    main()
