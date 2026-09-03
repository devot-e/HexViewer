from math import log,ceil
import os
import sys
import subprocess
import shutil
import curses
from curses import panel,has_key,textpad
import argparse
# window = curses.initscr()
# window.get


flagCapturer=argparse.ArgumentParser(description="Hexadecimal viewer")
flagCapturer.add_argument("file", type=str, help="Path to the file to be viewed")
flagCapturer.add_argument("--offset", type=int, default=0, help="Starting offset in bytes (default: 0)")
flagCapturer.add_argument("--rows", type=int, default=200, help="Number of rows to display (default: 20)")
flagCapturer.add_argument("--bytes", type=int, default=8, help="Number of bytes per row (default: 8)")
flagCapturer.add_argument("--ascii", type=int, default=1, help="ASCII visibility (1 for visible, 0 for hidden, default: 1)")
flagCapturer.add_argument("--search-hex",type=str, help="pass hexadecimal stream to search in file")
flagCapturer.add_argument("--search-ascii",type=str, help="pass ascii stream to search in file")
flagCapturer.add_argument("--info",action="store_true",help="print file info and exit")
flagCapturer.add_argument("--interactive",action="store_true",help="interactive mode")
args = flagCapturer.parse_args()

file_loc=args.file
starting_offset = args.offset
number_of_row = args.rows
bytes_per_row = args.bytes
ASCII_visibility = args.ascii

file_size=os.path.getsize(file_loc) #in Bytes
file_type=''
for i in range(len(file_loc),0,-1):
    if(file_loc[-i]=='.'):
        file_type=file_loc[-i+1:]
        break
fileExt_type={
    'Portable document':['.pdf'],
    'Text file':['.txt'],
    'Binary file':['.bin'],
    'Pictures':['.jpeg','.jpg','.svg'],
    'Markdown':['md']
}
for i in fileExt_type:
    if(file_type in fileExt_type[i]):
        file_type=i
        break

file_checksum=subprocess.getoutput(f'sha256sum {file_loc}').split()[0]

NumberOfByte=file_size
sizeDict={0:"Bytes",1:"KB",2:"MB",3:"GB",4:"TB"}
sizeUnit=0
for i in range(5):
    if(NumberOfByte<1000):
        break
    else:
        NumberOfByte/=1000
        sizeUnit=i+1
file_size=f"{NumberOfByte:.2f} {sizeDict[sizeUnit]}"

if(args.info==1):
    print(f"File Name:       {file_loc}")
    print(f"File Size:       {file_size}")
    print(f"File Type:       {file_type}")
    print(f"SHA256 Checksum: {file_checksum}")
    sys.exit(0)

w1 = max(ceil(log(number_of_row * 16, 16)), len("Offset"))
w2 = 3 * bytes_per_row
header = "{head1:<{w1}} {head2:<{w2}} {head3:<}"
line_format = "{Offset:0{w1}x} {Hex:<{w2}} {ASCII:<}"

print(header.format(head1="Offset", head2="Hex",head3="ASCII",w1=w1,w2=w2))

non_printable_bytes={
    0x0a:"\\n",
    0x0d:"\\r",
    0x09:"\\t",
    0x00:"."
}

hex_search=args.search_hex
ascii_search=args.search_ascii

# t_hex_search=""
# if(hex_search is not None):
#     for c in hex_search:
#         if c in "0123456789abcdefABCDEF":
#             t_hex_search+=c
#         else:
#             pass


if(hex_search is None and ascii_search is not None):
    hex_search=ascii_search.encode("utf-8").hex()

offset=-1
if (hex_search is not None):
    with open(file_loc, "rb") as f:
        data = f.read()
        if hex_search is not None:
            search_bytes = bytes.fromhex(hex_search)
            offset = data.find(search_bytes)

starting_offset = offset if offset != -1 else starting_offset

lines=[]

with open(file_loc, "rb") as f:
    for i in range(number_of_row):
        offset = starting_offset + i * bytes_per_row
        f.seek(offset)
        data = f.read(bytes_per_row)
        if not data:
            break
        hex_data = "".join("{:02x} ".format(byte) for byte in data)
        hex_data+='\t'
        ascii_data = ""
        if ASCII_visibility:
            for b in data:
                if 32<= b <= 126:
                    ascii_data += chr(b)
                elif b in non_printable_bytes:
                    ascii_data += non_printable_bytes[b]
                else:
                    ascii_data += "."
        # print(line_format.format(Offset=offset, Hex=hex_data, ASCII=ascii_data,w2=w2,w1=w1))
        lines.append(line_format.format(Offset=offset, Hex=hex_data, ASCII=ascii_data,w2=w2,w1=w1))

if(args.interactive):
    terminal_size = shutil.get_terminal_size((80, 20))
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    lines_per_page = terminal_height - 2  
    total_lines = len(lines)
    current_line = 0
    # os.system('clear')  
    # print(header.format(head1="Offset", head2="Hex",head3="ASCII",w1=w1,w2=w2))
    # for i in range(0, min(current_line + lines_per_page, total_lines)):
    #     print(lines[i])
    # current_line += lines_per_page    
    while current_line < total_lines:

        os.system('clear')  
        print(header.format(head1="Offset", head2="Hex",head3="ASCII",w1=w1,w2=w2))
        for i in range(current_line, min(current_line + lines_per_page, total_lines)):
            print(lines[i])
        current_line += lines_per_page
        if current_line < total_lines:
            input("Press Enter to continue...")
else:
    for line in lines:
        print(line)
