import socket
import threading
import actuatorControl
import constants

nc = constants.networkConstant()
jc = constants.joystickConstant()
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, nc.PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_clinet(conns, addr):
    print(f"[NEW connnection] {addr}")

    connected = True
    while(connected):
        # will not pass next line of code unless we recieve a msg
        msg_length = conns.recv(nc.MSG_FORMAT).decode(nc.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conns.recv(msg_length).decode(nc.FORMAT)
            print(f"[{addr}] {msg}")
            if msg == nc.DISCONNECT_MSG:
                connected = False
            else:
                recv_data = int(msg) 
                recv_data = f'{recv_data:08b}'
                read_msg(recv_data)

    conns.close()

def start():
    server.listen()
    print(f" server listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        # creating a new thread with target function hadle and passing args
        thread = threading.Thread(target=handle_clinet, args=(conn, addr)) 
        thread.start()
        print(f"[Active connections] {threading.activeCount()-1}")

def read_msg(msg):
    print(f"** recv msg {int(msg)}")
    dir = "STOP"
    ## Check if any valid bit is set
    if (int(msg) & 127):
        acc = int((msg)[jc.BUTTON_ACC])
        rev = int((msg)[jc.BUTTON_REV])
        left = int((msg)[jc.BUTTON_LEFT])
        right = int((msg)[jc.BUTTON_RIGHT])
        rotate_left = int((msg)[jc.BUTTON_ROTL])
        rotate_right = int((msg)[jc.BUTTON_ROTR])
        if(acc):
            dir = "up"
        elif(rev):
            dir = "back"
        elif(left):
            dir = "left"
        elif(right):
            dir = "right"
        elif(rotate_left):
            dir = "rotate_left"
        elif(rotate_right):
            dir = "rotate_right"
    else:
        print("Stop!")
    
    motor.movement_auto(dir)

print(f" Starting Server .... ")
motor = actuatorControl.actuator()
motor.setup_gpio()
start()

