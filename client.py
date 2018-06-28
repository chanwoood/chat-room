import socket
from concurrent.futures import ThreadPoolExecutor
import string
import sys

def recvdata():
    while True:
        data = s.recv(1024).decode('utf-8')
        if data == 'true':
            print('修改成功！\n')
            sys.stdout.write('【我】 ')
            sys.stdout.flush()
            continue
        elif data == 'fail_reg':
            print('已存在用户！\n')
            sys.stdout.write('【我】 ')
            sys.stdout.flush()
            continue
        sys.stdout.write(data)
        sys.stdout.write('【我】 ')
        sys.stdout.flush()

def senddata():
    while True:
        msg = sys.stdin.readline()
        
        if msg == 'change\n':
            new_account = input('新账号：')
            new_psw = input('新密码：')
            s.send('change/{}/{}'.format(new_account, new_psw).encode('utf-8'))
            continue
        s.send(('\r【' + account + '】 ' + msg).encode('utf-8'))
        sys.stdout.write('【我】 ')
        sys.stdout.flush()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('107.175.115.87', 6666))
    except Exception:
        print('服务器还没开！')
        sys.exit()
    while True:
        choice = input('0.登陆     1.注册   请选择：    ')
        if choice == '0':
            account = input('账号：')
            psw = input('密码：')
            s.send('login/{}/{}'.format(account, psw).encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
            if data == 'true':
                print('登陆成功!\n\n ', end='')
                break
            elif data == 'fail_login':
                print('用户名不存在或密码有误！')
                continue
            elif data == 'logon':
                print('用户已登陆！')
                continue
            else:
                print(data)
        elif choice == '1':
            account = input('账号：')
            psw = input('密码：')
            s.send('reg/{}/{}'.format(account, psw).encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
            if data == 'true':
                print('注册成功!\n\n ', end='')
                break
            elif data == 'fail_reg':
                print('用户名已存在！')
                continue
            '''  
            elif choice == '2':
                account = input('原账号：')
                psw = input('原密码：')
                s.send('login/{}/{}'.format(account, psw).encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
                if data == 'true':
                    account = input('新账号：')
                    psw = input('新密码：')
                    s.send('reg/{}/{}'.format(account, psw).encode('utf-8'))
                    data = s.recv(1024).decode('utf-8')
                    if data == 'true':
                        print('更改成功!\n\n【我】 ', end='')
                        break
                    elif data == 'fail_reg':
                        print('用户名已存在！')
                        continue
                elif data == 'fail_login':
                    print('用户名不存在或密码有误！')
                    continue
            '''
        else:
            print('输入有误！')
            continue
    print('''
用法：
输入 show 显示当前所有在线用户
输入 change 更改用户信息
输入其他信息将会广播进行群聊
    ''')
    print('【我】 ', end='')
    executor = ThreadPoolExecutor(max_workers=4)
    fs = executor.submit(senddata)
    fr = executor.submit(recvdata)
