import argparse
import subprocess

def change_wifi_config(ssid, password):
    config_file = '/etc/wpa_supplicant/wpa_supplicant.conf'
    new_config = f'''country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
}}'''

    # Write the new configuration to a temporary file
    temp_file = '/tmp/temp_wpa_supplicant.conf'
    with open(temp_file, 'w') as file:
        file.write(new_config)

    # Move the temporary file to the actual configuration file
    subprocess.run(['sudo', 'mv', temp_file, config_file], check=True)
    subprocess.run(['sudo', 'chmod', '600', config_file], check=True)

    # Restart the networking service
    subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], check=True)

def main():
    parser = argparse.ArgumentParser(description='Change WiFi SSID and password on Raspberry Pi')
    parser.add_argument('--ssid', nargs='+', required=True, help='New WiFi SSID')
    parser.add_argument('--password', required=True, help='New WiFi password')

    args = parser.parse_args()
    ssid = ' '.join(args.ssid)  # Join the SSID arguments with a space
    change_wifi_config(ssid, args.password)

if __name__ == '__main__':
    main()
