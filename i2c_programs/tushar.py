import smbus
import time

# Define the I2C bus number and EEPROM address
bus = smbus.SMBus(1)
eeprom_address = 0x50

# Function to write a byte of data to the EEPROM
def write_byte(address, data):
    bus.write_byte_data(eeprom_address, address, data)
    time.sleep(0.01)  # Delay to allow the write operation to complete

# Prompt the user to enter the memory address and data byte
address = input("Enter memory address (0-32767): ")
data = input("Enter data byte (0-255): ")

# Convert the input values to integers
address = int(address)
data = int(data)

# Validate the input values
if address < 0 or address > 32767:
    print("Invalid memory address!")
    exit()

if data < 0 or data > 255:
    print("Invalid data byte!")
    exit()

# Split the 16-bit address into two bytes
address_high = (address >> 8) & 0xFF
address_low = address & 0xFF

# Write the address and data to the EEPROM
write_byte(address_high, data)
write_byte(address_low, data)

print("Data written successfully to the EEPROM.")

