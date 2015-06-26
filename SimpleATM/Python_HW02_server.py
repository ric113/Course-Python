import socket, threading
 
HOST = ''
PORT = 54321
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
sock.bind((HOST, PORT))
sock.listen(4)
people = {}
lock = threading.Lock()
 
class TServer(threading.Thread):
    def __init__(self, socket, adr):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address= adr
    
    def run(self):
        global people
        print 'Client %s:%s connected.' % self.address
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                cont = data.split(":")
                ##print cont[0]
                ##print cont[1]
                if len(cont) > 1:
                    if cont[0] == "a":
                        if people.has_key(cont[1]) == False:
                            temp = {str(cont[1]):0}
                            people.update(temp)
                        self.socket.send(str(people[cont[1]]))  
                            
                    elif cont[0] == "d" or cont[0] == "w" or cont[0] == "t":
                        lock.acquire()
                        if cont[0] == "d":
                            people[cont[1]] += int(cont[2])
                            self.socket.send(str(people[cont[1]]))  
                            ##print people[cont[1]]
                        elif cont[0] == "w":
                            people[cont[1]] -= int(cont[2])
                            if people[cont[1]]<0:
                                people[cont[1]] += int(cont[2])
                                self.socket.send("n:"+str(people[cont[1]]))
                            else:
                                self.socket.send(str(people[cont[1]]))  
                            ##print people[cont[1]]
                        elif cont[0] == "t":
                            if people.has_key(cont[2]) == False:
                                temp = {cont[2]:0}
                                people.update(temp)
                            people[cont[1]] -= int(cont[3])
                            if people[cont[1]]<0:
                                people[cont[1]] += int(cont[3])
                                self.socket.send("n:"+str(people[cont[1]]))
                            else:
                                people[cont[2]] += int(cont[3])
                                self.socket.send(str(people[cont[1]]))  
                        lock.release()
                    print "(Account : balance) :"
                    print people
                      
                    
            except socket.timeout:
                break
        self.socket.close()
        print 'Client %s:%s disconnected.' % self.address
 
if __name__ == "__main__":
    while True:
        (client, adr) = sock.accept()
        TServer(client, adr).start()
