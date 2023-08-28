#i2c data write in EEPROM
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
    data_to_save = [23, 11, 19, 2, 5, 6, 0xCD, 0xEF]

    write_data_to_AT24C256(data_to_save)
    print("Data saved successfully!")
