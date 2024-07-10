X50 OneClick OpenSources 

req: OBS v30 / python 3.10 / obsws-python / paho.mqtt / r2client (for storage service)

support encode: HEVC / H264 

HEVC: You will need MP4Box convert HVC1 for macOS/iOS to preview mp4.




conn struct:

OBS PC <-MQTT-> OneClick Client <-MQTT-> DB(Broker) Server




recommand :

use "ESP32" build OneClick Client for process start/stop button and display .

use "RTOS" for ESP32 and async mqtt client to connect with all service.

use "Redis" and "DB" you like to make yourself backend and process preview for user download. 




I'll not plan to opensources myself Hardware client / DB Broker ^_^ .

If you just want copy and paste plase leave this repo.
