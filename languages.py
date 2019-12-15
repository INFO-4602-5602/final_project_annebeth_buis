#!/usr/bin/env python3
import csv, json

# Code for using WALS
language_data = {}
# Read data set from CSV
with open('wals_languages.csv/language.csv') as csvfile:
    print("Open from CSV")
    lreader = csv.reader(csvfile, delimiter=",", quotechar='"')
    language_data["languages"] = []
    # Parse csv into list of lists,  replace '' with NaN (empty cells)
    for i, row in enumerate(lreader):
        if i > 0:
            language_name = row[3]
            if "(" in language_name:
                language_name = language_name.split("(")[0].strip()
            language_longitude = row[5]
            language_latitude = row[4]
            language_family = row[7]
            language_data["languages"].append({
                "name": language_name,
                "longitude": language_longitude,
                "latitude": language_latitude,
                "family": language_family
            })

# with open('languages.json', 'w') as outfile:
#     json.dump(language_data, outfile, indent=4)

ud_languages = []
with open('data/UDLanguages.csv') as csvfile:
    lreader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for i, row in enumerate(lreader):
        if i > 0:
            ud_languages.append(row[1])
print("UD Languages count: ", len(ud_languages))

um_languages = []
with open('data/UnimorphLanguages.csv') as csvfile:
    lreader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for i, row in enumerate(lreader):
        if i > 0:
            um_languages.append(row[1])
print("Unimorph Languages count: ", len(um_languages))

languages = list(set(ud_languages + um_languages))
print("Languages count: ", len(languages))

with open('data/languages.csv', 'w') as outfile:
    for l in languages:
        outfile.write(l + "\n")
