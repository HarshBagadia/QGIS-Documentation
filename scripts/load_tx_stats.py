#!/usr/bin/env python3

from os import path
from datetime import date

import requests
#import yaml

# This script downloads the statistics of localization of the project from Transifex.
# To be able to use it, you need to provide your user account token
# and run `python3 scripts/load_tx_stats.py` from the repo main folder

#Load stats of the QGIS Documentation project from transifex
response = requests.get('https://api.transifex.com/organizations/qgis/projects/qgis-documentation/',
                        auth=('api', '<token>')
                       )
data = response.json()
#print(data)

# Get statistics of translation for each target language
language_rate={}

# Fetch list of languages
for lang in data['languages']:
    code = lang['code']
    name = lang['name']
    language_rate[code] = name

# Fetch and store stats of interest for each target language
for code in data['stats']:
    language_rate[code] = {'name' : language_rate[code],
                           'percentage' : round(data['stats'][code]['translated']['percentage']*100, 2)
                          }

# Stats for the whole project (== English source language)
# Number of languages declared in transifex for the project
nb_languages = len(data['languages'])
# Total number of strings in English to translate
totalstringcount = data['stringcount']
# translation percentage of the whole project
translation_ratio = round(sum([value['percentage'] for value in language_rate.values()])/nb_languages, 2)

language_rate['en']={'nb_languages': nb_languages,
                     'stringcount': totalstringcount,
                     'percentage' : translation_ratio
                     }
print('all', language_rate)

def load_overall_stats():
    """Format statistics of translation in the project"""

    text = (f".. list-table::\n"
            f"   :widths: auto\n"
            f"\n"
            f"   * - Number of strings\n"
            f"     - Number of target languages\n"
            f"     - Overall Translation ratio\n"
            f"   * - **{totalstringcount}**\n"
            f"     - **{nb_languages}**\n"
            f"     - **{translation_ratio}%**\n"
            f"\n")

    return text

def load_lang_stats(stats, nb_columns=1):
    """Format statistics of translated languages into a multicolumn table"""

    text = (f".. list-table::\n"
            f"   :widths: auto\n"
            f"\n"
            f"   * - Language\n"
            f"     - Translation ratio (%)\n")
    #Add more columns
    text +=(f"     - Language\n     - Translation ratio (%)\n" * (nb_columns - 1))

    i=1
    for lang in stats:
        if lang != 'en':
            if i % nb_columns == 1 or nb_columns == 1:
                text += (f"   * - {stats[lang]['name']}\n")
            else:
                text += (f"     - {stats[lang]['name']}\n")

            text += (f"     - {stats[lang]['percentage']}\n")
            i+=1

            # todo: Add empty cells when the number of languages
            # is not a multiple of number of columns

    return text

# Store the stats as a table in a rst file
statsfile = path.join(path.dirname(__file__), '..','docs/user_manual/preamble/translation_stats.rst')
with open(statsfile, 'w') as f:
    f.write(f":orphan:\n\n"
            f".. DO NOT EDIT THIS FILE DIRECTLY. It is generated automatically by\n"
            f"   load_tx_stats.py in the scripts folder.\n\n"
            f"Statistics of translation\n"
            f"===========================\n\n"

            f"*(last update: {date.today()})*"
            f"\n\n"
            f"{load_overall_stats()}"
            f"\n\n"
            f"{load_lang_stats(language_rate, nb_columns=3)}"
            f"\n\n"
           )


# Output all stats to a yaml file we can parse to feed documentation based on locale
#cfgfile = path.join(path.dirname(__file__), '..','transifex.yml')
#with open(cfgfile, 'w') as yaml_file:
#    yaml_file.write("#last update: {}\n\n".format(datetime.datetime.now()))
#    yaml.dump(language_rate, yaml_file)


