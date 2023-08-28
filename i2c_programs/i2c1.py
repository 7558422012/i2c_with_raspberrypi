#CODE TO GET DEVICE ID
import sys 
import board
import busio

i2c=busio.I2C(board.SCL, board.SDA)

print("I2C devices found:",[hex(i) for i in i2c.scan()])

AT24C256 = 0x50

if not AT24C256 in i2c.scan():
          print("Could not find AT24C256")
          sys.exit()

def get_AT24C256_id():
          i2c.writeto(AT24C256,bytes([0xd0]),stop=False)
          result=bytearray(1)
          i2c.readfrom_into(AT24C256, result)
          print("AT24C256 ID:",int.from_bytes(result,"big"))

if __name__=="__main__":
        get_AT24C256_id()
