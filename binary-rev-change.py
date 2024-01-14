import os
import argparse

verbose = 0
just_print = 0

bin_offset_990 = 0x20f

def parse_args():
    parser = argparse.ArgumentParser(description="change the binary version of Samsung firmware")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-p", "--print", action="store_true")
    parser.add_argument("filename", help="Filename (WITHOUT LZMA (NOT .LZ4))")
    parser.add_argument("target", help="Target binary revision")
    args = parser.parse_args()
    return args

def print_verbose(text):
    if verbose == 1:
        print(text)

def main():
    global verbose

    args = parse_args()

    if args.verbose == True:
        verbose = 1

    global just_print

    if args.print == True:
        just_print = 1
    
    fs = os.stat(args.filename)
    size = fs.st_size - 1
    print_verbose("Last byte offset: " + hex(size)) # calculate the offset of the last byte

    offset = int(size) - bin_offset_990
    print_verbose("REV offset: " + str(hex(offset)))

    print_verbose("Opening file...")
    fileptr = open(args.filename, "r+")

    fileptr.seek(int(offset))
    value = fileptr.read(1)
    if just_print == 1:
        print("BINARY REV: " + value.encode("utf-8").hex())
        return 0
    print_verbose("First revision: " + value.encode("utf-8").hex())

    if len(str(int(args.target,16))) == 1:
        toWrite = "0" + str(int(args.target,16))
    elif len(str(int(args.target,16))) == 2:
        toWrite = str(int(args.target,16))
    else:
        print("Invalid target value!")
        return -2

    byte_str = bytes.fromhex(toWrite) 
    regular_str = byte_str.decode('utf-8')  

    print_verbose("We are going to write " + regular_str.encode("utf-8").hex() + " to " + str(hex(offset)))

    fileptr.seek(int(offset))

    fileptr.write(regular_str)

    print("Wrote " + str(int(args.target, 16)) + " to " + str(hex(offset)) + ".")
main()