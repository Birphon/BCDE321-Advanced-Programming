from re import A
import sys
from Commands import Commands


if __name__ == "__main__":
    print("Number of command-line arguments: ", len(sys.argv))
    print(sys.argv[0])
    commands = Commands()
    commands.cmdloop()
