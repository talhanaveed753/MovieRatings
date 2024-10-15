#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 13:32:10 2023

@author: macbook_user
"""

from project2Phase1a import *

tests = []

# tests for createUserList
userList = createUserList()
# Test 1
tests.append(len(userList) == 943)
# Test 2
tests.append(userList[10]["occupation"] == 'other')
# Test 3
tests.append(sorted([str(x) for x in userList[55].values()]) == ['25', '46260', 'M', 'librarian'])
# Test 4
tests.append(len([x for x in userList if x["gender"]=="F"]) == 273)
# Test 5
tests.append(sorted(list(userList[10].keys())) == ['age', 'gender', 'occupation', 'zip'])
# Test 6
tests.append([type(userList[5][x]) for x in ['age', 'gender', 'occupation', 'zip']] == [int, str, str, str])


# tests for createMovieList
movieList = createMovieList()
# Test 7
tests.append(len(movieList) == 1682)
# Test 8
tests.append(movieList[27]["title"] == 'Apollo 13 (1995)')
# Test 9
tests.append(movieList[78]["title"].split("(")[0] == 'Fugitive, The ')
# Test 10
tests.append(sorted([x for x in movieList[1657].values() if type(x) == str]) == ['', '06-Dec-1996', 'Substance of Fire, The (1996)', 'http://us.imdb.com/M/title-exact?Substance%20of%20Fire,%20The%20(1996)'])
# Test 11
tests.append(movieList[88]["title"] == 'Blade Runner (1982)')
# Test 12
tests.append(sorted(movieList[10].keys()) == ['IMDB url', 'genre', 'release date', 'title', 'video release date'])
# Test 13
tests.append([type(movieList[11][x]) for x in sorted(movieList[10].keys())] == [str, list, str, str, str])
# Test 14
tests.append(movieList[11]['genre'] == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])

# tests for readRatings
rawRatings = readRatings()
# Test 15
tests.append(rawRatings[:2] == [(196, 242, 3), (186, 302, 3)])
# Test 16
tests.append(len(rawRatings) == 100000)
# Test 17
tests.append(len([x for x in rawRatings if x[0] == 1]) == 272)
# Test 18
tests.append(len([x for x in rawRatings if x[0] == 2]) == 62)
# Test 19
tests.append(sorted([x for x in rawRatings if x[0] == 2][:11]) == [(2, 13, 4), (2, 50, 5), (2, 251, 5), (2, 280, 3), (2, 281, 3), (2, 290, 3), (2, 292, 4), (2, 297, 4), (2, 303, 4), (2, 312, 3), (2, 314, 1)])
# Test 20
tests.append([x for x in rawRatings if x[1] == 1557] == [(405, 1557, 1)])

# tests for createRatingDataStructure
numUsers = len(userList)
numMovies = len(movieList)
[rLu, rLm] = createRatingsDataStructure(numUsers, numMovies, rawRatings)
# Test 21
tests.append(len(rLu) == 943)
# Test 22
tests.append(len(rLm) == 1682)
# Test 23
tests.append(len(rLu[0]) == 272)
# Test 24
tests.append(min([len(x) for x in rLu]) == 20)
# Test 25
tests.append(min([len(x) for x in rLm]) == 1)
# Test 26
tests.append(sorted(rLu[18].items()) == [(4, 4), (8, 5), (153, 4), (201, 3), (202, 4), (210, 3), (211, 4), (258, 4), (268, 2), (288, 3), (294, 3), (310, 4), (313, 2), (319, 4), (325, 4), (382, 3), (435, 5), (655, 3), (692, 3), (887, 4)])
# Test 27
tests.append(len(rLm[88]) == 275)
# Test 28
tests.append(rLu[10][716] == rLm[715][11])
# Test 29
tests.append([m for m in range(1, numMovies+1) if m in rLu[0] and m in rLu[417]] == [258, 269])
# Test 30
tests.append(rLu[0][258] == 5)
# Test 31
tests.append(rLu[417][258] == 5)
# Test 32
tests.append(rLu[0][269] == 5)
# Test 33
tests.append(rLu[417][269] == 5)

# tests for createGenreList
genreList = createGenreList()
# Test 34
tests.append(genreList == ['unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir','Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

# Output the test results
i = 0
for result in tests:
    if not result:
        print("Test", i + 1, "failed")
    i = i + 1