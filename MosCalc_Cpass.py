import requests
import json


def calculateJitterMos1(jitter,ploss,rtt=0):
    if rtt==0:
        rtt=10
    latency=rtt+(jitter*2)+10
    mos_val=0
    r_factor=0
    if latency<160:
        r_factor=93.2 -(latency/40)
    else:
        r_factor=93.2 -(latency-120)/10
    r_factor=r_factor-(ploss*2.5)
    if r_factor >100:
        r_factor=100
    elif r_factor<0:
        r_factor=0
    mos_val=1+(0.035)*r_factor+(0.000007)*r_factor*(r_factor-60)*(100-r_factor)
    if mos_val>4.7:
        mos_val=4.7
    return mos_val
            
    
    
    
 #               if($rtt == 0) $rtt = 10;
  #              $effective_latency = $rtt + ($jitter * 2) + 10;
  #              $mos_val = 0;
  #              $r_factor = 0;
  #              if ($effective_latency < 160) {
  #                      $r_factor = 93.2 - ($effective_latency / 40);
  #              }
  #              else {
  #                      $r_factor = 93.2 - ($effective_latency - 120) / 10;
  #              }

#                 $r_factor = $r_factor - ($numpacketlost * 2.5);
#                 if ($r_factor > 100) $r_factor = 100;
#                 else if ($r_factor < 0) $r_factor = 0;
#                 $mos_val = 1 + (0.035) * ($r_factor) + (0.000007) * ($r_factor) * (($r_factor) - 60) * (100 - ($r_factor));

#                 if ($mos_val > 4.7) $mos_val = 4.7;
#                 return ($mos_val);




headers = {'Authorization': 'Basic U2FsZXNrZW46U0BhbDM0c3dmcldFYXNk'}
def getChannelId():
    
    ch=requests.get("http://35.194.53.75:8088/ari/channels",headers=headers)
    rtp1=getRtpStats(json.loads(ch.text)[0]["id"])
    rtp2=getRtpStats(json.loads(ch.text)[1]["id"])
#     rtt1=rtp1["rtt"]
#     rtt2=rtp2["rtt"]
    mos1=calculateJitterMos1(rtp1["txjitter"],rtp1["txploss"],rtp1["rtt"])
    mos2=calculateJitterMos1(rtp2["txjitter"],rtp2["txploss"],rtp2["rtt"])
    trtp={"UpMos":mos1,"DownMos":mos2}
    tmos=(trtp["UpMos"]+trtp["DownMos"])/2
    print(tmos)
    return tmos

def getRtpStats(ch_id):
    rtp=requests.get("http://35.194.53.75:8088/ari/channels/{}/rtp_statistics".format(ch_id),headers=headers)
    return json.loads(rtp.text)

    
getChannelId()