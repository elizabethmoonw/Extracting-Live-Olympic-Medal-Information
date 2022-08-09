# query_olympics.py
# Prof. Lee (cs1110-prof@cornell.edu)
# Feb 10 2022

"""
Allow user to query live 2022 Winter Olympics medal statistics available at
     https://olympics.com/beijing-2022/...
webpages.
For a given "NOC" (similar to a country), prints out sport/event/medal type
for each medal.
"""

import a1_second  # We will use your code in this program!
import os  # For accessing file system
import glob  # File-existence checking
import requests  # For accessing webpages
import difflib # To get potential typo fixes


DATA_PREFIX = "https://olympics.com/beijing-2022/olympic-games/en/results/"
DATA_PREFIX = DATA_PREFIX + "all-sports/noc-medalist-by-sport"


TEAMS = \
['albania','american-samoa','andorra','argentina','armenia','australia',
'austria','azerbaijan','belarus','belgium','bolivia','bosnia-herzegovina',
'brazil','bulgaria','canada','chile','chinese-taipei','colombia','croatia',
'cyprus','czech-republic','timor-leste','denmark','ecuador','eritrea','estonia',
'finland','france','georgia','germany','ghana','great-britain','greece','haiti',
'hong-kong-china','hungary','iceland','india','ireland','islamic-rep-of-iran',
'israel','italy','jamaica','japan','kazakhstan','kosovo','kyrgyzstan','latvia',
'lebanon','liechtenstein','lithuania','luxembourg','madagascar','malaysia',
'malta','mexico','monaco','mongolia','montenegro','morocco','netherlands',
'new-zealand','nigeria','north-macedonia','norway','pakistan','china','peru',
'philippines','poland','portugal','puerto-rico','republic-of-korea',
'rep-of-moldova','roc','romania','san-marino','saudi-arabia','serbia',
'slovakia','slovenia','spain','sweden','switzerland','thailand',
'trinidad-and-tobago','turkey','ukraine','united-states','uzbekistan',
'virgin-islands-us']


# Helper functions

def print_badinput_message(mode, given, give_hint=True):
    """Prints a message saying we couldn't get that team's data,
    and suggests typo fixes.

    Preconditions:
        mode: either 's' or 'l' (lower-case ell), for sample or live mode.
        given [str]: purported team code for which an error is arising.
        give_hint [bool]: whether or not to print nearest matches to `given`
            in TEAMS
    """
    if mode=='l':
        print("Sorry, I couldn't access the relevant page on the" +
                " Olympics website.\n" +
                "Could there be a problem with the webserver?" )
    else:
        assert mode == 's', "print_bad_input_message: bad mode " + str(mode)
        print("Sorry, I don't have a file for that team.\n" +
              "Is folder 'sample_data' in the current directory?")
    if give_hint:
        closest = difflib.get_close_matches(given, TEAMS, cutoff=.3)
        if len(closest) > 0:
            print('Or, maybe you meant one of the following: ' +
                    ', '.join(closest)+'\n')
        else:
            print('I cannot guess what you might have intended.\n')

def text_til_next(source_text, indicator, start):
    """Returns: text in `source_text` starting from index `start` and running
    until next occurrence of string `indicator` (or end of source_text if
    there is no next occurrence).

    Preconditions:
        `indicator` [str]: length > 0
        `source_text` [str]:  contains at least one occurrence of `indicator`
        `start` [int]: >= 0, < len(source_text)
    """
    end = source_text.find(indicator, start)
    if end == -1:
        end = len(source_text)
    return source_text[start:end]

def live_data_fn(tcode):
    """Returns webpage contents for team code tcode.

    Preconditions: tcode is a lower-case country code used by this year's
    Winter Olympics webpages.

    Does no error checking of the requested webpage.
    (The Olympics server redirects 404s to a special page and returns 200.)
    """

    url = a1_second.data_url(DATA_PREFIX, tcode)
    return requests.get(url).text

