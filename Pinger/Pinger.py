from pythonping import ping
from colorama import init, Fore, Back, Style
from threading import Thread
import time
import os
import keyboard



class NetworkObject:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.connected = False
        self.ms = 0

scanning = True
quitting = False

def detectMode():
    global scanning
    global quitting
    while True:
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('s'):
                scanning = not scanning
            if keyboard.is_pressed('q'):
                quitting = True
                break
        except:
            break
    
def createNetworkObjectList(object_list):
    with open("ip") as f:
        line = f.read().splitlines()
    for attr in line:
        info = attr.split(',')
        object_list.append(NetworkObject(info[0], info[1]))

def pingThread(o):
    while(True):
        if(quitting):
            break
        if(scanning):
            response = ping(o.ip, count=5, timeout=4)
            o.connected = response.success()
            o.ms = response.rtt_avg_ms
            time.sleep(1)        

def pingNetworkObjects(obj):
    for i in range(len(obj)):
        Thread(target = pingThread, args=(obj[i],)).start()
        
def renderNetworkObjectsInfo(obj):
    init(autoreset=True)
    while(True):
        if(quitting):
            break
        if(scanning):
            os.system('cls')         
            print(Back.CYAN + Style.BRIGHT + '{:<18}  {:<15}  {:<10} {:<8}'.format("IP", "DEVICE", "STATUS", "MS"))
            for i in range(len(obj)):
                if obj[i].connected:
                    print(Back.GREEN + '{:<18}  {:<15}  {:<10} {:<8}'.format(obj[i].ip, obj[i].name, "Online", obj[i].ms))
                else:
                    print(Back.RED + '{:<18}  {:<15}  {:<10} {:<8}'.format(obj[i].ip, obj[i].name, "Offline", obj[i].ms))
            time.sleep(1)
        

def main():
    network_objects = []
    createNetworkObjectList(network_objects)    
    pingNetworkObjects(network_objects)
    Thread(target=renderNetworkObjectsInfo, args=(network_objects,)).start()
    detectMode()
    

if __name__ == "__main__":
    main() 
