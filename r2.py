from r2client.R2Client import R2Client as r2

import paho.mqtt.client as mqtt

import sys
import os
import subprocess
import time 


# Need setup yourself Cloudflare R2 Access.
client = r2(
    access_key='',
    secret_key='',
    endpoint=''
)


local_file_path = sys.argv[1]
name = local_file_path.split('/')[-1]
r2_file_key = str(sys.argv[2])+'.mp4'
bucket_name = sys.argv[3]
hevc = int(sys.argv[4])

# HEVC(H265) need call mp4box for iOS/macOS file convert.
if hevc == 1 :
    time.sleep(30)
	# MP4BOX Split sound / video track 
    subprocess.call('mp4box -raw 1 '+ local_file_path,shell=True)
    subprocess.call('mp4box -raw 2 '+ local_file_path,shell=True)
	# Path name for MP4BOX 
    local_file_path_hvc = local_file_path.replace('.mp4','_track1.hvc')
    local_file_path_hvc1 = local_file_path.replace('.mp4','-hvc1.mp4')
    local_file_path_aac2 = local_file_path.replace('.mp4','_track2.aac')
	# MP4BOX convert main process
    subprocess.call('mp4box -add '+local_file_path_hvc+' -add '+local_file_path_aac2 +' '+ local_file_path_hvc1,shell=True)
	# R2 Upload file
    client.upload_file(bucket_name, local_file_path_hvc1, r2_file_key)
	# Kill all transfer file
    os.remove(local_file_path_hvc)
    os.remove(local_file_path_hvc1)
    os.remove(local_file_path_aac2)
else:
    time.sleep(10)
	# R2 Upload file
    client.upload_file(bucket_name, local_file_path, r2_file_key)
    
# Remove original file for local disk space
os.remove(local_file_path)


# For backend notify file uploading 
# You can change to RESTFul API or other method to do this.
client = mqtt.Client()
client.username_pw_set("MQTT_USR","MQTT_PWD")

def on_connect(client,userdata,flags,rc):
    client.subscribe(bucket_name)

client.on_connect = on_connect
client.connect("MQTT_IP",21883,60)
client.publish('BROKER_SERVER_CHANNEL',str([bucket_name,'r2_upload_done',r2_file_key,'done']))
