# Usefull scripts for PEN-300

Upon preparing for my PEN-300 exams, I created different scripts to help me out. Below you can find them

## encode_payload.py
I created this script in order to encode payloads via ROT or XOR. The course material directs you to use the `helper` app created via C#, but I found a Python script much, much easier. Usage:

```
encode_payload.py -t / --type <vb or csharp) -b / --bytes <ROT or XOR value> -o / --output <outfile> -e / --encryption <rot or xor> input file
```

The code is not done yet. C# is not implemented yet and I can optimise the code. But for now, the VisualBasic works great and includes a decryption algorithm as well for ease of use, so you can copy/paste it straight into the your macro.

