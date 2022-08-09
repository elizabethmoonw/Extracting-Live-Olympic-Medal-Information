# a1_second.py
# Sources/people consulted: NONE
# February 21, 2022
# Skeleton by Prof. Lee, further edited and developed by Elizabeth Moon

"""
Functions for extracting medal data from the olympics.com Beijing 2022 webpages.
"""

def after_last(text, marker):
    """Returns substring of `text` after last occurrence of `marker`.
    Preconditions:
     `text` [str]: contains at least one instance of `marker`
     `marker` [str]: length > 0

    Examples:
        after_last("ab+c", "+") ---> 'c'
            To be clear, that's a length-one string.

        after_last('faith <cough> hope <cough>Charity', '<cough>') --->
            'Charity'
    """
    start_pos = text.rindex(marker)+len(marker)
    return text[start_pos:]


def data_url(prefix, c):
    """Returns: new string of the form prefix-c.htm
    Precondition: `c` and `prefix` are non-empty strings

    Example: If we had
        prefix: "https://olympics.com/noc-medalist-by-sport"
        c: "united-states"
    Then this function would return the string
        "https://olympics.com/noc-medalist-by-sport-united-states.htm"
    """
    data_url_info = str(prefix + "-" + c + ".htm")
    return data_url_info


def after_first(text, marker):
    """Returns: portion of `text` starting just after the 1st occurrence of
    `marker`.

    Preconditions:
     `text` [str]: contains at least one instance of `marker`
     `marker` [str]: length > 0

    Examples:
        after_first("ab+c", "+") ---> 'c'
            To be clear, that's a length-one string.

        after_first('faith <cough> hope <cough>Charity', '<cough>') --->
            ' hope <cough>Charity'
            To be clear, the returned string starts with a space.
    """
    start_pos = text.index(marker)+len(marker) 
    return text[start_pos:]

def before_first(text, marker):
    """Returns: portion of `text` ending just before the first occurrence of
    `marker`.

    Preconditions:
     `text` [str]: contains at least one instance of `marker`
     `marker` [str]: length > 0

    Examples:
        before_first("ab+c", "+") ---> 'ab'

        before_first('faith <cough> hope <cough>Charity', '<cough>') --->
            'faith '
    """
    start_pos = text.index(marker)
    return text[:start_pos]

def scoop(text, starter, ender):
    """Returns substring of `text` that:
     * starts just after the end of the 1st occurrence of `starter` in `text`
     * ends just before the beginning of the 1st following occurrence of `ender`.

    Preconditions:
     `text` [str]: length > 0.
     `starter` and `ender` [str]: both non-empty and occur in `text`.
     At least one `ender` appears after a `starter` in `text`.

    Examples:
     scoop('+a+b+c!+4def+5','+', '!') ---> 'a+b+c'
     scoop('good job :) good example foo(0) ', '(', ')' ) --> '0'
     t = '<li style="color:purple">python</li><span> the < is intentional</span>'
     scoop(t, '<span>','</span>') ---> " the < is intentional"
    """
    start_pos =  len(before_first(text, starter)) + len(starter)
    spliced_text = text[start_pos:]
    end_pos =  len(text) - len(after_first(spliced_text, ender)) - len(ender)
    scooped_str = text[start_pos:end_pos]
    return scooped_str


def one_medal_info(s):
    """Returns string of the form
        <winner name>!<sport>!<event>!<medal type>
    where the relevant data is pulled from `s`.

    These four data items should have exactly the capitalization, punctuation,
    and spacing as in `s`.

    See a1_first.test_one_medal_info() for examples.

    Preconditions:

    `s` is a string of the following form, where WN, SP, EV, and MT
    indicates non empty word(s) with no double-quotes, angle brackets ("<" or ">"),
    or '!', and "..." stands for anything:

    1. `s` starts with
            <div class="name">...>WN</a></div>
        with no "<div>" or "</div>" in the middle.
        There are no other occurrences of <div class="name"> in `s`.

        [Technicality: in real data, for individual (e.g., non-team)
        winners), there a </span> right before the </a>.  Our
        "wrapper" code will delete this for students.]

    2. After that, `s` has a portion
            daily-schedule - SP">
        There are no other occurrences of 'daily-schedule' in `s`.
    3. After that, `s` has a portion
            <td class="StyleCenter">
            EV</td>
        There are no other occurrences of 'StyleCenter' in `s`.
    4. After that, `s` has a portion
            medals/big/MT.png
        There are no other occurrences of 'medals/big/' in `s`.
    """
    # 1: Retrieving the Winner Name (WN)

    # Step 1a
    scoop_WNstarter = '<div class="name">'
    scoop_WNender = '</a></div>'
    WN_scooped = scoop(s, scoop_WNstarter, scoop_WNender)

    # Step 1b: Then, get the stuff in the scooped-out part after the last ‘>’
    isolated_WN = after_last(WN_scooped,'>')

    # 2: Retrieving the sport (SP)
    scoop_SPstarter = 'daily-schedule - '
    scoop_SPender = '">'
    SP_scooped = scoop(s, scoop_SPstarter, scoop_SPender)

    # 3: Retrieving the event (EV)
    scoop_EVstarter = '<td class="StyleCenter">\r'
    scoop_EVender = '</td>'
    EV_scooped = scoop(s, scoop_EVstarter, scoop_EVender)

    # 4: Retrieving the medal type (MT)
    scoop_MTstarter = 'medals/big/'
    scoop_MTender = '.png'
    MT_scooped = scoop(s, scoop_MTstarter, scoop_MTender)

    # 5: Putting it all together...
    # Concatenate the str such that <winner name>!<sport>!<event>!<medal type>
    medal_info_str = isolated_WN + '!' + SP_scooped + '!' + EV_scooped + '!' + \
    MT_scooped

    return medal_info_str
