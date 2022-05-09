import hashlib
import requests

tempFile = "a.temp"
outFile = "block-all.txt"

def main():
    get_lists()
    remove_duplicates()


def get_lists():
    print("Downloading lists...")

    response = requests.get(
        "https://filterlists.com/api/directory/lists",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        )
    response.raise_for_status()
    lists = response.json()

    open(tempFile, "w").close()

    for list in lists:
        if find_maintainer(list["maintainerIds"]) and find_syntax(list["syntaxIds"]) and block_tags(list['tagIds']) and find_license(list["licenseId"]) and find_language(list["languageIds"]):
            print("Downloading list: " + list["name"])
            blob = requests.get(list['primaryViewUrl']).text.strip()
            with open(tempFile, "a", encoding="utf-8") as output_file:
                output_file.write(blob + "\n")

    print("Done!")

def remove_duplicates():
    print("Removing duplicates...")

    completed_lines = set()

    with open(outFile, "w", encoding="utf-8") as output_file:
        for lines in open(tempFile, "r", encoding="utf-8"):
            line = lines.rstrip()
            if not line.startswith(("!", "# ", "#	", "  ", "	", " 	", "[")):
                hash_value = hashlib.md5(line.encode('utf-8')).hexdigest()
                if hash_value not in completed_lines:
                    output_file.write(line + "\n")
                    completed_lines.add(hash_value)

    print("Done!")

def find_syntax(list):
    # https://filterlists.com/api/directory/syntaxes

    for id in list:
        if id in {
            3, # Adblock Plus
            4, # uBlock Origin Static
            6, # AdGuard
            17, # uBlock Origin scriptlet injection
            28, # Adblocker-syntax domains
            38, # Adblock Plus Advanced
        }:
            return True

def find_license(license):
    # https://filterlists.com/api/directory/licenses

    if license in {
        2, # The MIT License (MIT)
        6, # CC BY-NC-SA 3.0
        8, # CC BY-SA 4.0
        9, # CC BY-NC-SA 4.0
        10, # BSD-3-Clause
        11, # The Unlicense
        12, # CC BY-SA 3.0
        13, # CC BY-NC 4.0
        14, # WTFPL
        16, # CC BY 3.0
        17, # ISC
        18, # Apache 2.0
        20, # Public Domain
        23, # "Dont Be a Dick" Public License
        24, # CC BY 4.0
        27, # BSD-2-Clause
        28, # CC0 1.0 Universal
        32, # Permissive non-commercial
        33, # Mozilla Public License v2.0
        35, # Dandelicence
        37, # Lesser GPL v2.1
        38, # Generic copyfree
        40, # McRae General Public License
        44, # CPAL-1.0
    }:
        return True

def find_maintainer(maintainers):
    # https://filterlists.com/api/directory/maintainers

    for maintainer in maintainers:
        if maintainer in {
            7, # The EasyList Authors
            45, # Disconnect
            46, # AdGuard
            82, # AdBlock
        }:
            return True

def block_tags(tags):
    # https://filterlists.com/api/directory/tags

    for tag in tags:
        if tag in {
            10, # allowlist
            38, # beta
        }:
            return False
    return True

def find_language(languages):
    # https://filterlists.com/api/directory/languages

    if languages == []:
        return True

    for language in languages:
        if language in {
            31, # Danish
            37, # English
        }:
            return True

if __name__ == "__main__":
    main()
