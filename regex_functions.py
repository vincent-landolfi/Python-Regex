"""
# Copyright Nick Cheng, Brian Harrington, Vincent Landolfi,
# Danny Heap, 2013, 2014, 2015, 2016
#
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.


def is_regex_helper(regex_list, ternaries=['0', '1', '2', 'e'],
                    symbols=['.', '|']):
    ''' (list,list,list) -> str
    Takes in a list regex_list expression and then
    creates a string that can be evaluated by
    the built in python parser.
    >>> is_regex_helper(['0','*','|','9','*'])
    '(True or False and False or False)'
    >>> is_regex_helper([['1','.',['0','|','2']'*'],'.','0'])
    '((True and (True and True) or False) and True)'
    >>> is_regex_helper(['1','1','.','e'])
    (TrueTrue and True)
    >>> is_regex_helper(['3','|','e'])
    (False)
    >>> is_regex_helper(['2','.','3'])
    (True and False)
    >>> is_regex_helper(['2','*','*','*'])
    (True of False or False or False)
    '''
    # if we've gone through the list
    if regex_list == [] or regex_list == ():
        # add the ending bracket to the bool
        result = ')'
    # if we're still traversing
    else:
        # check if we have a list element
        if isinstance(regex_list[0], list):
            # make sure its the right length
            if (len(regex_list[0]) == 3 or
                    (len(regex_list[0]) > 3 and '*' in regex_list[0])):
                # do the same to that list
                result = '(' + \
                    is_regex_helper(regex_list[0]) + \
                    is_regex_helper(regex_list[1:])
            # otherwise its just false
            else:
                result = 'False)'
        # if we have a ternary value
        elif regex_list[0] in ternaries:
            # then when know that element yields true as a regex_list value
            result = 'True' + is_regex_helper(regex_list[1:])
        # if we have a symbol
        elif regex_list[0] in symbols:
            # this is like 'and' in our boolean
            result = ' and ' + is_regex_helper(regex_list[1:])
        # if we have a star
        elif regex_list[0] == '*':
            # its based on the previous numbers, so its like
            # saying 'or False'
            result = ' or False' + is_regex_helper(regex_list[1:])
        # if its neither of those
        else:
            # then its False, no need to keep looking
            result = 'False)'
    # send back the stringed boolean statement
    return result


def is_regex(regex):
    ''' (str) -> bool
    Tells the user if the given string is a valid
    regex or not
    >>> is_regex('((1.(0|1)*).2)')
    True
    >>> is_regex('(1)')
    False
    '''
    # instantiate some vars
    result = True
    ternaries = ['0', '1', '2', 'e']
    if regex not in ternaries:
        # check if there shouldnt be brackets, its blank, or there
        # should be brackets, back to back brackets, or too small
        # of an expression between brackets
        if ((regex == '') or (regex[0] == '(' and regex[-1] == ')'and
            len(regex) <= 4) or (len(regex) >= 3 and '*' not in regex and
                                 (regex[0] != '(' or regex[-1] != ')') or
                                 '()' in regex)):
            # then its false, not valid
            result = False
        # were going to make the string easier to work with
        # by making it a nested list, or tuple if there arent
        # brackets
        if result:
            # check if there are the right amount of brackets
            if (regex.count('(') == regex.count(')')):
                # first were just casting it to list type, and then
                # taking the string of that, and removing the opening
                # and close hard brackets
                lis = str(list(regex))[1:-1]
                # then we'll replace the hard brackets with soft brackets
                lis = lis.replace("'(',", '[').replace("')'", ']')
                # try to evaluate if
                try:
                    # make a nested list using python'regex built
                    # in parser
                    lis = eval(lis)
                # if we cant
                except:
                    # its obviously not a valid regex
                    result = False
            # if there is not the right number of brackets
            else:
                # then its not a regex
                result = False
        # see if we have to do this part
        if result:
            # make sure the current list is the right length
            # and the result isnt already false
            if len(lis) <= 3 or (len(lis) > 3 and '*' in lis):
                # send the new list to the helper
                result = '(' + is_regex_helper(lis)
            # if its not, then its false
            else:
                result = False
        # we should only do this if result is a string
        if type(result) == str:
            # were going to try to evaluate the result now
            # the result is a boolean in the form of a string
            # which the helper made for us

            # check if it contains two booleans in a row, which would
            # yield a name error
            if ('TrueTrue' in result or 'TrueFalse' in result):
                # then its false
                result = False
            # if there'regex no sketchy booleans
            else:
                # test out parsing the boolean
                try:
                    # we'll try to evaluate the boolean in string form
                    result = eval(result)
                # if there'regex an error, the regex is obviously not valid
                except:
                    result = False
        # return the evaluated boolean
    return result


def tree_helper(regex_list, ternaries=['0', '1', '2', 'e']):
    ''' (list) -> RegexTree
    Takes in a list form of the regex and creates a
    tree recursively
    >>> tree_helper(['e'])
    Leaf('e')
    >>> tree_helper(['1','.','0'])
    DotTree(Leaf('1'), Leaf('0'))
    >>> tree_helper(['1','|',['2','.','e'],'*'])
    BarTree(Leaf('1'), StarTree(DotTree(Leaf('2'), Leaf('e'))))
    '''
    # base check if there are dots or bars in the
    # regex
    if '.' in regex_list:
        # make a dot node
        # everything left of the dot is left, right of
        # dot is right
        result = DotTree(tree_helper(regex_list[:regex_list.index('.')]),
                         tree_helper(regex_list[regex_list.index('.') + 1:]))
    # check for bars
    elif '|' in regex_list:
        # make a bar node
        # everything left of the bar is left, right of
        # bar is right
        result = BarTree(tree_helper(regex_list[:regex_list.index('|')]),
                         tree_helper(regex_list[regex_list.index('|') + 1:]))
    # check for stars
    elif '*' in regex_list:
        # make a star node, everything to the left of it is its child
        result = StarTree(tree_helper(regex_list[:regex_list.index('*')]))
    # if we've gone through all the dots and bars
    else:
        # if its a list
        if isinstance(regex_list[0], list):
            # call the tree helper on that list
            result = tree_helper(regex_list[0])
        # if its a symbol
        elif regex_list[0] in ternaries:
            # make a new leaf node
            result = Leaf(regex_list[0])
    # return the result
    return result


def build_regex_tree(regex):
    ''' (str) -> RegexTree
    Takes the given regex and returns the root
    of the newly created tree of that regex
    >>> build_regex_tree('0')
    Leaf('0')
    >>> build_regex_tree('2*')
    StarTree(Leaf('2'))
    >>> build_regex_tree('e')
    Leaf('e')
    >>> build_regex_tree('(1.0)')
    DotTree(Leaf('1'), Leaf('0'))
    >>> build_regex_tree('(1|(2.e)*)')
    BarTree(Leaf('1'), StarTree(DotTree(Leaf('2'), Leaf('e'))))
    '''
    # convert the regex expression into a list
    # using the same methods highlighted in is_regex

    # first were just casting it to list type, and then
    # taking the string of that, and removing the opening
    # and close hard brackets
    lis = str(list(regex))[1:-1]
    # then we'll replace the hard brackets with soft brackets
    lis = lis.replace("'(',", '[').replace("')'", ']')
    # we know its valid so we can evaluate it
    # to make it a nested list
    lis = eval(lis)
    # check if we have any symbols in the regex,
    # if so, get the smallest
    # call the helper to do everything
    tree = tree_helper(lis)
    # return it
    return tree


def match_helper(tree, tern_str):
    ''' (RegexTree,str) -> bool
    Returns a string that contains all the leftover
    values of regex. If it returns blank, then all the values
    were removed, and regex matches the tree.
    >>> x = build_regex_tree('e')
    >>> match_helper(x,'')
    ''
    >>> x = build_regex_tree('((2*.1)*.(1*.0*))')
    >>> match_helper(x,'22222111002')
    '2'
    >>> x = build_regex_tree('(1.0)')
    >>> match_helper(x,'02')
    '02'
    >>> match_helper(x,'')
    'NO'
    >>> x = build_regex_tree('((1.0)|(2|e))')
    >>> match_helper(x,'10')
    ''
    >>> match_helper(x,'2')
    ''
    >>> match_helper(x,'2e')
    'e'
    '''
    # check if we have a dot
    if tree.get_symbol() == '.':
        # first check the left side
        result = match_helper(tree.get_children()[0], tern_str)
        # check if left string is shorter, or if its not a star, since
        # stars can yield empty strings
        if ((len(result) < len(tern_str)) or
                tree.get_children()[0].get_symbol() == '*'):
            # do the right string too
            result = match_helper(tree.get_children()[1], result)
    # if we have a bar
    elif tree.get_symbol() == '|':
        # check the left side
        result = match_helper(tree.get_children()[0], tern_str)
        # check if the string remained the same size
        if len(result) == len(tern_str):
            # check the right side
            result = match_helper(tree.get_children()[1], tern_str)
    # if we have a star (my favorite)
    elif tree.get_symbol() == '*':
        # check if tern_str is blank
        if tern_str == '':
            # send back the blank
            result = tern_str
        # if its not
        else:
            # check its only child
            result = match_helper(tree.get_children()[0], tern_str)
        # check if the result is smaller than tern_str, and keep going
        # until the list is blank or it stops matching
        while (len(result) < len(tern_str)) and result != '':
            # make tern_str the previous result
            tern_str = result
            # do it again, with result instead of tern_str
            result = match_helper(tree.get_children()[0], result)
    # check if the tree is a leaf
    elif tree.get_symbol() in ['1', '2', '0', 'e']:
        # check if we have characters to work with
        if len(tern_str) > 0:
            # check if it is the same as the char at the
            # 0th index of x
            if tree.get_symbol() == tern_str[0]:
                # send back a sliced string, 0th element gone
                result = tern_str[1:]
            # otherwise
            else:
                # just send back tern_str
                result = tern_str
        # otherwise they're not equal
        else:
            # check if we have an e
            if tree.get_symbol() == 'e':
                # make it blank
                result = ''
            # if we dont
            else:
                # ruin the string, so it wont be blank
                result = 'NO'
    # return the result
    return result


def regex_match(tree, tern_str):
    ''' (RegexTree,str) -> bool
    Returns true iff the inputted string matches
    the tern_str of the inputted tree
    >>> x = build_regex_tree('e')
    >>> regex_match(x,'')
    True
    >>> regex_match(x,'2222111')
    False
    >>> x = build_regex_tree('((2*.1)*.(1*.0*))')
    >>> regex_match(x,'22222111002')
    False
    >>> regex_match(x,'2222211100')
    True
    >>> x = build_regex_tree('(1.0)')
    >>> regex_match(x,'02')
    False
    >>> regex_match(x,'')
    False
    >>> x = build_regex_tree('((1.0)|(2|e))')
    >>> regex_match(x,'10')
    True
    >>> regex_match(x,'2')
    True
    >>> regex_match(x,'2e')
    False
    '''
    # get a returned string from the helper
    match = match_helper(tree, tern_str)
    # if we were able to clear all the values,
    # then we have a match
    if match == '':
        # so the result is true
        result = True
    # if there is still some string left
    else:
        # then its not a match
        result = False
    # send the answer back to the user
    return result


def ex7_perms(regex):
    '''(str) -> set of str
    Takes in a string and returns all the
    possible permutations of that string
    >>> ex7_perms('cat')
    ['cat', 'cta', 'act', 'atc', 'tca', 'tac']
    >>> ex7_perms('cs')
    ['cs', 'sc']
    >>> ex7_perms('112')
    ['112', '121', '112', '121', '211', '211']
    >>> ex7_perms('.|..')
    ['.|..', '.|..', '..|.', '...|', '..|.', '...|', '|...', '|...', '|...',
    '|...', '|...', '|...', '.|..', '.|..', '..|.',
    '...|', '..|.', '...|', '.|..', '.|..', '..|.', '...|', '..|.', '...|']
    '''
    # instatiate result
    result = []
    # base case, if were down to one letter
    if len(regex) == 1:
        # add the regular word
        result.append(regex)
    # if we're still going through letters
    else:
        # go through each letter in the word
        for i in regex:
            # go through every possibility of other letters
            for j in ex7_perms(regex[:regex.index(i)] +
                               regex[regex.index(i) + 1:]):
                # add the permutation to the set
                result.append(i + j)
    # return the set of words
    return result


def add_brackets(pos_list):
    ''' (list) -> list
    Returns a list of every possible combination
    of 2 ternary values and 1 symbol at each given
    index. It treats anything covered with brackets
    as a ternary value
    >>> add_brackets(['1.0.e'])
    ['(1.0).e', '1.(0.e)']
    >>> add_brackets(['(1.0).e', '1.(0.e)'])
    ['((1.0).e)', '(1.(0.e))']
    >>> add_brackets(['1.0'])
    ['(1.0)']
    '''
    # make a blank list to append all the possible
    # brackets spots to
    possible = []
    # go through the list
    for i in pos_list:
        # instantiate vars
        # counter will count how many usable
        # values it has passed
        counter = 0
        # start index will tell us where to slice the
        # string for
        start = 0
        # index will tell us where to slice to
        index = 0
        # this will be the start value if we need to
        # start to the left of a bracket
        b_start = -1
        # this will tell us how many right brackets we need
        # to pass to add the brackets
        brackets = 0
        # while the index is still usable
        while index < len(i):
            # if we pass a left bracket
            if i[index] == '(':
                # if the bracket starting value hasnt been set
                if b_start == -1:
                    # set the bracket starting value to the
                    # current index
                    b_start = index
                # we need to pass one more right bracket
                brackets += 1
            # if we pass a right bracket
            elif i[index] == ')':
                # number of right brackets we need to pass goes down
                brackets -= 1
            # if we dont need to pass any brackets
            if brackets == 0:
                # its a usable value, so increase usable counter value
                counter += 1
                # if we've pass three usable values
                if counter == 3:
                    # wrap them in brackets
                    val = (i[:start] +
                           '(' + i[start:index + 1] + ')' + i[index + 1:])
                    # append to the possible bracket combinations
                    possible.append(val)
                    # if we didnt start from a bracket
                    if b_start == -1:
                        # we'll start from the current index now
                        start = index
                    # if we did start from a bracket
                    else:
                        # we'll start from that bracket
                        start = b_start
                        # and we'll reset the bracket start
                        b_start = -1
                    # finally, usable value counter goes back to 1
                    counter = 1
            # icrease the index
            index += 1
    # return all the possible bracket combos
    return possible


def all_regex_permutations(rand_str):
    ''' (str) -> set
    Takes any string at all, and returns a set
    of all the permutations of that string that
    are a valid regex
    >>> all_regex_permutations('(1).0')
    {'(1.0)', '(0.1)'}
    >>> all_regex_permutations('e')
    {'e'}
    >>> all_regex_permutations('2********')
    {'2********'}
    >>> all_regex_permutations('()0|*1')
    {'(1|0*)', '(0|1)*', '(0*|1)', '(0|1*)', '(1*|0)', '(1|0)*'}
    all_regex_permutations('(0|1).e)(')
    {'(0|(e.1))', '((0.1)|e)', '(0.(1|e))', '((0|1).e)', '((1|e).0)',
    '(1|(0.e))', '(0.(e|1))', '(1.(e|0))', '((e|1).0)', '(e|(0.1))',
    '((1.e)|0)', '((1|0).e)', '(1|(e.0))', '((1.0)|e)',
    '((0|e).1)', '((0.e)|1)', '((e.1)|0)','(e.(1|0))', '(0|(1.e))',
    '((e|0).1)', '((e.0)|1)', '(e.(0|1))', '(e|(1.0))', '(1.(0|e))'}
    '''
    # instiate the perms and result
    perms = set()
    star_perms = []
    result = None
    # make regex a string to hold tern values and a string
    # to hold symbols
    terns = ''
    symbols = ''
    # also number of stars counter
    num_stars = 0
    # check if its a single ternary value, and a tern value
    # with stars after it
    if (len(rand_str) == 1 and rand_str in ['1', '2', '0', 'e'] or
            rand_str[1:].count('*') == len(rand_str[1:])):
        # its the only permutation
        perms = set({rand_str})
        # dont make it run the second part of the
        # algorithm
        result = perms
    # first we'll check some simple stuff
    # like if there'rand_str the same number of left and right brackets
    # same number of brackets as the are bars or dots
    # also check if it doesnt have any brackets to begin with
    if (rand_str.count('(') != rand_str.count(')') or (len(rand_str) > 1 and
                                                       '*' not in rand_str and
                                                       ('(' not in rand_str or
                                                        ')' not in rand_str))):
        # blank set, no need to perm it
        result = perms
    # no we'll check if there are  any values that shouldn't be in there
    # and fill our lists while doing it
    # go through the string
    for i in rand_str:
        # check for bad values
        if i not in ['1', '2', '0', 'e', '.', '|', '*', '(', ')']:
            # then it won't ever be valid
            result = perms
        # if were not at a bad value
        else:
            # check if the value should go in terns
            if i in ['1', '0', '2', 'e']:
                # add it to terns
                terns += i
            # check if the value should go in symbols
            if i in ['.', '|']:
                # add it to our list of symbols
                symbols += i
    # now we'll check if it might actually work
    if result != perms:
        # get the number of starts
        num_stars = rand_str.count('*')
        # we'll get a list of all of ther perms of the terns
        tern_perms = ex7_perms(terns)
        # and a list of all the perms of the symbols
        symbol_perms = ex7_perms(symbols)
        # make a blank list framework, and a blank
        # list to hold all the perms
        framework = []
        perms = []
        # now we'll go through the tern perms
        for i in tern_perms:
            # go through the symbols perms
            for j in symbol_perms:
                # make a blank str
                new = ''
                # and go through each char
                for char in range(len(j)):
                    # add the symbols to the tern perm
                    new += i[char] + j[char]
                # add the end value
                new = new + (i[-1])
                # append it to the framework list
                framework.append(new)
        # now we have a frame work, which is basically
        # a list of all possible terns and symbols together

        # now we'll go through the framework
        for i in framework:
            # we'll put the index of i into a holder var
            holder = [i]
            # we go through it the amount of times it takes to
            # get the right amount of brackets
            for j in range(len(i) // 2):
                # add brackets to each element in the holder
                holder = add_brackets(holder)
            # once we go through all of them, we have the right
            # amount of brackets, so we can add it to the perms
            perms += holder
    # check if there are stars
    if num_stars != 0:
        # put perms in the holder
        holder = []
        star_perms = perms
        j = 0
        # do once for each star
        for i in range(num_stars):
            # go through each element in the holder
            while j < len(star_perms):
                # go through the string at i
                for k in star_perms[j]:
                    # check if a star can go after it
                    if k not in ['(', '.', '|']:
                        # add a star in, append that to the holder
                        holder.append(star_perms[j][:star_perms[j].index(
                            k) + 1] + '*' +
                            star_perms[j][star_perms[j].index(k) + 1:])
                # increment the counter
                j += 1
            # reset the counter
            j = 0
            # push all the holder perms into star perms
            star_perms = holder
            # clear the holder
            holder = []
    # check if star perms was used
    if star_perms != []:
        # set all the perms to that
        perms = star_perms
    # return it
    # that was tiring
    return set(perms)
