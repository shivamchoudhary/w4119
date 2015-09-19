def read_password(filename = 'user-pass.txt'):
    with open('user_pass.txt','r') as f:
        a = f.read()
        print a

read_password()
