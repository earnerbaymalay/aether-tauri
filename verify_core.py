import sys
from pathlib import Path

# Add agent dir to path
sys.path.append(str(Path(__file__).parent / "agent"))

def test_imports():
    print("[*] Testing imports...")
    try:
        from system_scanner import SystemScanner
        from rag_engine import AetherRAG
        from p2p_sync import AetherLink
        print("[OK] All modules imported.")
    except Exception as e:
        print(f"[FAIL] Import error: {e}")

def test_scanner():
    print("[*] Testing System Scanner...")
    try:
        from system_scanner import SystemScanner
        scanner = SystemScanner()
        report = scanner.generate_report()
        if "OS:" in report:
            print("[OK] Scanner generated valid report.")
        else:
            print("[FAIL] Scanner report empty or invalid.")
    except Exception as e:
        print(f"[FAIL] Scanner error: {e}")

if __name__ == "__main__":
    test_imports()
    test_scanner()
    print("\n[DONE] Core logic verification complete.")
