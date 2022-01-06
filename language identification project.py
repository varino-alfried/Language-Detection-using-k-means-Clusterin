# -*- coding: utf-8 -*-

import pandas as pd
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk

print("Hello")
print("We Wish  you a nice day")
print("PLease Select your an option: ")

print("Enter  1  if you Choose to identify a text Query")
print("Enter  2  if you Choose to input identify a voice Query")

opt = int(input("Enter Your number"))
if (opt!=1 and opt!=2):

    print("Program exit due to Wrong intput")
    exit(0)
else:
    stopwords = nltk.corpus.stopwords.words('english')
    ps = nltk.PorterStemmer()
# Cleaning up text

    def clean_text(text):

        #stopword removal

        toke=list(text.split(' '))


        #punctutaion removal
        t_lator=str.maketrans('','',string.punctuation)
        text=text.translate(t_lator)
        remove_digits = str.maketrans('', '', string.digits)
        text = text.translate(remove_digits)

        #removing special symbol
        for i in '“”—':
            text = text.replace(i, ' ')

        return text

    def clean_data(df):
        df.dropna(how='any')

    vectorizer = TfidfVectorizer()
    def train_data(df):

        X = vectorizer.fit_transform(df['text'])
        true_k = 4
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        for i in range(true_k):
            print("Cluster %d:" % i),
            for ind in order_centroids[i, :10]:
                print(' %s' %terms[ind]),
                print
        return model

    print("-------------------------------------------------------")
    print("All languages in The Program ")
    print("-------------------------------------------------------")
    df = pd.read_csv("dataset2.csv")
    df.dropna(how='any') #clean the dataset
    df.columns=['text','language']
    df = df.sort_values(['language'])
    i = 0
    while i < 4000:
         print(df.iat[i, 1])
         i += 1000
    print("-------------------------------------------------------")
    print("learning from the dataset.... ")
    print("-------------------------------------------------------")
    clean_data(df)
    train=train_data(df)
    if(opt == 2 ):
        print("-------------------------------------------------------")
        print("voice input ")
        print("-------------------------------------------------------")

        r = sr.Recognizer()
        with sr.Microphone() as source:
                print("speak")
                audio= r.record(source, duration=5)
        try:
            print("recognising...")
            text= r.recognize_google(audio)
            print('{}'.format(text))
            clean_text(text)
        except:
            print("try again!")

    if(opt == 1 ):
        print("-------------------------------------------------------")
        print("text input ")
        print("-------------------------------------------------------")

        text = input("Please enter a string:\n")
        clean_text(text)
    def predicti (model):
        try:
            Y = vectorizer.transform([text])
            prediction = model.predict(Y)
            print (prediction)

            z= prediction[0]*1000
            return df.iat[z, 1]
        except:
            print("try again!")

    print("-------------------------------------------------------")
    print("model prediction")
    print("-------------------------------------------------------")
    try:
        output = predicti(train)
        print("The predicted language is " + output)
    except:
        print("try again!")



    root = tk.Tk()
    root.title("AI PROJECT")
    root.geometry("600x600")

    if(output == 'Arabic'):
        photo = Image.open("Assets/Arabic.jpg")
        resized_image = photo.resize((600,600), Image.ANTIALIAS)
        converted_image = ImageTk.PhotoImage(resized_image)
    elif(output == 'English'):
        photo = Image.open("Assets/English.jpg")
        resized_image = photo.resize((600,600), Image.ANTIALIAS)
        converted_image = ImageTk.PhotoImage(resized_image)
    elif(output == 'French'):
        photo = Image.open("Assets/French.jpg")
        resized_image = photo.resize((600,600), Image.ANTIALIAS)
        converted_image = ImageTk.PhotoImage(resized_image)
    elif(output == 'Dutch'):
        photo = Image.open("Assets/Dutch.jpg")
        resized_image = photo.resize((600,600), Image.ANTIALIAS)
        converted_image = ImageTk.PhotoImage(resized_image)
    else:
        label = tk.Label(root, text="Sorry try again", width=600, height=600)

try:
    label = tk.Label(root, image = converted_image, width = 600 , height = 600)
    label.pack()
    root.eval('tk::PlaceWindow . center')
    root.attributes('-topmost',True)
    root.mainloop()
except:
    print("try again!")