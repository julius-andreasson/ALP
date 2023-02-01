# ALP (Assembly-Like Programming)

ALP is a minimal programming language, made for fun. It consists of basic assembly features, but also simple while-loops and if-statements.

The compiler in this repository compiles `.alp` (`assembly-like programming` source file) to machine code, made to run on our custom-made Micro-Controller Unit.

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
(Padded with 0000; according to the MCU programming software format.)