def sim_data_fn(tcode):
    """Return html for team code tcode from local files in folder ./sample_data.
    All newlines (\n) will be replaced with \r, for consistency with the
    live data.

    Does not error-check.
    Preconditions: There is a relevant file <tcode>.htm in ./sample_data."""

    fname = tcode + ".htm"
    team_file = os.path.join(os.path.dirname(__file__),
                          "sample_data",
                          fname)
    with open(team_file, encoding="utf8") as infile:
        data_text = infile.read().replace('\n','\r')
    return data_text

#################################################

if __name__ == '__main__':
    print() # leave blank line before starting interaction

    # Does user want to use sample or live data?
    got_in_mode = False  # whether we know which input mode to use
    while not got_in_mode:
        in_prompt = ('Enter "S" or "L" (without the quotes. No response = "S").\n' +
                    '"S": use sample files on your computer.\n' +
                    '\t(Avoids hundreds of people bothering the real'+
                    ' webserver frequently/simultaneously.\n\t' +
                    'Also useful in case of Internet access problems.)\n' +
                    '"L": use the live Olympics webpages.\n'+
                    'Your choice? ')
        in_mode = input(in_prompt).strip().lower()
        in_mode = in_mode.replace('"','').replace("'",'')
        if in_mode not in ["l", "s", ""]:
            print("Sorry, I couldn't process your response.\n")
        else:
            got_in_mode=True
            if in_mode == "l":
                get_data_fn = live_data_fn
            else:
                assert in_mode in ['s', '']
                in_mode = 's'
                get_data_fn = sim_data_fn

    print()
    tcode_prompt = ('Enter a team code (without quotes)\n' +
                    'Or, just hit return for "united-states".\n' +
                    'Or, type "q" to quit: ')
    tcode = False # dummy initialization
    while tcode != "q":

        tcode = input(tcode_prompt).strip()
        while tcode not in TEAMS + ['','q']:
            print_badinput_message(in_mode, tcode)
            tcode = input(tcode_prompt).strip()


        if tcode == "":
            tcode = 'united-states'
        elif tcode == 'q':
            exit()

        tcode = tcode.replace('"', '').replace("'", "")

        # Set up data_text, checking input along the way
        try:
            data_text = get_data_fn(tcode)

            # Rough-n-ready grab of the medal list's approximate
            # portion of webpage.
            medal_instance_clue = 'Legend'
            medal_instance_start = data_text.index('playerTag') + \
                len('playerTag')
            data_text = text_til_next(data_text,
                                      medal_instance_clue,
                                      medal_instance_start)
        except requests.exceptions.RequestException:
            print_badinput_message(in_mode,tcode,give_hint=False)
            exit()
        except FileNotFoundError:
            assert tcode in TEAMS, "While-loop departure invariant violated"
            # Here because get_data_fn failed.
            print_badinput_message(in_mode,tcode,give_hint=False)
            exit()
        except ValueError:
            # Here because no medal info exists (no 'playerTag')
            print('No medals found for '+tcode+'\n')
            continue

        name_marker = '<div class="name">'
        while name_marker in data_text:
            # Assertion: there's another medal to report on

            section_start = data_text.index(name_marker)
            section_text = name_marker + \
                text_til_next(data_text,
                              name_marker,
                              section_start + len(name_marker))

            # Handle the asymmetry between individual and team winners
            # where one has an extra <span>...</span> around the name.
            section_text = section_text.replace('</span></a></div>', '</a></div>')

            tokens = a1_second.one_medal_info(section_text).split('!')
            if tokens[3] == '1':
                tokens[3]='Gold'
            elif tokens[3]=='2':
                tokens[3]='Silver'
            else:
                tokens[3]='Bronze'

            # There is a leading '\r' in the event.
            print(", ".join(tokens).replace('\r', ''))

            # Advance to next section, if any
            data_text = data_text[section_start + len(section_text):]


        tcode_prompt = ('......\n\nEnter another country code,' +
                        'like "united-states",' +
                        ' or <return> for "united-states", or "q" to quit: ')
