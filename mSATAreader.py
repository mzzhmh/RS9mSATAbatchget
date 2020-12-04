#!/usr/bin/python3.6
from easysnmp import Session
import re
import pprint
import requests
import sys
import time

class mSATAreader(object):
    def __init__(self):
        self.siteMap={}
        self.debugf=None

    def readInput(self,inputfile):
        self.debugf=open('debug.log','w')
        with open(inputfile) as ifile:
            itemList=[]
            site=""
            self.siteMap={}
            for line in ifile:
#               print(line)
                r1 = re.search(r'TD.*TH(V|U)',line)
                if r1 != None:
                    deviceName=line.split("><")[2].split(">")[1].split("<")[0]
                    #print(deviceName)
                    deviceIP=line.split("><")[5].split(">")[1].split("<")[0]
                    #print(deviceIP)
                    tmpList=[deviceName,deviceIP]
                    itemList.append(tmpList)
                r2 = re.search(r'<Type dt:dt="ui4">1<\/Type>',line)
                if r2 != None:
                    siteName=line.split("><")[2].split(">")[1].split("<")[0]
                    if(len(itemList)>0):
                        self.siteMap[siteName]=itemList
                        itemList=[]

    def printMap(self):
        pprint.pprint(self.siteMap)

    def getmSATA(self):
        print("Site,TX Name,IP Address,mSATA Label")
        for site, devices in self.siteMap.items():
            for device in devices:
                print("#####################",file=self.debugf)
                print(site+","+device[0]+","+device[1],file=self.debugf)
                #get the snmp values
                IP=(device[1])[7:]
                print(IP,file=self.debugf)

                try:
                    #get the mSATA info
                    mSATA = "NOT FOUND"
                    url="http://"+IP+"/diaggui/cgi-bin/index.cgi"
                    print(url,file=self.debugf)
                    #post login
                    payload = {'rsdiaggui_password':loginpw,'submit.x':'62','submit.y':'33'}
                    headers = {'Content-Type': 'text/plain'}
                    r = requests.post(url, data=payload, headers=headers, timeout=5)
                    respStr = r.text
                    print(respStr,file=self.debugf)
                    rlines = respStr.split('\n')
                    #find mSATA
                    for rline in rlines:
                        #print(rline)
                        inx = rline.find('mSATA')
                        if (inx > -1):
                            mSATA=rline.strip().split(',')[0].split(' ')[6]

                    print(site+","+device[0]+","+device[1]+","+mSATA)
                    print(site+","+device[0]+","+device[1]+","+mSATA,file=self.debugf)
                except Exception as e:
                    print(site+","+device[0]+","+device[1]+","+str(e))
                    print(site+","+device[0]+","+device[1]+","+str(e),file=self.debugf)
                print("#####################",file=self.debugf)
                self.debugf.flush()
            time.sleep(30)
    
if __name__ == "__main__":
    myreader=mSATAreader()
    myreader.readInput("THVU9.txt")
    #myreader.printMap()
    myreader.getmSATA()
