# Connect to wireless network as client
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("itcollege")

# Synchronize clock
import ntptime
ntptime.settime()

# Create a variable for hostname based on MAC address:
import ubinascii as binascii
name = "esp-%s" % binascii.hexlify(wlan.config("mac")[-3:]).decode("ascii")

# Clean up
import gc
gc.collect()
