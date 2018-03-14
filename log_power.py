import requests
from xml.etree import ElementTree
from time import sleep
import datetime

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
    return et.find('.//InsightParams').text.split("|")[7]

def main():
    with open("powerlog.csv", "a+") as file:
        while True:
            power = get_power("192.168.11.102:49153")
            timeStamp = datetime.datetime.now()
            logline = str(timeStamp) + "," + str(power) + "\n"
            file.write(logline)
            print(logline, end="")
            sleep(1)

if __name__ =="__main__":
    main()