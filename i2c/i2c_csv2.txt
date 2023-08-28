import network
import ure
import machine
import time
import sys
from machine import I2C, Pin

wlan = network.WLAN(network.STA_IF)  # create station interface
wlan.active(True)  # activate the interface
wlan.connect('vivo', '12345678')  # connect to an AP

# Wait until connected to the network
while not wlan.isconnected():
    time.sleep(1)

print('Connected to network:', wlan.ifconfig())

i2c = I2C(scl=Pin(22), sda=Pin(21))
AT24C2 = 0x50

if not AT24C2 in i2c.scan():
    print("Could not find AT24C2")
    sys.exit()

def write_data_to_AT24C2(data):
    address = 0x00  # Starting address in AT24C256
    data_bytes = bytearray([address >> 8, address & 0xFF]) + bytearray(data, 'utf-8')
    i2c.writeto(AT24C2, data_bytes)

if __name__ == "__main__":
    # Read CSV data
    with open("tushar.csv", "r") as csv_file:
        data_to_save = csv_file.read()

    # Write data to AT24C2 EEPROM
    write_data_to_AT24C2(data_to_save)
    print("Data saved successfully!")

if not AT24C2 in i2c.scan():
    print("Could not find AT24C256")
    sys.exit()

def read_AT24C2_data(address, length):
    address_bytes = bytearray([address >> 8, address & 0xFF])
    i2c.writeto(AT24C2, address_bytes)
    time.sleep_ms(5)  # Delay to allow the EEPROM to process the address
    result = bytearray(length)
    i2c.readfrom_into(AT24C2, result)
    return result

if __name__ == "__main__":
    data = read_AT24C2_data(0x0000, len(data_to_save))  # Read bytes starting from address 0x0000
    string_data = data.decode('utf-8')
    print("Data read from AT24C2:")
    print(string_data)
