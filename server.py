import socket
import select
import sqlite3

def broadcast(sock, message):
    for socket in sockets:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message.encode('utf-8'))
            except Exception as e:  # 客户端意外退出会出现此异常
                print(str(e) + 'aa')
                socket.close()
                sockets.remove(socket)


if __name__ == "__main__":
    # 数据库用来存放用户账号密码
    conn = sqlite3.connect("accounts.db")
    cs = conn.cursor()
    cs.execute(
        """
        create table if not exists accounts (
            account varchar(20) primary key,
            psw varchar(10)
        )
        """
    )
    
    sockets = []
    online = []
    sock_account = {}
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 6666))
    server_socket.listen()
    sockets.append(server_socket)
    print("聊天室服务器启动，端口 6666")

    while True:
        # 通过 select 模型，获取状态变化的 socket
        read_sockets, write_sockets, error_sockets = select.select(sockets, [], [])

        for sock in read_sockets:
            if sock == server_socket:   # 新连接
                sockfd, addr = server_socket.accept()
                sockets.append(sockfd)

            else:   # 某个客户端发信息
                try:
                    data = sock.recv(1024).decode('utf-8')
                    test = data.split('/')
                    if test[0] == 'reg':    # 用户在注册，发过来是的用户名和密码
                        cs.execute("select * from accounts")
                        result = cs.fetchall()
                        for i in result:
                            if i[0] == test[1]:  # 用户名重复
                                sock.send('fail_reg'.encode('utf-8'))
                                break
                        else:
                            cs.execute(
                                "insert into accounts (account, psw) values (?, ?)",
                                (test[1], test[2]),
                            )
                            conn.commit()
                            sock.send('true'.encode('utf-8'))
                            account = test[1]
                            sock_account[sock] = account
                            online.append(account)
                            print('【%s】注册成功！' % account)
                            broadcast(sock, "\r【服务器】 %s 进入聊天室\n" % account)

                    elif test[0] == 'login':    # 用户在登录，发过来的是用户名和密码
                        cs.execute("select * from accounts")
                        result = cs.fetchall()
                        if (test[1], test[2]) in result:
                            if test[1] in online:
                                sock.send('logon'.encode('utf-8'))
                                continue
                            sock.send('true'.encode('utf-8'))
                            account = test[1]
                            sock_account[sock] = account
                            online.append(account)
                            print("【%s】登陆成功！" % account)
                            broadcast(sock, "\r【服务器】 %s 进入聊天室\n" % account)
                        else:
                            sock.send('fail_login'.encode('utf-8'))
                    
                    elif data[-5:] == 'show\n':    # 显示在线用户
                        test = ''
                        for i in online:
                            test += i + '   ' 
                        sock.send("\r【服务器】 在线用户：{}\n".format(test).encode('utf-8'))
                        
                    elif test[0] == 'change':    # 修改用户名、密码
                        old_account = sock_account[sock]
                        cs.execute("delete from accounts where account=?", (old_account,))
                        conn.commit()
                        sock_account[sock] = test[1]
                        online.remove(old_account)
                        cs.execute("select * from accounts")
                        result = cs.fetchall()
                        for i in result:
                            if i[0] == test[1]:  # 用户名重复
                                sock.send('fail_reg'.encode('utf-8'))
                                break
                        else:
                            cs.execute(
                                "insert into accounts (account, psw) values (?, ?)",
                                (test[1], test[2]),
                            )
                            conn.commit()
                            sock.send('true'.encode('utf-8'))
                            online.append(sock_account[sock])
                            print('{}更名为{}成功！'.format(old_account, sock_account[sock]))
                            broadcast(sock, "\r【服务器】 {}已更名为{}\n".format(old_account, sock_account[sock]))
                        
  
                    else:   # 用户发信息
                        broadcast(sock, data)

                except Exception as e:
                    # Windows 下，有时突然关闭客户端，会抛出 "Connection reset by peer" 异常
                    broadcast(sock, ("\r【服务器】 %s 已离线！\n" % sock_account[sock]))
                    online.remove(sock_account[sock])
                    print("【%s】已离线" % sock_account[sock])
                    sock.close()
                    sockets.remove(sock)
                    del sock_account[sock]
                    continue

    server_socket.close()
