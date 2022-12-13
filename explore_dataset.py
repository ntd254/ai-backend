import pandas as pd
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from joblib import dump
from sklearn import metrics


def text_process(mess):
    """
        Takes in a string of text, then performs the following:
        1. Remove all punctuation
        2. Remove all stopwords
        3. Returns a list of the cleaned text
        """
    STOPWORDS = stopwords.words('english') + ['u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)

    # Now just remove any stopwords
    return ' '.join([word for word in nopunc.split() if word.lower() not in STOPWORDS])


data = pd.read_csv("spam.csv", encoding="latin-1")
data.dropna(how="any", inplace=True, axis=1)
data.columns = ["label", "message"]
data["label_num"] = data.label.map({"ham": 0, "spam": 1})
data["clean_msg"] = data.message.apply(text_process)
X = data.clean_msg
y = data.label_num
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
vect = CountVectorizer()
vect.fit(X_train)
X_train_dtm = vect.transform(X_train)
X_test_dtm = vect.transform(X_test)
nb = MultinomialNB(alpha=1)
nb.fit(X_train_dtm, y_train)
print(metrics.accuracy_score(y_test, nb.predict(X_test_dtm)))
print(nb.predict(vect.transform(["[image: Google]ai_project đã được cấp quyền truy cập vào Tài khoản Google của bạndat726416@gmail.comNếu không cấp quyền truy cập thì bạn nên kiểm tra hoạt động này và bảo mậttài khoản của mình.Kiểm tra hoạt động<>Bạn cũng có thể xem hoạt động bảo mật tạihttps://myaccount.google.com/notificationsChúng tôi gửi email này để thông báo cho bạn biết về những thay đổi quantrọng đối với Tài khoản Google và dịch vụ của bạn.© 2022 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA"]))[0])
print(data.clean_msg.head())
# dump(nb, "predict_spam.joblib")