import sys
import argparse

def throw_error(message):
    print (f"Error: {message}\nQUITTING!")
    exit(1)

def process_vba(args):
    print (f"[-] Visual Basic mode")
    filename = args.filename
    outfile = args.output
    enctype = args.encryption
    print (f"[-] Converting {filename} to {outfile}, ", end='')
    if (enctype == 'rot'):
    	print (f"rotating {args.bytes} bytes.")
    elif (enctype == 'xor'):
    	print (f"XOR-ring with 0x{args.bytes:02X}.")
    try:
        file = open(filename)
        infile = file.read()
        file.close()
    except (OSError, IOError) as e:
        throw_error(e)
    
    # Write output file to disk
    try:
        file = open(outfile, "wb")
        start = infile.find('(')
        if (start == -1):
            throw_error('Error: No ( found in vb file to indicate start of bytes')
        b=''
        written=0
        charswritten=0
        file.write(b'buf = Array(')
        for i in range (start, len(infile)):
            if ((infile[i] >= '0') and (infile[i] <= '9')):
                b += infile[i]
                charswritten += 1
            if ((infile[i] == ',') or (infile[i] == ')')):
                # indicates next byte; complete this one
                written += 1
                num = int(b)
                if (enctype == 'rot'):
                	num += args.bytes
                elif (enctype == 'xor'):
                	num = num ^ args.bytes
                num = num % 256
                file.write(str(num).encode('utf-8'))
                if (infile[i] == ','):
                    file.write(b',')
                    charswritten += 1
                elif (infile[i] == ')'):
                    file.write(b')')
                    charswritten += 1
                    break
                b=''
                if (charswritten > 150):
                    file.write(b' _\n')
                    file.write(b'            ')
                    charswritten -= 150
        # Write decryption algorithm as well for easy use
        if (enctype == 'rot'):
        	file.write(b'\n\nFor i = 0 to UBound(buf)\n')
        	file.write(b'    buf(i) = buf(i) - ' + str(args.bytes).encode('utf-8'))
        	file.write(b'\nNext i')
        elif (enctype == 'xor'):
        	file.write(b'\n\nFor i = 0 to UBound(buf)\n')
        	file.write(b'    buf(i) = buf(i) Xor ' + str(args.bytes).encode('utf-8'))
        	file.write(b'\nNext i')
        file.close()
        print (f"[+] Conversion done. Payload size: {written} bytes.")
    except (OSError, IOError) as e:
        throw_error(e)

    return

def process_csharp(args):
    print (f"[-] CSharp mode")
    filename = args.filename
    outfile = args.output
    enctype = args.encryption
    print (f"[-] Converting {filename} to {outfile}, ", end='')
    if (enctype == 'rot'):
        throw_error('Sorry, not implemented yet...')
    elif (enctype == 'xor'):
    	print (f"XOR-ring with 0x{args.bytes:02X}.")
    try:
        file = open(filename)
        infile = file.read()
        file.close()
    except (OSError, IOError) as e:
        throw_error(e)
    
    # Write output file to disk
    try:
        file = open(outfile, "wb")
        start = infile.find('{')
        if (start == -1):
            throw_error('Error: No { found in cs file to indicate start of bytes')
        b=b''
        written=6 # First line only 6 byte
        charswritten=0
        output = b''
        # file.write(b'byte[] buf = new byte [] {')
        for i in range (start, len(infile)):
            if ((infile[i] == ',') or (infile[i] == '}')):
                # found a byte, XOR the shit out of it.
                actual_byte = bytes([int(b.decode()[2:], 16)])
                result = actual_byte[0] ^ args.bytes
                rb = f'0x{result:02x}'
                output += rb.encode('utf-8')
                if (infile[i] == ','):
                    output += b','
                elif (infile[i] == '}'):
                    output += b'};'

                written+=1
                if (written % 12) == 0:
                    output += b'\n'
                b = b''
            elif ((infile[i] == '{') or (infile[i] == '\n')):
                # ignore these bytes
                b = b
            else:
                b += infile[i].encode('utf-8')
        written -= 6 #correction for earlier indent.
        file.write(b'byte[] buf = new byte[' + str(written).encode('utf-8') + b'] {')
        file.write(output)

        # Write decryption algorithm as well for easy use
        if (enctype == 'rot'):
        	file.write(b'\n\nFor i = 0 to UBound(buf)\n')
        	file.write(b'    buf(i) = buf(i) - ' + str(args.bytes).encode('utf-8'))
        	file.write(b'\nNext i')
        elif (enctype == 'xor'):
            file.write(b'\n\n\n')
            file.write(b'// Decodoing routine\n')
            file.write(b'byte [] result = new byte[buf.Length];\n')
            file.write(b'for (int i = 0; i < buf.Length; i++) \n')
            file.write(b'{\n')
            file.write(b'\tresult[i] = (byte)(buf[i] ^ ' + str(args.bytes).encode('utf-8') + b');\n')
            file.write(b'}\n')
            
        file.close()
        print (f"[+] Conversion done. Payload size: {written} bytes.")
    except (OSError, IOError) as e:
        throw_error(e)
    return

def main():
    parser = argparse.ArgumentParser(prog='encode_rot.py', 
        description='This program applies ROT (Caesar) or XOR encryption to payloads generated by msfvenom. This greatly increases my flexibility while preparing for Offensive Securitys PEN-300 exam',
        epilog='I found a python script easier than the C# solution from the learning guide.')
    parser.add_argument('filename')
    parser.add_argument('-t', '--type', required=True, help='Specifies file type. Choices are: vb, csharp')
    parser.add_argument('-b', '--bytes', type=int, required=True, help='Specifies the number of bytes to rotate or the byte to XOR with (integer, decimal)')
    parser.add_argument('-o', '--output', required=True, help='Specifies the output file name')
    parser.add_argument('-e', '--encryption', required=True, help='Specifies encryption scheme. Choices are: xor, rot')
    args = parser.parse_args()

    ftype = args.type.lower()
    enctype = args.encryption.lower()

    if ((ftype != 'vb') and (ftype != 'csharp')):
        throw_error ("Unknown file type specified. Options are: vb, csharp. You specified " + ftype)

    if ((enctype != 'xor') and (enctype != 'rot')):
        throw_error ("Unknown encryption scheme. Options are: rot, xor")

    if ftype == 'vb':
        process_vba(args)
    elif ftype == 'csharp':
        process_csharp(args)
    else:
        throw_error ("How did you get here?\nUnknown file type specified. Options are: vb, csharp")


    return

if __name__ == "__main__":
    main()
