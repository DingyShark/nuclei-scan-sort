import sys
from urllib.parse import urlparse
from colorama import Fore, Style, init
from argparse import ArgumentParser


def sort_by_url(scan_results):
    try:
        return sorted(scan_results, key=lambda x: x.split(" ")[3])
    except IndexError:
        # Check if scan file is valid
        print(Fore.RED + 'Not valid Nuclei Scan format' + Style.RESET_ALL)
        sys.exit(1)


def sort_by_severity(scan_results):
    severity_order = {'[critical]': 1, '[high]': 2, '[medium]': 3, '[low]': 4, '[info]': 5, '[unknown]':6}
    return sorted(scan_results, key=lambda x: severity_order[x.split(" ")[2]])


def sort_by_all(scan_results):
    unique_domains = {}
    sorted_results = []
    sorted_by_url = sort_by_url(scan_results)

    for i in sorted_by_url:
        # Find all urls
        parts_of_url = urlparse(i.split(" ")[3])
        domains = []
        # Add to "domains" list parts of url without http:// or https://
        if parts_of_url.netloc != '':
            domains.append(parts_of_url.netloc)
        else:
            domains.append(parts_of_url.path)
        # Create new list to split all unique domains
        for domain in domains:
            if domain not in unique_domains:
                unique_domains[domain] = [i]
            else:
                unique_domains[domain].append(i)

    # Sort by severity for all unique domains
    for i in unique_domains.values():
        by_severity = sort_by_severity(i)
        # Add delimiter between different domains
        by_severity[-1] += '\n'
        for j in by_severity:
            sorted_results.append(j)

    return sorted_results


def main(input_file):
    garbage_info = []
    # Read file with nuclei scan and append to the list
    with open(input_file, 'r') as file:
        scan_results = [result.strip() for result in file.readlines()]

    for i in scan_results:
        # Check if there is garbage information in [INF] brackets
        if i.split(" ")[0] == '[INF]':
            # Append it to "garbage_info" list and remove from original one
            garbage_info.append('Garbage: ' + i)
            scan_results.remove(i)
            print(garbage_info)
        else:
            continue

    # Identify the color of each severity
    color_map = {
        '[critical]': Fore.MAGENTA,
        '[high]': Fore.RED,
        '[medium]': Fore.YELLOW,
        '[low]': Fore.GREEN,
        '[info]': Fore.CYAN,
        '[unknown]': Fore.WHITE
    }

    # Sort by severity and URL and split the list
    results = [i.split(" ") for i in sort_by_all(scan_results)]

    # Move [severity] to the first position, color with color_map and remove from original position
    for i in results:
        print(color_map.get(i[2]) + i[2] + Style.RESET_ALL + " " + " ".join(i).replace(i[2], ''))


if __name__ == '__main__':
    # Colorama function to color text in CMD
    init()
    # Available arguments(in CMD type -h for help)
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file with Nuclei scan: /home/kali/scan.txt', default='', required=True)
    args = parser.parse_args()

    # Check if file or path is valid and sort it
    if args.input != '':
        try:
            main(args.input)
        except FileNotFoundError:
            print(Fore.RED + '[!]  Not existing file or path' + Style.RESET_ALL)
    else:
        print(Fore.RED + '[!]  No input file was given' + Style.RESET_ALL)
        sys.exit(1)

