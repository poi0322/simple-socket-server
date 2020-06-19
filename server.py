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
            print(split_data)  # split_data example : ['login', 'admin', '1234']
            # 맨앞에꺼 opcode
            op = split_data[0]

            # 4444444 여기서부터 로직 짜면됨
            if op == 'register':
                print('get register operation')
                member.append({'id': split_data[1], 'pw': split_data[2], 'name': split_data[3], 'score': 0})
                client_socket.send(str.encode('ok'))
            elif op == 'login':
                print('login operation')
                login_flag = False
                for m in member:
                    if m.id == split_data[1]:
                        if m.pw == split_data[2]:
                            client_socket.send(str.encode('ok'))
                            login_flag = True
                            break
                        else:
                            client_socket.send(str.encode('wrong password'))
                if not login_flag:
                    client_socket.send(str.encode('invalid id'))
            elif op == 'rank':
                for r in rank:
                    client_socket.send(str.encode(r.name+''+r.score+'\n'))
                client_socket.send(str.encode('rank end'))
            elif op == 'scoreUpdate':
                for i,m in enumerate(member):
                    if m.name == split_data[1]:
                        member[i].score = int(split_data[2])
                        rank.append({'name': split_data[1], 'score': int(split_data[2])})
                client_socket.send(str.encode('upt success'))

            saveAll()

        # 연결 리셋 에러
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


def saveAll():
    global rank
    rank = sorted(rank, key=lambda x: x['score'], reverse=True)
    w = open('data.db', mode='wt', encoding='utf-8')
    for m in member:
        w.write("member " + m.id + " " + m.pw + " " + m.name + " " + m.score + "\n")
    for r in rank:
        w.write('write ' + r.name + " " + r.score + "\n")
    w.close()


# 접속할 서버 주소임
HOST = '127.0.0.1'
PORT = 9898

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
# 1111
server_socket.listen()

member = []
rank = []

r = open('data.db', mode='rt', encoding='utf-8')
while True:
    line = r.readline()
    if not line:
        break
    if 'member' in line:
        data = line.split(' ')
        member.append({'id': data[1], 'pw': data[2], 'name': data[3], 'score': int(data[4])})
        print('member added ' + line, end='')
    elif 'rank' in line:
        data = line.split(' ')
        rank.append({'name': data[1], 'score': int(data[2])})
        print('rank added ' + line, end='')

rank = sorted(rank, key=lambda x: x['score'], reverse=True)
r.close()
print('file load finished')

print('members list')
for m in member:
    print(m)

print('')
print('ranks')
for r in rank:
    print(r)

print('------------------')
while True:
    try:
        print('server is listening')
        client_socket, addr = server_socket.accept()
        # 22222
        start_new_thread(threaded, (client_socket, addr))
    except KeyboardInterrupt:
        # 이거 키보드 ctrl+d
        print('exiting server')
        server_socket.close()
