import hashlib

import requests

tempFile = "abc.temp"
outFile = "block-all.txt"

def main():
    get_lists()
    remove_duplicates_and_comments()


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
        if find_license(list["licenseId"]) and dont_add(list["id"]) and find_syntax(list["syntaxIds"]):
            print("Downloading list: " + list["name"])
            blob = requests.get(list['primaryViewUrl']).text.strip()
            with open(tempFile, "a", encoding="utf-8") as output_file:
                output_file.write(blob + "\n")

    print("Done!")

def remove_duplicates_and_comments():
    print("Removing duplicates and comments...")

    completed_lines = set()

    with open(outFile, "w", encoding="utf-8") as output_file:
        for lines in open(tempFile, "r", encoding="utf-8"):
            line = lines.rstrip()
            if not line.startswith(("!", "# ", "#	", "  ", "	", " 	")):
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
            8, # URLs
            9, # IPs (IPv4)
            16, # Domains with wildcards
            28, # Adblocker domains
            38 # Adblock Plus Advanced
            }:
            return True

def find_license(license):
    # https://filterlists.com/api/directory/licenses

    if license in {
        2, # The MIT License (MIT)
        23, # "Dont Be a Dick" Public License
        24, # CC BY 4.0
        28, # CC0 1.0 Universal
        38 # Generic copyfree
        }:
        return True

def dont_add(id):
    # https://filterlists.com/api/directory/lists

    if id not in {
        375, #All-in-One Customized Adblock List
        2553 #Maltrail - Parking sites
        }:
        return True

if __name__ == "__main__":
    main()
