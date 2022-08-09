# a1_first.py
# Sources/people consulted: NONE
# February 16, 2022
# Skeleton by Prof. Lee (cs1110-prof@cornell.edu), Feb 10 2022, further edited and developed by Elizabeth Moon

import cornellasserts
import a1_second

DONE_MSG = 'finished test \n'


def test_data_url():
    """Test function a1_second.data_url()"""
    print("Testing a1_second.data_url()")

    # something like what we expect in real usage
    s1 = "https://olympics.com/noc-medalist-by-sport"
    s2 = "united-states"
    correct_str = 'https://olympics.com/noc-medalist-by-sport-united-states.htm'
    result = a1_second.data_url(s1, s2)
    cornellasserts.assert_equals(correct_str, result)

    # inputs with slashes and spaces
    result = a1_second.data_url("A//", "b c")
    cornellasserts.assert_equals("A//-b c.htm", result)

    # a one-character input including hyphen, a long input
    result = a1_second.data_url("-", "longstringwithhtm")
    cornellasserts.assert_equals("--longstringwithhtm.htm", result)
    result = a1_second.data_url("longstringwithhtm", "-")
    cornellasserts.assert_equals("longstringwithhtm--.htm", result)

    print(DONE_MSG)


def test_after_first():
    """Test function a1_second.after_first()
    """
    print("Testing a1_second.after_first()")

    # 1. marker at beginning
    result = a1_second.after_first('+c', '+')
    cornellasserts.assert_equals('c', result)

    # 2. marker in middle
    result = a1_second.after_first("ab+c", "+")
    cornellasserts.assert_equals('c', result)

    # 3. marker at end
    result = a1_second.after_first("abc+", "+")
    cornellasserts.assert_equals('', result)

    # 4. marker occurs multiple times (and longer than one character)
    result = a1_second.after_first("Lee, Lillian; Lee, Tommy; Lee, Stan", "Lee")
    cornellasserts.assert_equals(", Lillian; Lee, Tommy; Lee, Stan", result)

    # 5. text and marker are the same
    result = a1_second.after_first('+', '+')
    # cornellasserts.assert_equals('+', result)
    cornellasserts.assert_equals('', result)

    # 6. marker is a space
    result = a1_second.after_first("Hi! How's it going?", " ")
    cornellasserts.assert_equals("How's it going?", result)

    # 7. parts of marker show up before the full marker
    result = a1_second.after_first('12a1b123target', '123')
    cornellasserts.assert_equals('target', result)

    # 8. marker is part of a word, case mismatch earlier
    result = a1_second.after_first("Famous leeks are made in Leeds, Lee", "Lee")
    cornellasserts.assert_equals('ds, Lee', result)

    # 9. marker occurs multiple times and is ONE character
    result = a1_second.after_first("I! love CS1110!", "!")
    cornellasserts.assert_equals(' love CS1110!', result)
    print(DONE_MSG)


def test_before_first():
    """ Quick checks of function a1_second.before_first """
    print('Testing a1_second.before_first()')

    result = a1_second.before_first("ab+c", "+")
    cornellasserts.assert_equals('ab', result)

    result = a1_second.before_first('faith <cough> hope <cough>Charity', '<cough>')
    cornellasserts.assert_equals('faith ', result)

    print(DONE_MSG)

def test_scoop():
    """Test function a1_second.scoop"""

    print("Testing a1_second.scoop")

    # Case 1: The markers are spaces
    result =  a1_second.scoop('CS1110 is fun!', ' ', '!')
    cornellasserts.assert_equals('is fun', result)

    # Case 2: end_str is more than one character
    result = a1_second.scoop('CS1110 Project','C', 'Project')
    cornellasserts.assert_equals('S1110 ', result)

    # Case 3: start_str and end_str are adjacent
    result = a1_second.scoop('CS is fun', 'i', 's')
    cornellasserts.assert_equals('', result)

    # Case 4: start_str and end_str are the same
    result = a1_second.scoop('Coding is cool', 'o','o')
    cornellasserts.assert_equals('ding is c', result)

    # Case 5: parts of marker show up before the full marker
    result = a1_second.scoop('12123456', '123', '6')
    cornellasserts.assert_equals('45', result)

    # Case 6: multiple end_str show up before multiple start_str
    result = a1_second.scoop('CS1110 1110 Project Project 1110', 'Pro', '1110')
    cornellasserts.assert_equals('ject Project ', result)

    # simple markers, typical case (given, guaranteed correct)
    result = a1_second.scoop('+a+b+c!+4def+5', '+', '!')
    cornellasserts.assert_equals('a+b+c', result)

    # end_str before start_str (given, guaranteed correct)
    result = a1_second.scoop('good job :) god example foo(0) ', '(', ')' )
    cornellasserts.assert_equals("0", result)

    # given, guaranteed correct
    t = '<li style="color:purple">python</li><span> the < is intentional</span>'
    result=a1_second.scoop(t, '<span>','</span>')
    cornellasserts.assert_equals(" the < is intentional", result)

    # start_str is more than one character
    t = '<li style="color:purple">python</li><span>the < is intentional</span>'
    result = a1_second.scoop(t, '<span>', '<')
    cornellasserts.assert_equals("the ", result)


    print(DONE_MSG)


