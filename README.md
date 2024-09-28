# Usefull scripts for PEN-300

Upon preparing for my PEN-300 exams, I created different scripts to help me out. Below you can find them

## encode_payload.py
I created this script in order to encode payloads via ROT or XOR. The course material directs you to use the `helper` app created via C#, but I found a Python script much, much easier. Usage:

```
encode_payload.py -t / --type <vb or csharp) -b / --bytes <ROT or XOR value> -o / --output <outfile> -e / --encryption <rot or xor> input file
```

The code is not done yet. For C# only the XOR-encoding has been created and I'm sure the code can be optimised. But for now, the VisualBasic works great and includes a decryption algorithm as well for ease of use, so you can copy/paste it straight into the your macro. The XOR on C# works great as well and incldues a decryption routine. 

### Example: XOR C-Sharp payload
```
$ python3 ./encode_payload.py -t csharp -b 170 -o rev-serviio-xor.cs -e xor rev-serviio.cs
[-] CSharp mode
[-] Converting rev-serviio.cs to rev-serviio-xor.cs, XOR-ring with 0xAA.
[+] Conversion done. Payload size: 789 bytes.
```

