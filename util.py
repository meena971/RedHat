import sys
import re


def print_help():
    help_text = """
    Usage: ./util.py [OPTION]... [FILE]
    Parse logs of various kinds.

    Options:
    -h, --help       Show this help message and exit
    --first N        Print the first N lines
    -l N, --last N   Print the last N lines
    --timestamps     Print lines that contain a timestamp
    --ipv4           Print lines that contain an IPv4 address
    --ipv6           Print lines that contain an IPv6 address
    """
    print(help_text)


def parse_lines(lines, option, value=None):
    if option == '--first' and value:
        for line in lines[:int(value)]:
            print(line.strip())
    elif option == '--last' and value:
        for line in lines[-int(value):]:
            print(line.strip())
    elif option == '--timestamps':
        for line in lines:
            if re.search(r"\b([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b", line):
                print(line.strip())
    elif option == '--ipv4':
        ipv4_pattern = "(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(?:[\.|\s])?"
        for line in lines:
            if re.search(ipv4_pattern, line):
                print(line.strip())
    elif option == '--ipv6':
        ipv6_pattern = r'\b(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|::|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}(([0-9]{1,3}\.){3,3}[0-9]{1,3})|([0-9a-fA-F]{1,4}:){1,4}:(([0-9]{1,3}\.){3,3}[0-9]{1,3}))\b'
        for line in lines:
            if re.search(ipv6_pattern, line):
                print(line.strip())


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    option = sys.argv[1]

    if option in ('-h', '--help'):
        print_help()
        return

    file = None
    value = None

    if option in ('--first', '-l', '--last'):
        if len(sys.argv) < 4:
            print(f"Error: Missing required value for option {option}")
            return
        value = sys.argv[2]
        file = sys.argv[3]
    else:
        if len(sys.argv) < 3:
            print(f"Error: Missing required file argument for option {option}")
            return
        file = sys.argv[2]

    try:
        with open(file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {file} not found")
        return

    parse_lines(lines, option, value)


if __name__ == "__main__":
    main()