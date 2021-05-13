#!/usr/bin/env python3
import re
import argparse
import logging
import importlib
import json_serializer


dump = json_serializer.dump
dumps = json_serializer.dumps

logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source", type=str, help="Input python file with function for serialization"
    )
    parser.add_argument(
        "object_name", type=str, help="Name of function for serialization"
    )
    parser.add_argument("file", type=str, help="Output file for serialized object")
    parser.add_argument(
        "-p", "--print", action="store_true", help="Is printing to console"
    )

    args = parser.parse_args()

    args.source = re.sub(r"\.py$", "", args.source)
    module = importlib.import_module(args.source)
    func = getattr(module, args.object_name)

    dump(func, args.file)

    if args.print:
        line = re.sub(r'\s+',' ', dumps(func))
        logging.info(line)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.error("Stopped")