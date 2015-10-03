from random import sample
from string import ascii_lowercase, ascii_uppercase, digits

words = ascii_uppercase + ascii_lowercase + digits


def get_name():
    return ''.join(sample(words, 7))


def main():
    print(get_name())

if __name__ == '__main__':
    main()
