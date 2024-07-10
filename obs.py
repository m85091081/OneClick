import os
import obsws_python as obs
import paho.mqtt.client as mqtt
import sys
import subprocess
import time 
import random
import string

obsid = "OBSPC_ID"
azid = "BROKER_SERVER_CHANNEL"
r2url = "R2_URL"
r2bucket = "R2_BUCKET_NAME"
hevc = "1" # 1 for yes other for no
host = 'OBSPC_HOST'
port = 4455

print("[OBS] Now is starting...")
print("[0muOBS] Config : " + host +':'+ str(port))

cl = obs.ReqClient(host=host, port=port, timeout=3)

print("[0muOBS] Connected.")
rs = cl.get_record_status()
rec = False
if rs.output_active:
    file = cl.stop_record()
    os.remove(file.output_path)

allow = []

def on_connect(client,userdata,flags,rc):
    client.subscribe(obsid)

def on_message(client,userdata,msg):
    global rec
    global allow
    msgq = msg.payload.decode('utf-8')
    msg = eval(msgq)
    try:
        if msg[0] == "obs_start":
			#["obs_start","ONE_CLICK_CLIENT",[Allow_ID]]
            client.publish(azid,str([obsid,'obs_resp_start',msg[1]]))
            client.publish(msg[1],str(['rec_ui_show']))
            rs = cl.get_record_status()
            if rs.output_active:
                file = cl.stop_record()
                os.remove(file.output_path)
            try:
                cl.start_record()
                allow = msg[2]
                rec = True
            except:
                rec = False
                client.publish(msg[1],str(['get_status']))
				pass
            
        elif msg[0] == "obs_stop":
			#["obs_stop","ONE_CLICK_CLIENT"]
            if rec :
                rec = False
                rnd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
                client.publish(azid,str([obsid,'obs_resp_stop',msg[1],allow,r2url+'.url.r2.self'+rnd+'.mp4']))
                time.sleep(1)
                client.publish(msg[1],str(['get_status']))
                file = cl.stop_record()
                try:
                    subprocess.Popen(['python','r2.py',file.output_path,rnd,r2bucket,hevc],close_fds=True,shell=True)
                except Exception as e:
                    print(e)
                    pass
					
        elif msg[0] == "obs_stop_wo_upload":
			#["obs_stop_wo_upload","ONE_CLICK_CLIENT"]
            if rec :
                rec = False
                client.publish(azid,str([obsid,'obs_resp_stop_wo_upload',msg[1]]))
                time.sleep(1)
                client.publish(msg[1],str(['get_status']))
                file = cl.stop_record()
                try:
                    subprocess.Popen(['python','removefile.py' ,file.output_path],close_fds=True,shell=True)
                except Exception as e:
                    print(e)
                    pass

    except Exception as e:
        print(e)
		pass
  


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("MQTT_USR","MQTT_PWD")
client.connect("MQTT_IP",21883,60)
client.loop_forever()
