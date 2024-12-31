from pwn import *

cnt = 0

while True:
    cnt += 1
    print(f'Try #{cnt}')
    r = remote('node1.anna.nssctf.cn', '28975')
    r.sendline('0')
    r.sendline('[]')
    r.recvuntil('hex format!')
    r.interactive()
    r.close()