import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

df = pd.read_csv("spam.csv", encoding="latin-1")
df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
# Features and Labels
df['label'] = df['type'].map({'ham': 0, 'spam': 1})
x = df['text']
y = df['label']

# Extract Feature With CountVectorizer Extract Feature With CountVectorizer :cleaning involved converting all of our
# data to lower case and removing all punctuation marks.
cv = CountVectorizer()
x = cv.fit_transform(x)  # Fit the Data


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
# Naive Bayes Classifier

model = MultinomialNB()  # NAIVE BAYES
model.fit(x_train, y_train)
joblib.dump(model, "predict_spam.joblib")
vect = cv.transform(["This Halloween, we have a treat for you. Save on exclusive courses, community support, and more with 50% off an annual membership to Codecademy Pro. Just use promo code HALLOWEEN22 at checkout"])
print("spam" if model.predict(vect)[0] == 1 else "ham")
# print(model.predict(cv.transform(["."]))[0] == 1)
print(model.score(x_test, y_test))
