# Shellen

## General
Shellen is an interactive shellcoding environment. If you want a handy tool to write shellcodes, then shellen may be your friend. Also, it can be used just as assembly/disassembly tool.

It uses [keystone](https://github.com/keystone-engine/keystone) and [capstone](https://github.com/aquynh/capstone) engines for all provided operations.

## Installing
Just clone this repo and see the chapter ```How to run```.
```sh
git clone https://github.com/merrychap/shellen.git
cd ./shellen
```
In the future it will be changed on ```pip```.

## How to run:
To run shellen just type the next in your terminal:
```sh
$ python3 main.py
```
There is ```help``` command inside the tool, that will explain almost everything.

## Features
Shellen was created for assembling and disassembling instructions, so there are two modes of using the tool: **asm** and **dsm** respectively. Of course, there are some other possibilities.

### Prompt
It also has a usefull prompt, displaying current mode and chosen architecture exactly for this mode. It looks as follows:
```
asm:x86_32 >
```
You can edit your input like you're typing in a terminal. Also, it has a history of commands (just type up arrow to see them).

To change current mode, enter ```asm``` or ```dsm``` in the prompt.
```
dsm:arm32 > asm

[+] Changed to asm (assembly) mode

asm:x86_32 > dsm

[+] Changed to dsm (disassembly) mode

dsm:arm32 > 
```

### Assembling
To assembly instuctions, type them separated by colons as follows:
```
asm:x86_32 > mov edx, eax; xor eax, eax; inc edx; int 80;
   [+] Bytes count: 7
       Raw bytes:  "\x89\xc2\x31\xc0\x42\xcd\x50"
       Hex string: "89c231c042cd50"
```
If your assembled bytes contain a null byte, then shellen will tell you about this.

### Disassembling
It works exactly as assembling. Type your bytes in the input prompt and see the result!
```
dsm:x86_32 > 89c231c042cd50
        0x00080000:     mov     edx, eax
        0x00080002:     xor     eax, eax
        0x00080004:     inc     edx
        0x00080005:     int     0x50
```

### Architectures
```asm``` and ```dsm``` modes work for different architectures. To see a list of available architectures for a current mode, type this:
```
dsm:x86_32 > archs
┌────────┬────────┬─────────┬─────────┬────────┐
│        │        │         │         │        │
│ arm32  │ mips32 │ sparc32 │ systemz │ x86_16 │
│ arm64  │ mips64 │ sparc64 │         │ x86_32 │
│ arm_tb │        │         │         │ x86_64 │
└────────┴────────┴─────────┴─────────┴────────┘
```

And if you want to change current architecture, enter follow:
```
dsm:x86_32 > setarch arm32

[+] Architecture of dsm changed to arm32
```

### Base commands
Command | Description
------- | -----------
```clear``` | Clear the terminal screen. As usual ```cls``` on Windows or ```clear``` on *nix systems.
```help``` | Show the help message.
```quit,q,exit``` | Finish the current session and quit


## Requirements
- [keystone](https://github.com/keystone-engine/keystone)
- [capstone](https://github.com/aquynh/capstone)
- [colorama](https://github.com/tartley/colorama)
- [termcolor](https://pypi.python.org/pypi/termcolor)
- [terminaltables](https://github.com/Robpol86/terminaltables)


## TODO
- [ ] Syscalls lists
- [ ] Database of common shellcodes

## Pictures
Just a little bunch of pictures

Example of using the tool.
<p align="center">
  <img src="screens/use.png">
</p>

Help screen.
<p align="center">
  <img src="screens/help.png">
</p>

Architecture tables.
<p align="center">
  <img src="screens/tables.png">
</p>
