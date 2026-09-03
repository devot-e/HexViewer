import curses
w = curses.initscr()
a=w.getkey()
b=w.getkey()
with open("output.txt", "a") as f:
    f.write(a)
    f.write(b)

def main(a):
    a.