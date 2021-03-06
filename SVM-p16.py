from numpy.random import seed
from sklearn import svm
import numpy as np
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as selection

# Set the random seed to 1
seed(1)

# ====================================
# STEP 1: read the training and testing data.

# specify path to training data and testing data
train_x_location = "x_train16.csv"
train_y_location = "y_train16.csv"

test_x_location = "x_test.csv"
test_y_location = "y_test.csv"

print("Reading training data")
x_train = np.loadtxt(train_x_location, dtype="uint8", delimiter=",")
y_train = np.loadtxt(train_y_location, dtype="uint8", delimiter=",")

m, n = x_train.shape # m training examples, each with n features
m_labels, = y_train.shape # m2 examples, each with k labels
l_min = y_train.min()

assert m_labels == m, "x_train and y_train should have same length."
assert l_min == 0, "each label should be in the range 0 - k-1."
k = y_train.max()+1

print(m, "examples,", n, "features,", k, "categiries.")

print("Reading testing data")
x_test = np.loadtxt(test_x_location, dtype="uint8", delimiter=",")
y_test = np.loadtxt(test_y_location, dtype="uint8", delimiter=",")

m_test, n_test = x_test.shape
m_test_labels, = y_test.shape
l_min = y_train.min()

assert m_test_labels == m_test, "x_test and y_test should have same length."
assert n_test == n, "train and x_test should have same number of features."

print(m_test, "test examples.")


# ====================================
# STEP 2: pre  processing
print("Pre processing data")

# The same pre processing must be applied to both training and testing data
scaler = preprocessing.StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)



# ====================================
# STEP 3: train model.

print("---train")
params = {'kernel': ['poly'],
          'C': [4**i for i in range(-6, 6)],
          'degree': [0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5],
          'gamma': [4**i for i in range(-6, 6)]}
print('Training data and choosing the best parameters...')
selector = selection.GridSearchCV(svm.SVC(), params, n_jobs=-1)
selector.fit(x_train, y_train)

model = svm.SVC(**selector.best_params_, coef0=1)
model.fit(x_train, y_train)

# ====================================
# STEP3: evaluate  model

print("---evaluate")
print("number of support vectors:", model.n_support_)
acc = model.score(x_test, y_test)
print("acc:", acc)
