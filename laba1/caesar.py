#!/usr/bin/env python3
import sys
import string
import io
import argparse
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="%(message)s")


@contextmanager
def file_context(file_name, method):
    try:
        file = io.open(file_name, method)
        yield file
        file.close()
    except OSError:
        logging.error("no such file")
        sys.exit()


def file_cipher(
    file_name, output_file_name, key=3, decrypt=False, characters=string.ascii_lowercase
):
    if decrypt:
        key = len(characters) - key

    table = str.maketrans(characters, characters[key:] + characters[:key])

    with file_context(file_name, "r") as f_in:
        with file_context(output_file_name, "w") as f_out:
            for line in f_in:
                new_line = str.lower(line).translate(table)
                f_out.write(new_line)

    logging.info(
        "The file %s has been translated successfully and saved to %s",
        file_name,
        output_file_name,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Input file for ecnrypting")
    parser.add_argument(
        "output_file", type=str, help="Output file for encrypted output"
    )
    parser.add_argument("-k", "--key", type=int, default=3, help="Key for encryption")
    parser.add_argument(
        "-d", "--decrypt", action="store_true", help="Is decrypting file"
    )

    args = parser.parse_args()

    file_cipher(args.input_file, args.output_file, args.key, args.decrypt)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.error("Stopped")
