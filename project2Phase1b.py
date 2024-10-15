###########################################################################################################
#
# Creating the data structures
#
###########################################################################################################


# User demographic information: {age, gender, occupation, zip}
def createUserList():
    
    userList = []
    f = open("u.user")
    
    for line in f:
        
        userInfo = line.strip().split('|')
        userDict = {"age": int(userInfo[1]), "gender": userInfo[2], "occupation": userInfo[3], "zip": userInfo[4]}
        userList.append(userDict)
        
    f.close()
    
    return userList



# Movies information: {title, release date, video release date, IMDB url, genre}
def createMovieList():
    
    movieList = []
    f = open("u.item")
    
    for line in f:
        
        movieInfo = line.strip().split('|')
        movieDict = {"title": movieInfo[1], "release date": movieInfo[2], "video release date": movieInfo[3], "IMDB url": movieInfo[4], "genre": [int(x) for x in movieInfo[5:]]}
        movieList.append(movieDict)
        
    f.close()
    
    return movieList



# First fucntion in processing the ratings
def readRatings():
    
    ratings = []
    f = open("u.data")
    
    i = 0
    line = f.readline()
    
    while line and i < 100000:
        
        values = line.split()
        user = int(values[0])
        movie = int(values[1])
        rating = int(values[2])

        ratings.append((user, movie, rating))
        line = f.readline()
        
        i = i + 1
        
    f.close()
    
    return ratings

# Second function for processing the ratings
def createRatingsDataStructure(numUsers, numMovies, ratingTuples):
    
    rLu = [{} for i in range(numUsers)]
    rLm = [{} for i in range(numMovies)]
    
    for user, movie, rating in ratingTuples:
        
        rLu[user-1][movie] = rating
        rLm[movie-1][user] = rating
        
    return [rLu, rLm]



# Movie genres list
def createGenreList():
    
    genres = []
    f = open("u.genre")
    
    for line in f:
        
        genre = line.strip().split('|')[0]
        
        if genre != '':
            
            genres.append(genre)
        
    f.close()
    
    return genres

###########################################################################################################
#
# Data exploration function
#
###########################################################################################################

def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):
    
    fractions = []
    subpopulation = []
    
    i = 0
    for user in userList:
        
        if (gender != "A"):
            
            if (user["gender"] == gender) and ((user["age"] >= ageRange[0]) and (user["age"] < ageRange[1])):
                
                subpopulation.append(i)
                
        elif ((user["age"] >= ageRange[0]) and (user["age"] < ageRange[1])):
            
                subpopulation.append(i)
        i = i + 1
        
    genreCountsRated = [0] * 19
    genreCountsTotal = 0
    
    for user in subpopulation:
        
        for movie, rating in rLu[user].items():
            
            genreCountsTotal = genreCountsTotal + 1
            genres = movieList[movie-1]["genre"]
            
            i = 0
            for genre in genres:
                
                if genre == 1:
                    
                    if rating >= ratingRange[0] and rating <= ratingRange[1]:
                        
                        genreCountsRated[i] += 1
                i = i + 1

    for i in range(1, 20):
        
        if genreCountsTotal == 0:
            
            fractions.append(None)
        else:
            
            fractions.append(genreCountsRated[i-1] / genreCountsTotal)

    return fractions

###########################################################################################################
#
# Making the visualizations
#
###########################################################################################################

