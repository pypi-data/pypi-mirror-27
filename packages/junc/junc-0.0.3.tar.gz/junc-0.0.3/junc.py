import clint
from clint import arguments

args = arguments.Args()

def cli():
    print("CLI!")
    user_in = input("Input: ")
    print(user_in)
    print(str(args))

if __name__ == '__main__':
    cli()
