# ALP (Assembly-Like Programming)

This project aims to produce a simple compiler from `.alp` (`assembly-like programming` source file) to machine code, made to run on our custom-made Micro-Controller Unit.

The project is called `assembly-like programming` as it's made for coding on the instruction level, but we will not limit ourselves to features commonly found in assembly languages.

# Features
- Custom instruction names and codes
- Automatic conversion from decimal to binary
- Comments
- Label system for line jumps
- Output format is .hex, made to fit MCU programming software supplied by our university.

# Examples
An example:
```
LD R0 10
#Check
// If R0 == 0, goto End
BZ R0 #End
// Else, subtract one from R0
SUB R0 1
// goto #Check
B R0 #Check
#End
```
becomes
```
0C0A;
0404;
0A01;
0601;
0000;
0000;
0000;
...
0000;

```