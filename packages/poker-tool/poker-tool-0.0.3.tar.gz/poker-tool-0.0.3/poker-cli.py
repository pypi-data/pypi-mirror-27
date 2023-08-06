#! /usr/bin/env python3

import argparse

from poker.packer import Packer

def main(tasks_file, compressed_to):
    p = Packer(tasks_file)
    collection_path = p.collect()
    compressed_path = p.compress(compressed_to)

    print("The files be collected in ", collection_path)
    print("And compressed into ", compressed_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks_file")
    parser.add_argument("-o", dest="compressed_to", help = "The compressed file path.")
    args = parser.parse_args()
    main(args.tasks_file, args.compressed_to)