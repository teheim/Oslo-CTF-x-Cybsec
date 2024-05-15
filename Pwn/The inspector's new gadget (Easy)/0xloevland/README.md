# The inspector's new gadget

<p align="center">
<img src="./utils/the_inspectors_new_gadget.png" alt="Challenge" width="500"/>
</p>

Connecting to the remote instance with `netcat` we are given some of the [source code](./utils/program.c) for the challenge. We are also given the goal of the challenge, and some options to interact with the program.

```
Your goal is to overwrite the saved return address with a "pop rdi" gadget.
The value popped into rdi should be 0x1337 (hint: use p64()).
The gadget is located at 0x4038db
Use the "Verify ROP chain" menu option to get the flag.

Google these terms for help:
- return oriented programming (ROP)
- ROP gadgets

Good luck!

1. Fill buffer
2. Print stack frame
3. Verify ROP chain
4. Print challenge description
5. Print gadgets
6. Lookup symbol
7. Add string
8. [Quit]
>
```

A quick summary of the menu options:
- `1` Write data to a buffer
- `2` Print the stack frame
- `3` Checks if our payload fulfills the requirements to get the flag.
- `4` Print the challenge description
- `5` Prints the address of some useful gadgets
- `6` Lets us look up the address of a symbol in the binary
- `7` Lets us add a string to the binary
- `8` Exits the program

This challenge is similar to the `did someone say ret2win?` challenge, but instead of overwriting the return address with the address of the `win` function, we will overwrite it with `gadgets`. Gadgets are snippets of assembly code from the binary, and does less than a function (e.g. changing values of registers or memory addresses). However, we can chain multiple gadgets together to perform operations as we want. For this challenge however, we are only required to set the value of the `rdi` register to `0x1337`. For this we will use the `pop rdi; ret;` gadget (shortened to `pop rdi`, because most gadgets will end with a `ret` instruction).

When using a `pop_rdi` gadget, the succeeding value in our payload on the stack will be popped into the `rdi` register. This means that the address of the `pop_rdi` gadget should be followed by the value we want to set the register to, `0x1337`. The address of the `pop_rdi` gadget is `0x4038db`, and we will use the `p64` function from pwntools to convert this address into the correct bytes-format. The setup for this exploit script is similar to the ret2win-challenge one, but with the address of the `pop_rdi` gadget and the value `0x1337` instead of `win`. Note that the offset for the padding for this challenge is 136 bytes instead of 120 (you can find this using the same method as previously, for example).

A commented exploit script can be found in [solve.py](./solve.py), which gives us the flag when run.

```console
$ python3 solve.py
[+] Opening connection to pwn.tokle.dev on port 1340: Done
[*] Switching to interactive mode
ROP chain looks good! Congrats, here's the flag: flag{greetings_inspector_gadget__}
```