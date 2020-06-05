import socket
import mysql.connector

try:
    mydb = mysql.connector.connect(
        user="script",
        password="script",
        database="Intermatiere",
        host="localhost"
    )
    mycursor = mydb.cursor()
except:
    print("Failed to connect to database")

PORT = 18000


######################################################################################################################
#                                               SQL INTERACTIONS


def C_New():
    sql = "SELECT * FROM commandes WHERE status = 'Debut' LIMIT 1"
    command = mycursor.execute(sql).fetchall()

    if command != []:
        id = command[0]
        C_Current(id)
    
        

def C_Current(id):
    sql = "UPDATE commandes SET status = 'EnCours' WHERE id = {}".format(id)
    R_Job(id)

    try:
        mycursor.execute(sql)

    except:
        R_Error("Problème lors de la connexion à la BDD C_Current", id)

def C_Success(id):
    sql = "UPDATE commandes SET status = 'Finie' WHERE id = {}".format(id)
    mycursor.execute(sql)


######################################################################################################################
#                                                ROBOTS INTERACTIONS

def R_Job(id):
    ip = SearchIP(id)

    try:
        DataSend(ip)
    
    except:
        R_Error("Problème lors du contact avec le robot", id)

def R_Error(error, id):
    sql = "UPDATE robot SET erreur = {} WHERE id = {}".format(error, id)
    mycursor.execute(sql)



######################################################################################################################
#                                               ID - IP MATCH
                                                
def SearchIP(id):
    f = open('IPList.txt', 'r+')
    for line in f:
        if str(id) in line and line[len(str(id))] == ':':
            return(line.split(':')[1])

######################################################################################################################
#                                               DATA MANAGER

def DataSend(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.connect((str(ip), PORT))
    s.sendall(str.encode('foo'))
    # reply = s.recv(1024)
    return None


def DataGrab():
    try:
        try:
            DataSend(str.encode("commande"))

        except:
            print("Request to ESP failed")
            return False
        
        query = "UPDATE commandes SET status = 'Terminee'"
        mycursor.execute(query)
        return False

    except:
        print("Query to database failed")
        return False

def main():
    while True:
        C_New()
        
main()

