import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.tweetString = ""

    def DownloadData(self):
        # authenticating
        consumerKey = '4TGPfg62pT76yWTnTE8INjJCL'
        consumerSecret = 'dkhHybaFTIAflvCVB5vFHQPu0eCHFQN1BIbpdx3hjt8q3aRqWy'
        accessToken = '3061686882-PrrngsYGKlMV92KseseATs1Gjr5Yyucry61Lwl2'
        accessTokenSecret = 'aLOiD62JKQg29mSoz6chfpLP7fbBpG4syMuaUvlAqe9J0'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            self.tweetString = self.tweetString + tweet.text

            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.polarity > 0 and analysis.polarity <= 0.3):
                wpositive += 1
            elif (analysis.polarity > 0.3 and analysis.polarity <= 0.6):
                positive += 1
            elif (analysis.polarity > 0.6 and analysis.polarity <= 1):
                spositive += 1
            elif (analysis.polarity > -0.3 and analysis.polarity <= 0):
                wnegative += 1
            elif (analysis.polarity > -0.6 and analysis.polarity <= -0.3):
                negative += 1
            elif (analysis.polarity > -1 and analysis.polarity <= -0.6):
                snegative += 1

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        plt.figure(figsize=(20,8))
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing recent Tweets.')
        plt.subplot(1,2,1)
        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
        plt.subplot(1,2,2)
        self.wordCloud()
        plt.show()

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        # plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()

    def wordCloud(self):

        cloud = WordCloud(background_color="white").generate(str(self.tweetString))
        plt.imshow(cloud)
        plt.axis('off')

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
