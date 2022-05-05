import hashlib
import json
import requests

# https://filterlists.com/

tempFile = "allv2.temp"
outFile = "block-allv2.txt"

def main():
    get_lists()
    remove_duplicates_and_comments()


def get_lists():
    print("Downloading lists...")

    lists = json.loads(requests.get("https://filterlists.com/api/directory/lists").text)

    open(tempFile, "w").close()

    for list in lists:
        if find_license(list["licenseId"]) and dont_add_name(list["name"]) and find_syntax(list["syntaxIds"]):
            print("Downloading list: " + list["name"])
            filter = requests.get(list['primaryViewUrl']).text.strip()
            with open(tempFile, "a", encoding="utf-8") as output_file:
                output_file.write(filter + "\n")

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
    for id in list:
        if id in {3, 4, 6, 8, 9, 16, 28, 38}:
            return True

def find_license(license):
    if license in {2, 23, 24, 28, 38}:
        return True

def dont_add_name(name):
    if name not in {"Maltrail - Parking sites"}:
        return True

if __name__ == "__main__":
    main()
