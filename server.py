import socket
from _thread import *


def threaded(client_socket, addr):
    # 함수안에서 전역변수를 사용하려면 global 키워드를 이용해 명시적으로 불러주세요 ex) global data_store
    print('Connected by :', addr[0], ':', addr[1])
    # 3333333
    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:

        try:
            # socket 서버 데이터 받는거
            data = client_socket.recv(1024)  # data example : login admin 1234

            # 받는다고 받았는데 data가 없으면 걍 연결 끊어버리는거지
            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            # 받으면 한번 표시해보고
            print('Received from ' + addr[0], ':', addr[1], data.decode())

            # 자르고
            split_data = data.decode().split(' ')
            print(split_data)    # split_data example : ['login', 'admin', '1234']
            # 맨앞에꺼 opcode
            op = split_data[0]

            # 4444444 여기서부터 로직 짜면됨
            if op == 'register':
                print('register operation')
            elif op == 'login':
                print('login operation')
                # 로그인 해보고 맞으면 ok 다르면 fail
                # 형식을 맞춰주기 위해서 str.encode('여기 쓰고싶은말 써야됨')
                client_socket.send(str.encode('ok'))
                client_socket.send(str.encode('fail'))

        # 연결 리셋 에러
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


# 접속할 서버 주소임
HOST = '127.0.0.1'
PORT = 9898

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
# 1111
server_socket.listen()

#자료형은 여기다 선언하는걸 추천, 파일입출력 쓰려면 로드하는부분도 여기서 짜는걸 추천

while True:
    try:
        print('server is listning')

        client_socket, addr = server_socket.accept()
        # 22222
        start_new_thread(threaded, (client_socket, addr))

    except KeyboardInterrupt:
        # 이거 키보드 ctrl+d
        server_socket.close()
