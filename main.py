import socket
from machine import Pin

led_pin = Pin(5, Pin.OUT)

CONTENT = """\
HTTP/1.0 200 OK
Content-Type: text/html

<html>
  <head>
  </head>
  <body>
    <p>Hello #%d from MicroPython!</p>
    <a href="/toggle">Click here to toggle LED hooked to pin 5</a>
  </body>
</html>
"""

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    counter = 0
    while True:
        sock, addr = s.accept()
        print("Client address:", addr)
        stream = sock.makefile("rwb")
        req = stream.readline().decode("ascii")
        method, path, protocol = req.split(" ")
        print("Got", method, "request for", path)
        if path == "/toggle":
            led_pin.value(1-led_pin.value())
        while True:
            h = stream.readline().decode("ascii").strip()
            if h == "":
                break
            print("Got HTTP header:", h)
        stream.write((CONTENT % counter).encode("ascii"))
        stream.close()
        sock.close()
        counter += 1
        print()

main() # Press Ctrl-C to stop web server

from time import sleep_ms
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(-1, Pin(4),Pin(5),freq=400000) # Bitbanged I2C bus
assert 60 in i2c.scan(), "No OLED display detected!"
oled = SSD1306_I2C(128, 64, i2c)
buf = "Hello Tristan wadup  "
oled.invert(0) # White text on black background
oled.contrast(255) # Maximum contrast
j = 0

while True:
    oled.fill(0)
    oled.text(buf[j%len(buf):]+buf, 10, 10)
    oled.show()
    sleep_ms(20)
    j += 1
