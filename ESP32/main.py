import usocket as socket
import utime as time
from machine import Pin, PWM
import sys


essid = 'SSID'
essid_password = 'PASSWORD'


from nettools import wlan_connect,wlan_disconnect

try:
    wlan_connect(essid,essid_password,timeout=15)
except:
    print('Failed to connect to WiFi')

HOST = '0.0.0.0'  
PORT = 18000        
time.sleep(2)



def DataReceive(conn):
    
    while True:
        data = conn.recv(1024)
        if not data:
            return None
        return data


def DataAnalyzer(data):
    if data.decode() == "commande":
        try:
            ActionManager()
        except:
            return False
    return 'Done'


def ActionManager():
    #Cleaning process
    cycle = 0
    max = 0 #A remplacer par la longueur du bras le long de la table
    for cycle in range(0, max):
        PWM(Pin(15)).duty(cycle)
    return None


    
def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((HOST, PORT))
        s.listen(1)
        print("Waiting for connexion")
        conn, addr = s.accept()
        print('Connected by', addr)

        data = DataReceive(conn)
        if DataAnalyzer(data) == False:
            print("An error occured")
            break
        conn.sendall(b'Done')
        s.close()

   
def alert():
    sys.exit()

main()