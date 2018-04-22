import requests
from xml.etree import ElementTree
from time import sleep
from datetime import datetime
from pytz import timezone
import os

### Configuration
#
# IP address of Wemo Insight
wemo_ip="192.168.1.80:49153"
# Directory where to store statistics
log_dir="/mnt/sda1/"

def get_power(ip_and_port):
    headers = {'Content-type': 'text/xml', 'SOAPACTION': '"urn:Belkin:service:insight:1#GetInsightParams"'}
    payload = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
                             s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                  <s:Body>
                   <u:GetInsightParams xmlns:u="urn:Belkin:service:insight:1"/>
                  </s:Body>
                 </s:Envelope>'''
    r = requests.post("http://{}/upnp/control/insight1".format(ip_and_port), headers=headers, data=payload)   
    et = ElementTree.fromstring(r.text)
    return int(et.find('.//InsightParams').text.split("|")[7]), float(et.find('.//InsightParams').text.split("|")[9])

def main():
    file_name="PWR"+datetime.now(timezone('UTC')).astimezone((timezone('US/Pacific'))).strftime("%Y-%m-%d")+".csv"
    with open(log_dir+file_name, "a+") as file:
        try:
            power, energy = get_power(wemo_ip)
        except:
            os.system("logger Error updating power-accounting log")
            return
        timeStamp = datetime.now(timezone('UTC')).astimezone((timezone('US/Pacific'))).strftime("%Y-%m-%d %H:%M:%S")
        logline = str(timeStamp) + "," + str(power) + "," + str(energy) + "\n"
        file.write(logline)
        os.system("logger Updated power-accounting log")

if __name__ =="__main__":
    main()
