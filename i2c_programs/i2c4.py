#CODE TO READ AND WRITE DATA WITH EEPROM
import sys
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

AT24C256 = 0x50

if not AT24C256 in i2c.scan():
    print("Could not find AT24C256")
    sys.exit()

def write_data_to_AT24C256(data):
    address = 0x00  # Starting address in AT24C256
    data_bytes = [address >> 8, address & 0xFF] + list(data)
    i2c.writeto(AT24C256, bytes(data_bytes))

if __name__ == "__main__":
    # Example data to be saved
    data_to_save = [12, 81, 19, 2, 5, 122, 0xCD, 0xEF]

    write_data_to_AT24C256(data_to_save)
    print("Data saved successfully!")

if not AT24C256 in i2c.scan():
    print("Could not find AT24C256")
    sys.exit()


def read_AT24C256_data(address, length):
    i2c.writeto(AT24C256, bytes([address >> 8, address & 0xFF]), stop=False)
    result = bytearray(length)
    i2c.readfrom_into(AT24C256, result)
    return result

if __name__ == "__main__":
    data = read_AT24C256_data(0x0000, 10)  # Read 10 bytes starting from address 0x0000
    print("Data read from AT24C256:", [int(byte) for byte in data])