def main():
    
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    
    userList = createUserList()
    movieList = createMovieList()
    rawRatings = readRatings()
    numUsers = len(userList)
    numMovies = len(movieList)
    [rLu, rLm] = createRatingsDataStructure(numUsers, numMovies, rawRatings)
    genreList = createGenreList()
    
    # Plot 1 (High Ratings)
    maleHighRatings = demGenreRatingFractions(userList, movieList, rLu, "M", [1, 100], [4, 5])
    femaleHighRatings = demGenreRatingFractions(userList, movieList, rLu, "F", [1, 100], [4, 5])
    
    genres = (genreList[1], genreList[5], genreList[8], genreList[11], genreList[14])
    ratingFraction = {
        'Male': (maleHighRatings[1], maleHighRatings[5], maleHighRatings[8], maleHighRatings[11], maleHighRatings[14]),
        'Female': (femaleHighRatings[1], femaleHighRatings[5], femaleHighRatings[8], femaleHighRatings[11], femaleHighRatings[14]),
        }

    x = np.arange(len(genres))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in ratingFraction.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fraction')
    ax.set_title('Male VS Female High Movie Ratings')
    ax.set_xticks(x + width, genres)
    ax.legend(loc='upper left', ncols=3)
    ax.yaxis.set_ticks(np.arange(0, 0.4, 0.1))
    ax.set_ylim(0, 0.4)

    plt.show()
    
    # Plot 2 (Low Ratings)
    maleLowRatings = demGenreRatingFractions(userList, movieList, rLu, "M", [1, 100], [1, 2])
    femaleLowRatings = demGenreRatingFractions(userList, movieList, rLu, "F", [1, 100], [1, 2])
    
    genres = (genreList[1], genreList[5], genreList[8], genreList[11], genreList[14])
    ratingFraction = {
        'Male': (maleLowRatings[1], maleLowRatings[5], maleLowRatings[8], maleLowRatings[11], maleLowRatings[14]),
        'Female': (femaleLowRatings[1], femaleLowRatings[5], femaleLowRatings[8], femaleLowRatings[11], femaleLowRatings[14]),
        }

    x = np.arange(len(genres))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in ratingFraction.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fraction')
    ax.set_title('Male VS Female Low Movie Ratings')
    ax.set_xticks(x + width, genres)
    ax.legend(loc='upper left', ncols=3)
    ax.yaxis.set_ticks(np.arange(0, 0.1, 0.025))
    ax.set_ylim(0, 0.1)

    plt.show()
    
    # Plot 3 (Younger Adults)
    youngerMaleRatings = demGenreRatingFractions(userList, movieList, rLu, "M", [20, 30], [1, 5])
    youngerFemaleRatings = demGenreRatingFractions(userList, movieList, rLu, "F", [20, 30], [1, 5])
    
    genres = (genreList[1], genreList[5], genreList[8], genreList[11], genreList[14])
    ratingFraction = {
        'Male': (youngerMaleRatings[1], youngerMaleRatings[5], youngerMaleRatings[8], youngerMaleRatings[11], youngerMaleRatings[14]),
        'Female': (youngerFemaleRatings[1], youngerFemaleRatings[5], youngerFemaleRatings[8], youngerFemaleRatings[11], youngerFemaleRatings[14]),
        }

    x = np.arange(len(genres))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in ratingFraction.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fraction')
    ax.set_title('Younger Male VS Younger Female Movie Ratings')
    ax.set_xticks(x + width, genres)
    ax.legend(loc='upper left', ncols=3)
    ax.yaxis.set_ticks(np.arange(0, 0.5, 0.1))
    ax.set_ylim(0, 0.5)

    plt.show()
    
    # Plot 4 (Older Adults)
    olderMaleRatings = demGenreRatingFractions(userList, movieList, rLu, "M", [50, 60], [1, 5])
    olderFemaleRatings = demGenreRatingFractions(userList, movieList, rLu, "F", [50, 60], [1, 5])
    
    genres = (genreList[1], genreList[5], genreList[8], genreList[11], genreList[14])
    ratingFraction = {
        'Male': (olderMaleRatings[1], olderMaleRatings[5], olderMaleRatings[8], olderMaleRatings[11], olderMaleRatings[14]),
        'Female': (olderFemaleRatings[1], olderFemaleRatings[5], olderFemaleRatings[8], olderFemaleRatings[11], olderFemaleRatings[14]),
        }

    x = np.arange(len(genres))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in ratingFraction.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('fraction')
    ax.set_title('Older Male VS Older Female Movie Ratings')
    ax.set_xticks(x + width, genres)
    ax.legend(loc='upper left', ncols=3)
    ax.yaxis.set_ticks(np.arange(0, 0.6, 0.1))
    ax.set_ylim(0, 0.6)

    plt.show()
    







