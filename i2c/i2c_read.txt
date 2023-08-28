import machine
import time
import sys
from machine import SoftI2C, Pin

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
AT24C2 = 0x50

if not AT24C2 in i2c.scan():
    print("Could not find AT24C2")
    sys.exit()

def read_AT24C2_data(address, length):
    address_bytes = bytearray([address >> 8, address & 0xFF])
    i2c.writeto(AT24C2, address_bytes)
    time.sleep_ms(5)  # Delay to allow the EEPROM to process the address
    result = bytearray(length)
    i2c.readfrom_into(AT24C2, result)
    return result

if __name__ == "__main__":
    data = read_AT24C2_data(0x0000, 60)  # Read bytes starting from address 0x0000 and provide the length of data you want to read
    string_data = data.decode('utf-8')
    print("Data read from AT24C2:")
    print(string_data)
