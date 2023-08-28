#Reboot with change ipaddress of RaspberryPi
import argparse
import os

def reboot_raspberry_pi(ip_address):
    # Change the static IP address configuration
    config_lines = [
        "interface eth0",
        f"static ip_address={ip_address}/24",
        "static routers=192.168.6.1",
        "static domain_name_servers=192.168.6.1"
    ]
    config_content = "\n".join(config_lines)
    with open("/etc/dhcpcd.conf", "w") as config_file:
        config_file.write(config_content)

    # Reboot the Raspberry Pi
    os.system("sudo reboot")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reboot Raspberry Pi 4 and change static IP address")
    parser.add_argument("ip_address", type=str, help="New static IP address")

    args = parser.parse_args()
    ip_address = args.ip_address

    reboot_raspberry_pi(ip_address)

