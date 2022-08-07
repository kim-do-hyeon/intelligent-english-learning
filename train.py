import os
import pandas as pd
path = "labeling"
file_list = os.listdir(path)

all_labeling_dataframe = pd.DataFrame()

for i in range(len(file_list)) :
    path = "labeling/" + file_list[i]
    df = pd.read_csv(path, sep=",", skiprows=1, names=['word1', 'word2', 'word3', 'value'])
    # Concat Dataframes
    all_labeling_dataframe = pd.concat([all_labeling_dataframe, df])

# print(all_labeling_dataframe)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
# LabelEncoder : Pre-processing with categorical data
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Preprocess word data into categorical data
from IPython.display import display

number = LabelEncoder()
all_labeling_dataframe['word1'] = number.fit_transform(all_labeling_dataframe['word1'])
all_labeling_dataframe['word2'] = number.fit_transform(all_labeling_dataframe['word3'])
all_labeling_dataframe['word3'] = number.fit_transform(all_labeling_dataframe['word3'])
all_labeling_dataframe['value'] = number.fit_transform(all_labeling_dataframe['value'])

display(all_labeling_dataframe)

features = ["word1", "word2", "word3"]
target = "value"
X = all_labeling_dataframe[features]
y = all_labeling_dataframe[target]


X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = GaussianNB()
model.fit(X_train, y_train)
pred = model.predict(x_test)
accuracy = accuracy_score(y_test, pred)
print("accuracy : ", accuracy)
y_pred = model.fit(X_train, y_train).predict(x_test)

# Compare the actual value with the predicted value of y to output the wrong number
print("Number of mislabeled points out of a total %d points : %d" % (x_test.shape[0], (y_test != y_pred).sum()))
