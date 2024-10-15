####################################################################################################
#
# Creating the data structures
#
####################################################################################################


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

####################################################################################################
#
# Data exploration function
#
####################################################################################################

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

