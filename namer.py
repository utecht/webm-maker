from random import sample
import json


with open("words.json") as f:
    words = json.load(f)


def get_name():
    return ''.join(sample(words, 3))


def main():
    print(get_name())

if __name__ == '__main__':
    main()
