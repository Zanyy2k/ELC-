# Lexicon - Based Sentiment Analysis

# Load in the required files 
setwd("C:/Users/zyu/Desktop/SocialMedia_Analysis")
JML_Yelp <- read.csv("C:/Users/zyu/Desktop/SocialMedia_Analysis/JML_Yelp.csv")
# Positive and negative words
pos.raw = scan('positive_words.txt', what = 'character', sep = ',')
neg.raw = scan('negative_words.txt', what = 'character', sep = ',')
trimws(pos.raw) #Remove white space head and tail
trimws(neg.raw) #Remove white space head and tail

# Select the review column
Yelp_Reviews = JML_Yelp$Reviews
View(Yelp_Reviews)

for(i in Yelp_Reviews){
  print(i)
  sentence = gsub('<p lang=\"en\">','',i)
  
  print(sentence)
}


