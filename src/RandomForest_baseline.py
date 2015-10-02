import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vect= TfidfVectorizer(  use_idf=True, smooth_idf=True, sublinear_tf=False)
from sklearn.cross_validation import train_test_split, cross_val_score


df = pd.read_csv('/path/file.csv',
                     header=0, sep=',', names=['SentenceId', 'Sentence', 'Sentiment'])



reduced_data = tfidf_vect.fit_transform(df['Sentence'].values)
y = df['Sentiment'].values



from sklearn.decomposition.truncated_svd import TruncatedSVD
svd = TruncatedSVD(n_components=5)
reduced_data = svd.fit_transform(reduced_data)

X_train, X_test, y_train, y_test = train_test_split(reduced_data,
                                                    y, test_size=0.33,
                                                    random_state=42)

from sklearn.ensemble import RandomForestClassifier

#se pasmo con 1000000
#probar con mas parametros
classifier=RandomForestClassifier(n_estimators=100)
classifier.fit(X_train, y_train)
prediction = classifier.predict(X_test)


#print X_train.shape

from sklearn.metrics.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score



print '\nAccuracy:', accuracy_score(y_test, prediction)
print '\nscore:', classifier.score(X_train, y_train)
print '\nrecall:', recall_score(y_test, prediction)
print '\nprecision:', precision_score(y_test, prediction)
print '\n clasification report:\n', classification_report(y_test, prediction)
print '\n confussion matrix:\n',confusion_matrix(y_test, prediction)

#plots:

import matplotlib.pyplot as plt
confusion_matrix_plot = confusion_matrix(y_test, prediction)
plt.title('matriz de confusion')
plt.colorbar()
plt.xlabel()
plt.xlabel('categoria de verdad')
plt.ylabel('categoria predecida')
plt.show()

#como arreglo
# import numpy as np
# scores = cross_val_score(classifier, X_train, y_train, cv=5)
# print "scores:\n",np.mean(scores), scores