def test_one_medal_info():
    """Test function a1_second.one_medal_info"""

    print("Testing a1_second.one_medal_info")

    # Very simple version of template.
    s = ('<div class="name"> >A</a></div>daily-schedule - B"> ' +
          '<td class="StyleCenter">\rC</td>medals/big/D.png')
    result = a1_second.one_medal_info(s)
    cornellasserts.assert_equals('A!B!C!D',result)

    # Another version of template. Variations in spacing, punctuation, etc.
    s0 = ('<div class="name"> x <>y >ITHACA</a></div> As you set out for ' +
          'Ithaca daily-schedule - 1865 on the Dot"> hope your road is' +
          'a long one <td class="StyleCenter">\r'  +
          'wAIting</td>\nfull of adventure, full medals/big/ ho la.png of' +
          ' discovery.')
    result = a1_second.one_medal_info(s0)
    cornellasserts.assert_equals('ITHACA!1865 on the Dot!wAIting! ho la',
                                 result)

    # Almost-completely-real example, individual name
    # (with pesky extra </span> removed)
    # Triple-single-quotes can be used to enclose multi-line strings
    # (with leading whitespace and newlines in the result).
    sre1 = (
            '<div class="name"><a href="../../../en/results/freestyle-skiing/athlete-profile-n1044687-colby-stevenson.htm" ' +
            'title="en/results/freestyle-skiing/athlete-profile-n1044687-colby-stevenson">' +
            '<span class="d-md-none">STEVENSON C</span><span class="d-none ' +
            'd-md-inline">STEVENSON Colby</a></div></div></td>' + '\n' +
            '''<td>
            <a href="../../../en/results/freestyle-skiing/olympic-daily-schedule.htm"'''+
            'title="en/results/freestyle-skiing/olympic-daily-schedule - Freestyle Skiing">' +
            '<img src="../../../static/owg2022/img/sports/FRS.png"' +
            ' role="presentation" aria-hidden="true" alt="" class="sport-icon"' +
            ' align="middle">FRS</a></td>\n' +
            '<td class="StyleCenter">\r' +
            "Men's Freeski Big Air</td>" +
            '<td class="text-center">' + '\n' +
            '<img class="medal-icon" src="../../../static/owg2022/img/medals/big/2.png" alt="2">\n' +
            '</td>\n</tr>')
    result = a1_second.one_medal_info(sre1)
    cornellasserts.assert_equals("STEVENSON Colby!Freestyle Skiing!Men's Freeski Big Air!2", result)


   # Almost-completely-real example, team name
    sre2 = (
    '''<div class="name"><a href="../../../en/results/figure-skating/athlete-profile-nfskxteam-usa01-null-null.htm" title="en/results/figure-skating/athlete-profile-nfskxteam-usa01-null-null">United States of America</a></div></div></td>
    <td>
    <a href="../../../en/results/figure-skating/olympic-daily-schedule.htm" title="en/results/figure-skating/olympic-daily-schedule - Figure Skating"><img src="../../../static/owg2022/img/sports/FSK.png" role="presentation" aria-hidden="true" alt="" class="sport-icon" align="middle">FSK</a></td>
    <td class="StyleCenter">''' + '\r' +
    'Team Event</td>\n' +
    '<td class="text-center">\n' +
    '<img class="medal-icon" src="../../../static/owg2022/img/medals/big/1.png" alt="1">\n' +
    '</td>\n'
    '</tr>\n')
    result = a1_second.one_medal_info(sre2)
    cornellasserts.assert_equals("United States of America!Figure Skating!Team Event!1", result)
    print(DONE_MSG)



###########
# Calls to testing functions
###########

# This line means the code below is executed only if this file is run as a
# script; if this file is imported, the test functions are _not_ called.
if __name__ == '__main__':

    test_data_url()


    test_after_first()

    test_before_first()

    test_scoop()

    test_one_medal_info()

    print('Passed all tests in this file. Hurrah!')
