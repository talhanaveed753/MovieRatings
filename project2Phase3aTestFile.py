from project2Phase3a import *

#main program
# Read and store in data structures
userList = createUserList()
numUsers = len(userList)
movieList = createMovieList()
numMovies = len(movieList)
rawRatings = readRatings()
[rLu, rLm] = createRatingsDataStructure(numUsers, numMovies, rawRatings)

tests = []

# Tests for similarity

# Test 1
tests.append(similarity(1, 1, rLu) == 1.0)

# Test 2
tests.append(similarity(1, 2, rLu) == 0.36087078613390927)

# Test 3
tests.append(similarity(1, 3, rLu) == 0.1572278924080942)

# Test 4
tests.append(similarity(2, 1, rLu) == 0.3608707861339095)

# Test 5
tests.append(similarity(2, 2, rLu) == 1.0)

# Test 6
tests.append(similarity(2, 3, rLu) == 0.13955602954011728)

# Test 7
tests.append(similarity(3, 1, rLu) == 0.1572278924080942)

# Test 8
tests.append(similarity(3, 2, rLu) == 0.13955602954011723)

# Test 9 
tests.append(similarity(3, 3, rLu) == 1.0)

# -------------
# Tests for k-nearest neighbors

# Test 10
# User 1 k nearest neighbors for k = 1..10
tests.append(kNearestNeighbors(1, rLu, 10) == [(418, 1.0000000000000002), (155, 1.0), (341, 1.0), (685, 1.0), (812, 0.9999239260769993), (351, 0.9964428433410024), (811, 0.9881231817211082),(166, 0.9807552329510851), (810, 0.9009590923599005), (309, 0.8944271909999159)])

# Test 11
# User 2 k nearest neighbors for k = 1..10
tests.append(kNearestNeighbors(2, rLu, 10) == [(51, 1.0), (98, 1.0), (289, 1.0), (366, 1.0), (522, 1.0), (700, 1.0),(778, 1.0), (912, 1.0), (369, 0.9999999999999998), (114, 0.9984871757166689)])

# Test 12
# User 3 k nearest neighbors for k = 1..10
tests.append(kNearestNeighbors(3, rLu, 10) == [(5, 1.0), (41, 1.0), (51, 1.0), (55, 1.0), (96, 1.0), (106, 1.0), (138, 1.0), (148, 1.0), (182, 1.0), (187, 1.0)])

# -------------
# Tests for CFRatingPrediction

# Test 13
# User = 1 Friends= 10 nearest neighbors Movie = 1 CF Rating Prediction =
# 3.610294117647059
tests.append(CFRatingPrediction(1, 1, rLu, kNearestNeighbors(1, rLu, 10)) == 3.610294117647059)

# Test14
# User = 1 Friends= 10 nearest neighbors Movie = 2 CF Rating Prediction =
# 3.610294117647059
tests.append(CFRatingPrediction(1, 2, rLu, kNearestNeighbors(1, rLu, 10)) == 3.610294117647059)

# Test 15
# User = 1 Friends= 20 nearest neighbors Movie = 1 CF Rating Prediction =
# 4.391544117647059
tests.append(CFRatingPrediction(1, 1, rLu, kNearestNeighbors(1, rLu, 20)) == 4.391544117647059)

# Test 16
# User = 1 Friends= 20 nearest neighbors Movie = 2 CF Rating Prediction =
# 3.610294117647059
tests.append(CFRatingPrediction(1, 2, rLu, kNearestNeighbors(1, rLu, 20)) == 3.610294117647059)

# Test 17
# User = 2 Friends= 10 nearest neighbors Movie = 1 CF Rating Prediction =
# 3.7837514934289125
tests.append(CFRatingPrediction(2, 1, rLu, kNearestNeighbors(2, rLu, 10)) == 3.7837514934289125)

# Test 18
# User = 2 Friends= 10 nearest neighbors Movie = 2 CF Rating Prediction =
# 3.7096774193548385
tests.append(CFRatingPrediction(2, 2, rLu, kNearestNeighbors(2, rLu, 10)) == 3.7096774193548385)

# Test 19
# User = 2 Friends= 20 nearest neighbors Movie = 1 CF Rating Prediction =
# 4.08806779512875
tests.append(CFRatingPrediction(2, 1, rLu, kNearestNeighbors(2, rLu, 20)) == 4.08806779512875)

# Test 20
# User = 2 Friends= 20 nearest neighbors Movie = 2 CF Rating Prediction =
# 2.774542284219703
tests.append(CFRatingPrediction(2, 2, rLu, kNearestNeighbors(2, rLu, 20)) == 2.774542284219703)



i = 0
for result in tests:
    if not result:
        print("Test", i + 1, "failed")
    i = i + 1
    if len(tests) == 0:
        print("congrajulashins!")