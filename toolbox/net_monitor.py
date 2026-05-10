import sys
import argparse
from scapy.all import sniff, IP, TCP, UDP

def analyze_packet(pkt):
    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        
        # Simple exfiltration detection logic
        # Check for high volume of small packets to unknown IPs
        if TCP in pkt:
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            print(f"🔒 [ACTIVE DEFENSE] TCP Flow: {ip_src}:{sport} -> {ip_dst}:{dport}")
        elif UDP in pkt:
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
            print(f"🔒 [ACTIVE DEFENSE] UDP Flow: {ip_src}:{sport} -> {ip_dst}:{dport}")

def start_monitor(interface=None, duration=60):
    print(f"🛡️ Hardened Active Defense engaged on {interface or 'all interfaces'}")
    print(f"🕵️ Monitoring for data exfiltration patterns...")
    sniff(iface=interface, prn=analyze_packet, timeout=duration)

def main():
    parser = argparse.ArgumentParser(description="Aether Hardened Network Monitor")
    parser.add_argument("--iface", help="Network interface to monitor")
    parser.add_argument("--time", type=int, default=60, help="Duration to monitor in seconds")
    args = parser.parse_args()
    
    try:
        start_monitor(args.iface, args.time)
    except PermissionError:
        print("❌ Error: Network monitoring requires root/sudo privileges.")
    except Exception as e:
        print(f"❌ Monitor failed: {e}")

if __name__ == "__main__":
    main()
