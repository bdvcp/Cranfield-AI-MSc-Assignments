from numpy import  *
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import *
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import PolynomialFeatures

TrainData = pd.read_csv("train_selected.csv")
XTrain = TrainData[['cycle','s1','s2','s3','s4']]
YTrain =  TrainData[['ttf']]

TestData = pd.read_csv("test_selected_ttf.csv")
XTest = TestData[['cycle','s1','s2','s3','s4']]
YTest = TestData[['ttf']]

corr = XTrain.corr()
sns.heatmap(corr, mask=zeros_like(corr, dtype=bool), cmap=sns.diverging_palette(220, 10, as_cmap=True), square=True).set_title('Multicollinearity Check')

model = 6
if model == 1:
    Pipeline = make_pipeline(LinearRegression())
    
if model == 2:
    Pipeline = make_pipeline(Lasso(alpha=0.1))

if model == 3: 
    Pipeline = make_pipeline(BayesianRidge())

if model == 4: 
    Pipeline = make_pipeline(KNeighborsRegressor())

if model == 5: 
    Pipeline = make_pipeline(PolynomialFeatures(degree=2),BayesianRidge())

if model == 6: 
    Pipeline = make_pipeline(PolynomialFeatures(degree=3),BayesianRidge())

if model == 7: 
    Pipeline = make_pipeline(PolynomialFeatures(degree=4),BayesianRidge())

if model == 8: 
    Pipeline = make_pipeline(PolynomialFeatures(degree=2),LinearRegression())

if model == 9: 
    Pipeline = make_pipeline(PolynomialFeatures(degree=3),LinearRegression())

if model == 10: 
    Pipeline = make_pipeline(PolynomialFeatures(degree=4),LinearRegression())

M = 1000000000   
Number_of_splits = 10
TestIndex = pd.DataFrame()
TrainIndex = pd.DataFrame()
N = 0

if(True):
    skf = KFold(n_splits=Number_of_splits, random_state=1, shuffle=False)
    skf.get_n_splits(XTrain, YTrain)
    print('RMSE for ' + str(Number_of_splits) + '-fold splits')
    for train_index, test_index in skf.split(XTrain, YTrain):
        X_train, X_test = XTrain.iloc[train_index], XTrain.iloc[test_index]
        y_train, y_test = YTrain.iloc[train_index], YTrain.iloc[test_index]
        Pipeline.fit(X_train,y_train)
        print(mean_squared_error(y_test, Pipeline.predict(X_test),squared=False))
        N += mean_squared_error(y_test, Pipeline.predict(X_test),squared=False)
        if M > mean_squared_error(y_test, Pipeline.predict(X_test),squared=False):
            M = mean_squared_error(y_test, Pipeline.predict(X_test),squared=False)
            
            TestIndex = test_index
            TrainIndex = train_index
    print('------')
    print('RMSE Average for ' + str(Number_of_splits) + '-fold splits: ' + str(round(N/Number_of_splits,2)))    
    print('------')

Pipeline.fit(XTrain,YTrain)
           
TestData['pttf'] = Pipeline.predict(XTest)

print('RMSE for model: ' + str(round(mean_squared_error(TestData['ttf'], TestData['pttf'],squared=False),2)))
print('r^2 score for model: ' + str(round(r2_score(TestData['ttf'], TestData['pttf']),4)))

