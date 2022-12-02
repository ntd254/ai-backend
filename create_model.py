import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import string
from nltk.corpus import stopwords

df = pd.read_csv("spam.csv", encoding="latin-1")
df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
# Features and Labels
df['label'] = df['type'].map({'ham': 0, 'spam': 1})
# print(df.head())
# print(df.label.value_counts())
# x = df['text']
# y = df['label']
# Extract Feature With CountVectorizer Extract Feature With CountVectorizer :cleaning involved converting all of our
# data to lower case and removing all punctuation marks.
# cv = CountVectorizer()
# x = cv.fit_transform(x)  # Fit the Data


def remove_punctuation_and_stopwords(sms):
    sms_no_punctuation = [ch for ch in sms if ch not in string.punctuation]
    sms_no_punctuation = "".join(sms_no_punctuation).split()
    sms_no_punctuation_no_stopwords = [word.lower() for word in sms_no_punctuation if word.lower() not in stopwords.words("english")]
    return sms_no_punctuation_no_stopwords


cv = CountVectorizer()
x = df['text']
y = df['label']
x = cv.fit_transform(x)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
# Naive Bayes Classifier

model = MultinomialNB(alpha=1)  # NAIVE BAYES
model.fit(x_train, y_train)
# joblib.dump(model, "predict_spam.joblib")
vect = cv.transform(["This Halloween, we have a treat for you. Save on exclusive courses, community support, and more with 50% off an annual membership to Codecademy Pro. Just use promo code HALLOWEEN22 at checkout"])
print("spam" if model.predict(vect)[0] == 1 else "ham")
print(model.score(x_test, y_test))
