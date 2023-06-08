# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 20:13:12 2022

@author: Richard and Flora
Title: Sentimental Analysis
Summary: Gets sentimental analysis of words from JSON file YELP reviews 
"""
import json
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
import csv



lem = nltk.WordNetLemmatizer()
text_and_star = {}
words_and_rating = {}
sorted_text_and_rating = {}
stop_words = set(stopwords.words('english'))
english_dic = set(words.words('en'))



def main():             #open and read from file
    with open('yelp_academic_dataset_review_small.json') as f:
        data = json.load(f)
        for review in data:
           
            #get star value and review text from data
            star = review['stars']
            text = review['text'].lower()
          
            
            
            #tokenize text
            tokenized_words = set(nltk.word_tokenize(text))
            
            #lemmatize words
            lemmatized_words = [lem.lemmatize(word) for word in tokenized_words]
            
           
            #put only non stop words and numbers into a set(faster look up time) called english_words, create the set of the stopword and english word beofre the loop, else it will create a set for each loop iteration
            english_words = set([word for word in lemmatized_words if word not in stop_words and word in english_dic])
           
           
            #loop through english_words
            for word in english_words:
                #add word if the word is not in text_and_star, dictionary do not need to use keys() fuction
                if word not in text_and_star:
                   
                    #we create key for the word and give it 5 values, it's appearence ranging from 1 star to 5
                    text_and_star[word] = [0,0,0,0,0]
                    
               #if the word already exist in the dictionary, increment depending on rating, outside of if statement to save memory
                text_and_star[word][star-1] += 1
           
            #loop through the dictionary of words
    for key, value in text_and_star.items():
        word_sum = sum(value)
        #if the word is in less than 10 reviews, do not add to dictionary
        if word_sum < 10:
            continue
        else:
            #Get the average rating for every word and put in a dictionary
            value[1] = value[1] * 2
            value[2] = value[2] * 3
            value[3] = value[3] * 4
            value[4] = value[4] * 5
            star_value_sum = sum(value)
            star_avg = star_value_sum / word_sum
            words_and_rating[key] = star_avg
       
    #sort dictionary in decending order, we also got this from stack, link:https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_text_and_rating = sorted(words_and_rating.items(), key=lambda x: x[1], reverse=True)

   
    #write csv file using a csv writer
    with open('yelp_review_ratings.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(['Word', 'Top 500 AVG Star Rating'])
       
        #write the top 500 scored words
        for row in sorted_text_and_rating[0:499]:
            csv_writer.writerow(row)
       
        csv_writer.writerow(['Word', 'Worst 500 AVG Star Rating'])
        #write to 500 worst scored words
        for row in sorted_text_and_rating[-500:-1]:
            csv_writer.writerow(row)
       
       


main()

