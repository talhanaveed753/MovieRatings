# Programmer: Talha Naveed
# Date: May 1, 2023

# matplotlib.pyplot is needed for creating plots
import matplotlib.pyplot as plt
import random
import math

##############################################################################
#
# The next two functions were written by my PhD student Hankyu Jang. The function
# plot_grouped_bar_chart is based on the example in the matplotlob documentation
# on creating a bar plot by groups. 
#
##############################################################################

def add_to_all_elements_in_list(list1, val):
    return [elem+val for elem in list1]

def plot_grouped_bar_chart(data, label_tuple, title, ylabel):
    x = [val for val in range(len(label_tuple))]  # the label locations
    width = 1/(len(data)+1)  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots()

    for attribute, measurement in data.items():
        offset = width * multiplier
        rects = ax.bar(add_to_all_elements_in_list(x, offset), measurement, width, label=attribute)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(add_to_all_elements_in_list(x, width), label_tuple)
    # ax.legend(loc='upper left', ncols=3)
    ax.legend(loc='best')
    # ax.set_ylim(0, 250)
    y_max = max([max(v) for k,v in data.items()])
    ax.set_ylim(0, y_max*1.2)

    plt.show()

##############################################################################
# Reads information about users from the file u.user. This information is stored as a list dictionaries and returned.
# Each dictionary has keys "age", "gender", "occupation", and "zip". The dictionary for user i is stored in slot i-1.
##############################################################################
def createUserList():
    fusers = open("ml-100k/u.user", "r")

    userList = []
    for line in fusers:
        userInfo = line.strip().split("|")
        userList.append({"age": int(userInfo[1]), "gender": userInfo[2], "occupation": userInfo[3], "zip": userInfo[4]})

    fusers.close()
    return userList

##############################################################################
# Reads information about users from the file u.item. This information is stored as a list dictionaries and returned.
# Each dictionary has keys "title", "release date", "video release date", "IMDB url", and "genre". The dictionary for movie i
# is stored in slot i-1.
##############################################################################
def createMovieList():
    fitems = open("ml-100k/u.item", "r", encoding="windows-1252")
    itemList = []
    for line in fitems:
        itemInfo = line.strip().split("|")
        itemList.append({"title": itemInfo[1], "release date": itemInfo[2], "video release date": itemInfo[3], "IMDB url": itemInfo[4],
                     "genre": [int(x) for x in itemInfo[5:]]})

    fitems.close()
    return itemList

# This function reads the file u.genre for the names of genres.
def createGenreList():
    f = open("ml-100k/u.genre", "r")

    L = []
    for line in f:
        L.append(line.split("|")[0])

    f.close()
    return L

##############################################################################
# Read ratings from a file u.data. Each rating line consisting of a user, movie, and rating are turned into a length-3 int tuple.
# A list of 100,000 such ratings is returned. The timestamps that appear in each rating are ignored. 
##############################################################################
def readRatings():
    ratings = []
    f = open("ml-100k/u.data", "r")

    for line in f:
        data = tuple([int(x) for x in line.split()][:3])
        ratings.append(data)

    f.close()
    return ratings
   
##############################################################################
# This function is given a bunch of ratings in the form of a list of (user, movie, rating)-tuple.
# It then creates two data structures, one from the point of view of users and one from the point of view of movies. 
# In addition, the function takes the number of users and movies as parameters and uses these to appopriately initialize
# the rating lists.
##############################################################################
def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    # Initialization of rating lists
    ratingsList1 = []
    ratingsList2 = []
    for i in range(numUsers):
        ratingsList1.append({})

    for i in range(numItems):
        ratingsList2.append({})

    # Read each line in the rating file and store it in each 
    # of the two data structures
    for rating in ratingTuples:
        ratingsList1[rating[0]-1][rating[1]] = rating[2]
        ratingsList2[rating[1]-1][rating[0]] = rating[2]
    
    return [ratingsList1, ratingsList2]


##############################################################################
#
# This function takes demographic information given by gender and ageRange. It
# identifies the subpopulation of users that have the given gender and fall within
# the given ageRange. For each movie genre, the function computes the number N of ratings
# in the range ratingsRange provided by this subpopulation for movies in that genre. 
# It then returns the fraction, which is N dividied by the total number
# of ratings provided by all the users in this subpopulation. It returns this 
# fraction for the 19 genres as a length-19 list of floating points.
#
##############################################################################
def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):
    
    # Initialize the numerators and denominator of the to-be-computed fractions for all 19 genres
    numGenres = len(movieList[0]["genre"])
    numerator = [0]*numGenres
    denominator = 0
    
    # Walk down the user IDs, keeping in mind that they range from 1 through numUsers
    for i in range(len(userList)):
        
        # Check if this user fits the demographic constraints
        # If gender is "A", it does not matter what the user's gender is. 
        # Note that the user's age has to be strictly less than ageRange[1] for the user to qualify
        if ((gender == "A") or (userList[i]["gender"] == gender)) and (ageRange[0] <= userList[i]["age"] < ageRange[1]):
            
            # Update denominator by the number of movies this user has rated
            denominator = denominator + len(rLu[i])
            
            # Walk down the ratings provided by this user by using the provided ratings list rLu
            for movie in rLu[i]:
                
                # Store the rating user i+1 provides to movie in a variable called rating
                rating = rLu[i][movie]
                
                # Check if this rating is in the given range
                if (ratingRange[0] <= rating <= ratingRange[1]):
                
                    # movieList[movie-1] contains 19 bits representing the genres
                    # For each genre, update the denominator and if in rating range,
                    # update the numerator as well
                    j = 0
                    for bit in movieList[movie-1]["genre"]:
                        numerator[j] = numerator[j] + bit
                        j = j + 1
                       
    return [numerator[i]/denominator if denominator > 0 else None for i in range(len(numerator))]
    
