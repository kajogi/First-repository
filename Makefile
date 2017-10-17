NAME=esp8266-20170612-v1.9.1.bin

deploy:
	wget -c http://micropython.org/resources/firmware/${NAME}
	esptool.py -p /dev/ttyUSB0 -b 460800 erase_flash
	esptool.py -p /dev/ttyUSB0 -b 460800 write_flash 0 ${NAME}
	sleep 5
	ampy -p /dev/ttyUSB0 put main.py 
	ampy -p /dev/ttyUSB0 put boot.py 
	echo "Press now reset to start the scripts"
	picocom -b115200 /dev/ttyUSB0

console:
	echo "Press Crtl-A and than Crtl-Q to hang up picocom!"
	picocom -b115200 /dev/ttyUSB0
