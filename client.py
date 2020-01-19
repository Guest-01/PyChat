import socket
import argparse
import threading


def handle_receive(sock, user):
    while True:
        try:
            data = sock.recv(1024)
        except:
            print('연결끊김')
            break
        msg = data.decode('utf-8')
        if not user in msg:  # to not receive from self
            print(msg)

def handle_send(sock):
    while True:
        data = input('>>>')
        try:
            sock.sendall(data.encode())
            if data == 'exit':
                break
        except:
            print('연결끊김')
            break
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyChat Client Args')
    parser.add_argument('-i', help='host', default='127.0.0.1')
    parser.add_argument('-p', help='port', default=5656)
    args = parser.parse_args()

    IP, PORT = args.i, args.p
    ADDR = (IP, PORT)

    user = input('사용할 닉네임: ')
    
    client = socket.socket()
    client.connect(ADDR)

    client.sendall(user.encode()) # first send username

    recv_thread = threading.Thread(target=handle_receive, args=(client, user))
    recv_thread.daemon = True
    recv_thread.start()

    send_thread = threading.Thread(target=handle_send, args=(client,))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()
    recv_thread.join()
    print('connection closed')