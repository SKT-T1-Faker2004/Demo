import pandas as pd
from sklearn import linear_model

def get_data(file, ball, ball_id):
    data = pd.read_csv(file)
    data['ball_id'] = ball_id
    X = []; Y = []
    for i, b in zip(data['ball_id'], data[ball]):
        X.append([i])
        Y.append([b])
    return X,  Y
 

def linear_model_test(X, Y, predict_value):
    reg = linear_model.LinearRegression()
    reg.fit(X, Y)
    predict_outcome = reg.predict(predict_value)
    predictions = {}
    predictions['intercept'] = reg.intercept_
    predictions['coefficient'] = reg.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions
 
 
def get_predicted_num(file, ball, ball_id, num):
    X, Y = get_data(file, ball, ball_id)

    predict_value = [[51]]
    result = linear_model_test(X, Y, predict_value)
    print('For',num,'>> Predicted value:', result['predicted_value'][0][0])
    print(f"[Intercept Value: {result['intercept'][0]} | Coefficient: {result['coefficient'][0][0]}]")