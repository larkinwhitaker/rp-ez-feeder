import subprocess
import netifaces
# pip3 install netifaces


def updateWifiSettings(ssid, password):
    # Check available interfaces
    interfaces = netifaces.interfaces()
    
    # Find the wireless interface (usually wlan0)
    wlan_interface = [interface for interface in interfaces if "wlan" in interface]
    if not wlan_interface:
        print("Wireless interface not found.")
        return
    
    wlan_interface = wlan_interface[0]

    # Turn off WiFi
    subprocess.run(["sudo", "ifconfig", wlan_interface, "down"])

    # Change WiFi settings
    subprocess.run(["sudo", "iwconfig", wlan_interface, "essid", ssid])
    subprocess.run(["sudo", "iwconfig", wlan_interface, "key", f"'{password}'"])

    # Turn on WiFi
    subprocess.run(["sudo", "ifconfig", wlan_interface, "up"])

def testInternetConnection():
    try:
        subprocess.run(["ping", "-c", "3", "www.google.com"], check=True)
        print("Internet connection is active.")
        return True
    except subprocess.CalledProcessError:
        print("No internet connection.")
        return False