###############################################################################
#
# project2Phase2
#
###############################################################################


# return a random integer
def randomPrediction(u, m):
    return random.randint(1, 5)

# return the mean of all ratings this user has given to movies
def meanUserRatingPrediction(u, m, rLu):
    
    userRatingsList = rLu[u - 1]
    meanRatings = 0
    
    ratings = userRatingsList.values()
    meanRatings = sum(ratings) / len(ratings)
    return meanRatings

# return the mean rating this movie has recieved
def meanMovieRatingPrediction(u, m, rLm):
    
    movieRatingsList = rLm[m - 1]
    meanRatings = 0
    
    ratings = movieRatingsList.values()
    
    if len(ratings) == 0 :
        return None
    meanRatings = sum(ratings) / len(ratings)
    return meanRatings

# return the mean of all similar dem ratings for that movie
def demRatingPrediction(u, m, userList, rLu):
    # Find users in U who have the same gender as u and age within ±5 years
    U = []
    i = 0
    gender = userList[u - 1]["gender"]
    age = userList[u - 1]["age"]
    
    for user in userList:
        if (i != (u - 1)) and (user['gender'] == gender) and ((user['age'] <= age + 5) and (user['age']) >= age - 5):
            U.append(i)
        i = i + 1
    # Compute mean rating of users in U for movie m
    ratings = []
    for user in U:
        if m in rLu[user]:
            ratings.append(rLu[user][m])
    if len(ratings) > 0:
        return sum(ratings) / len(ratings)
    else:
        return None

# return the mean of all similar genre ratings for that movie genre
def genreRatingPrediction(u, m, movieList, rLu):
    
   # Find movies in M that have the same genre as movie m
   genre1 = movieList[m - 1]["genre"]
   M = []
   i = 0
   for movie in movieList:
       if movie != movieList[m - 1]:
           j = 0
           genre2 = movie["genre"]
           while j < 19:
               if (genre2[j] == genre1[j]):
                       if genre2[j] == 1:
                           M.append(i + 1)
                           break
               j = j + 1
       i = i + 1
    
   # Compute mean rating of user u for movies in M
   ratings = []
   for movie in M:
       
       if movie in rLu[u - 1]:
           ratings.append(rLu[u - 1][movie])
   if len(ratings) > 0:
       return sum(ratings) / len(ratings)
   else:
       return None


# training set
def partitionRatings(rawRatings, testPercent):
    # Deepcode the raw ratings to ensure consistency of the data.
    deepcodedRatings = []
    for rating in rawRatings:
        deepcodedRating = (rating[0], rating[1], int(rating[2]))
        deepcodedRatings.append(deepcodedRating)
    rawRatings = deepcodedRatings

    numTest = int(len(rawRatings) * (testPercent / 100))

    # Shuffle the raw ratings.
    random.shuffle(rawRatings)

    # Split the ratings into training and test sets.
    testSet = []
    trainingSet = []
    for i in range(numTest):
        testSet.append(rawRatings[i])
    for i in range(numTest, len(rawRatings)):
        trainingSet.append(rawRatings[i])

    # Return the partitioned sets.
    return [trainingSet, testSet]

# testing set
def rmse(actualRatings, predictedRatings):
    
    T = 0
    numerator = 0
    newPredictedRatingList = []
    newActualRatingsList = []
    n = len(predictedRatings)
    
    i = 0
    while i < n:
        if predictedRatings[i] != None:
            newPredictedRatingList.append(predictedRatings[i])
            newActualRatingsList.append(actualRatings[i])
        i = i + 1
  
    
    for j in range(len(newActualRatingsList)):
        differenceSquared = (newActualRatingsList[j] - newPredictedRatingList[j]) ** 2
        numerator = numerator + differenceSquared
        T = T + 1

    if T == 0:
        return None
    
    mean = numerator / T
    
    return mean ** (1/2)

# plot function
def draw_boxplot(data, labels):
    plt.boxplot(x=data, labels=labels)
    plt.title("Algorithm performance comparison")
    plt.ylabel("RMSE values")
    plt.show()
    plt.close()

def main():
    userList = createUserList()
    movieList = createMovieList()
    ratingTuples = readRatings()
    numUsers = len(userList)
    numItems = len(movieList)
    
    # initialize empty lists to capture the predicted ratings

    random = []
    meanUser = []
    meanMovie = []
    dem = []
    genre = []
    actual = []
    algo1 = []
    algo2 = []
    algo3 = []
    algo4 = []
    algo5 = []
    
    
    for i in range (0,10):
        [trainingSet, testSet] = partitionRatings(ratingTuples, 20)
        [trainingRLu, trainingRLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)

        for tuple in testSet:
            actual.append(tuple[2])
            random.append(randomPrediction(tuple[0], tuple[1]))
            meanUser.append(meanUserRatingPrediction(tuple[0], tuple[1], trainingRLu))
            meanMovie.append(meanMovieRatingPrediction(tuple[0], tuple[1], trainingRLm))
            dem.append(demRatingPrediction(tuple[0], tuple[1], userList, trainingRLu))
            genre.append(genreRatingPrediction(tuple[0], tuple[1], movieList, trainingRLu))
        algo1.append(rmse(actual, random))
        algo2.append(rmse(actual, meanUser))
        algo3.append(rmse(actual, meanMovie))
        algo4.append(rmse(actual, dem))
        algo5.append(rmse(actual, genre))
    data = [algo1, algo2, algo3, algo4, algo5]
    labels = ["Algo1", "Algo2", "Algo3", "Algo4", "Algo5"]
    draw_boxplot(data, labels)
    return
     









