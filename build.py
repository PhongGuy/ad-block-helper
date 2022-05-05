import hashlib

import requests

dict = {}
# uBlock
dict["uBlock filters"] = "https://ublockorigin.github.io/uAssets/filters/filters.txt"
dict["uBlock filters – Badware risks"] = "https://ublockorigin.github.io/uAssets/filters/badware.txt"
dict["uBlock filters – Privacy"] = "https://ublockorigin.github.io/uAssets/filters/privacy.txt"
dict["uBlock filters – Quick fixes"] = "https://ublockorigin.github.io/uAssets/filters/quick-fixes.txt"
dict["uBlock filters – Resource abuse"] = "https://ublockorigin.github.io/uAssets/filters/resource-abuse.txt"
dict["uBlock filters – Unbreak"] = "https://ublockorigin.github.io/uAssets/filters/unbreak.txt"

# Ads
dict["AdGuard Base"]  = "https://filters.adtidy.org/extension/ublock/filters/2_without_easylist.txt"
dict["AdGuard Mobile Ads"] = "https://filters.adtidy.org/extension/ublock/filters/11.txt"
dict["EasyList"] = "https://easylist.to/easylist/easylist.txt"

# Privacy
dict["AdGuard Tracking Protection"] = "https://filters.adtidy.org/extension/ublock/filters/3.txt"
dict["AdGuard URL Tracking Protection"] = "https://filters.adtidy.org/extension/ublock/filters/17.txt"
dict["Block Outsider Intrusion into LAN"] = "https://ublockorigin.github.io/uAssets/filters/lan-block.txt"
dict["EasyPrivacy"] = "https://easylist.to/easylist/easyprivacy.txt"

# Malware domains
dict["Online Malicious URL Blocklist"] = "https://curben.gitlab.io/malware-filter/urlhaus-filter-online.txt"
dict["Phishing URL Blocklist"] = "https://curben.gitlab.io/malware-filter/phishing-filter.txt"
dict["PUP Domains Blocklist"] = "https://curben.gitlab.io/malware-filter/pup-filter.txt"

# Malware protection
dict["Spam404"] = "https://raw.githubusercontent.com/Spam404/lists/master/adblock-list.txt"

# Anti-circumvention
dict["ABP filters"] = "https://easylist-downloads.adblockplus.org/abp-filters-anti-cv.txt"

# Annoyances
dict["AdGuard Annoyances"] = "https://filters.adtidy.org/extension/ublock/filters/14.txt"
dict["AdGuard Social Media"] = "https://filters.adtidy.org/extension/ublock/filters/4.txt"
dict["Anti-Facebook"] = "https://filters.adtidy.org/extension/ublock/filters/4.txt"
dict["EasyList Cookie"] = "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt"
dict["Fanboy’s Annoyance"] = "https://secure.fanboy.co.nz/fanboy-annoyance.txt"
dict["Fanboy’s Social"] = "https://easylist.to/easylist/fanboy-social.txt"
dict["uBlock filters – Annoyances"] = "https://ublockorigin.github.io/uAssets/filters/annoyances.txt"

# Multi-purpose
dict["Dan Pollock’s hosts file"] ="https://someonewhocares.org/hosts/hosts"
dict["Peter Lowe’s Ad and tracking server list"] ="https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext"

# Other Custom filters
dict["Actually Legitimate URL Shortener Tool"] = "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/LegitimateURLShortener.txt"

tempFile = "all.temp"
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
