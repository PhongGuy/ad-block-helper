import hashlib

import requests

dict = {

    # uBlock
    "uBlock filters": "https://ublockorigin.github.io/uAssets/filters/filters.txt",
    "uBlock filters - Badware risks": "https://ublockorigin.github.io/uAssets/filters/badware.txt",
    "uBlock filters - Privacy": "https://ublockorigin.github.io/uAssets/filters/privacy.txt",
    "uBlock filters - Quick fixes": "https://ublockorigin.github.io/uAssets/filters/quick-fixes.txt",
    "uBlock filters - Resource abuse": "https://ublockorigin.github.io/uAssets/filters/resource-abuse.txt",
    "uBlock filters - Unbreak": "https://ublockorigin.github.io/uAssets/filters/unbreak.txt",

    # Ads
    "AdGuard Base": "https://filters.adtidy.org/extension/ublock/filters/2_without_easylist.txt",
    "AdGuard Mobile Ads": "https://filters.adtidy.org/extension/ublock/filters/11.txt",
    "EasyList": "https://easylist.to/easylist/easylist.txt",

    # Privacy
    "AdGuard Tracking Protection": "https://filters.adtidy.org/extension/ublock/filters/3.txt",
    "AdGuard URL Tracking Protection": "https://filters.adtidy.org/extension/ublock/filters/17.txt",
    "Block Outsider Intrusion into LAN": "https://ublockorigin.github.io/uAssets/filters/lan-block.txt",
    "EasyPrivacy": "https://easylist.to/easylist/easyprivacy.txt",

    # Malware domains
    "Online Malicious URL Blocklist": "https://curben.gitlab.io/malware-filter/urlhaus-filter-online.txt",
    "Phishing URL Blocklist": "https://curben.gitlab.io/malware-filter/phishing-filter.txt",
    "PUP Domains Blocklist": "https://curben.gitlab.io/malware-filter/pup-filter.txt",

    # Malware protection
    "Spam404": "https://raw.githubusercontent.com/Spam404/lists/master/adblock-list.txt",

    # Anti-circumvention
    "ABP filters": "https://easylist-downloads.adblockplus.org/abp-filters-anti-cv.txt",

    # Annoyances
    "AdGuard Annoyances": "https://filters.adtidy.org/extension/ublock/filters/14.txt",
    "AdGuard Social Media": "https://filters.adtidy.org/extension/ublock/filters/4.txt",
    "Anti-Facebook": "https://filters.adtidy.org/extension/ublock/filters/4.txt",
    "EasyList Cookie": "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
    "Fanboy’s Annoyance": "https://secure.fanboy.co.nz/fanboy-annoyance.txt",
    "Fanboy’s Social": "https://easylist.to/easylist/fanboy-social.txt",
    "uBlock filters – Annoyances": "https://ublockorigin.github.io/uAssets/filters/annoyances.txt",

    # Multi-purpose
    "Dan Pollock’s hosts file": "https://someonewhocares.org/hosts/hosts",
    "Peter Lowe’s Ad and tracking server list": "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext",

    # Other Custom filters
    "Actually Legitimate URL Shortener Tool": "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/LegitimateURLShortener.txt",
    "0131 Block List": "https://austinhuang.me/0131-block-list/list.txt"
}

tempFile = "a.temp"
outFile = "block-all.txt"

def main():
    get_lists()
    remove_duplicates_and_comments()


def get_lists():
    print("Downloading lists...")
    open(tempFile, "w").close()

    for list in dict:
        print(f"Fetching {list}")
        f = requests.get(dict[list])
        with open(tempFile, "a", encoding="utf-8") as file:
            file.write(f.text.rstrip())

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

if __name__ == "__main__":
    main()
