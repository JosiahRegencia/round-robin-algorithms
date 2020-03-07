import pandas as pd 
import numpy as np 
import tensorflow as tf
import xgboost  as xgb


from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression

from sklearn.model_selection import StratifiedKFold, KFold, cross_val_predict
from sklearn import ensemble, preprocessing
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, f1_score, recall_score, \
    precision_score, confusion_matrix, hamming_loss

VALIDATOR_FILE = 'RR/Dataset/rr.csv'
validator = pd.read_csv(VALIDATOR_FILE).drop(['Unnamed: 0'],  axis=1)

def print_results(clf):
	print('\nClassifier: ', clf)
	print('Accuracy:', clf.get_mean_accuracy())
	print('F1:', clf.get_mean_f1())
	print('Precision:', clf.get_mean_precision())
	print('Recall:', clf.get_mean_recall())
	print('Hamming Loss: ', clf.get_mean_hamming_loss())
	print('EID:', clf.get_mean_eid())
	print('\n\n')

def adaboost(dataset):	
	Features = dataset[:,:10]
	print('X: ', Features)
	Labels = dataset[:,10]
	print('Y: ', Labels)
	print('\n\n')
	
	regr = AdaBoostRegressor(random_state=0, n_estimators=100)
	regr.fit(Features, Labels)
	print ('Adaboost')
	print ('Score: {}'.format(regr.score(Features, Labels)))

	for index, row in validator.iterrows():
		bursts = [row.tolist()]
		bursts = [bursts[0][:10]]
		print ('Row: {}\tPrediction: {}'.format(row['opt_tq'], regr.predict(bursts)))


	joblib.dump(regr, 'RR/Models/NormalSorted/adaboost.pkl')

def randomforest(dataset):	
	Features = dataset[:,:10]
	print('X: ', Features)
	Labels = dataset[:,10]
	print('Y: ', Labels)
	print('\n\n')
	
	regr = RandomForestRegressor(random_state=0, n_estimators=100)
	regr.fit(Features, Labels)
	print ('RandomForest')
	print ('Score: {}'.format(regr.score(Features, Labels)))

	for index, row in validator.iterrows():
		bursts = [row.tolist()]
		bursts = [bursts[0][:10]]
		print ('Row: {}\tPrediction: {}'.format(row['opt_tq'], regr.predict(bursts)))


	joblib.dump(regr, 'RR/Models/NormalSorted/randomforest.pkl')

def gradientboosting(dataset):	
	Features = dataset[:,:10]
	print('X: ', Features)
	Labels = dataset[:,10]
	print('Y: ', Labels)
	print('\n\n')
	
	regr = GradientBoostingRegressor(random_state=0, n_estimators=100)
	regr.fit(Features, Labels)
	print ('GradientBoosting')
	print ('Score: {}'.format(regr.score(Features, Labels)))

	for index, row in validator.iterrows():
		bursts = [row.tolist()]
		bursts = [bursts[0][:10]]
		print ('Row: {}\tPrediction: {}'.format(row['opt_tq'], regr.predict(bursts)))


	joblib.dump(regr, 'RR/Models/NormalSorted/gradientboosting.pkl')

def mlpregressor(dataset):	
	Features = dataset[:,:10]
	print('X: ', Features)
	Labels = dataset[:,10]
	print('Y: ', Labels)
	print('\n\n')
	
	regr = MLPRegressor(hidden_layer_sizes=(100,100), solver='sgd')
	regr.fit(Features, Labels)
	print ('Multilayer Perceptron Regressor')
	print ('Score: {}'.format(regr.score(Features, Labels)))

	for index, row in validator.iterrows():
		bursts = [row.tolist()]
		bursts = [bursts[0][:10]]
		print ('Row: {}\tPrediction: {}'.format(row['opt_tq'], regr.predict(bursts)))


	joblib.dump(regr, 'RR/Models/NormalSorted/mlpregressor.pkl')

def xgboost(dataset):
	Features = dataset[:,:10]
	print('X: ', Features)
	Labels = dataset[:,10]
	print('Y: ', Labels)
	print('\n\n')
	
	regr = xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 100)
	regr.fit(Features, Labels)
	print ('XGBoost Regressor')
	print ('Score: {}'.format(regr.score(Features, Labels)))

	for index, row in validator.iterrows():
		bursts = [row.tolist()]
		bursts = [bursts[0][:10]]
		print ('Row: {}\tPrediction: {}'.format(row['opt_tq'], regr.predict(bursts)))


	joblib.dump(regr, 'RR/Models/NormalSorted/xgboostregressor.pkl')

def main():
	training_dataset = pd.read_csv('RR/Dataset/rr_sorted.csv').drop('Unnamed: 0',  axis=1)
	training = training_dataset.iloc[:,:].values
	print (training)
	adaboost(training)
	randomforest(training)
	gradientboosting(training)
	mlpregressor(training)
	xgboost(training)
	# dnnpregressor(training_dataset)

if __name__ == "__main__":
	main()

