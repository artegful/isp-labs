import logging
import argparse
from serializer import convert_file, dumps, loads

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main(*override_args):
    parser = argparse.ArgumentParser(
        description="Serialized file converter",
    )

    parser.add_argument("input", type=str, help="The path to the source file")
    parser.add_argument(
        "-i",
        "--ilang",
        metavar="ilang",
        type=str,
        default="",
        help="Markup language for source file",
    )
    parser.add_argument("output", type=str, help="The path to the new file")
    parser.add_argument(
        "-o",
        "--olang",
        metavar="olang",
        type=str,
        default="",
        help="Markup language for new file",
    )

    args = parser.parse_args(*override_args)

    try:
        convert_file(**vars(args))
    except (ValueError, IOError) as error:
        logging.error(error)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("The program was interrupted by user")
