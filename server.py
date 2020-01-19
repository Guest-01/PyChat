import socket
import threading
import argparse
import datetime

IP = '127.0.0.1'
PORT = 5656  # Default
ADDR = (IP, PORT)  # tuple for arg

user_list = {}

def msg_to_all(msg):
    dt = datetime.datetime.now()
    print(f'{dt.strftime("%Y-%m-%d %H:%M:%S")} {msg}')
    for user, conn in user_list.items():
        try:
            conn.sendall(msg.encode())
        except:
            print(f'비정상적으로 종료된 소켓: {user}, {conn}')

def handle_receive(sock, user):
    msg_to_all(f'-----{user}님이 들어오셨습니다.------')
    while True:
        data = sock.recv(1024)
        msg = data.decode('utf-8')
        if msg == 'exit':
            del user_list[user]
            msg_to_all(f'----{user}님이 나가셨습니다----')
            break
        msg_to_all(f'{user}: {msg}')
    sock.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyChat Args')
    parser.add_argument('-p', type=int, help='PORT', default=5656)
    args = parser.parse_args()
    PORT = args.p

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)

    server.listen()

    while True:
        try:
            conn, addr = server.accept()
        except KeyboardInterrupt:
            for user, con in user_list.items():
                con.close()
            server.close()
            print('Keyboard Interrupt')
            break
        else:
            print(f'{addr} connected!')

        user = conn.recv(1024).decode('utf-8')
        user_list[user] = conn

        recv_thread = threading.Thread(target=handle_receive, args=(conn, user))
        recv_thread.daemon = True
        recv_thread.start()