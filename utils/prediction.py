import numpy as n
from sklearn.linear_model import LinearRegression

class CostPrediction:
    def __init__(self):
        self.model = LinearRegression()

    def train(self,quantity,cost):
        x = n.array(quantity).reshape(-1,1)
        y = n.array(cost)
        self.model.fit(x,y)
    
    def predict(self,quantity:float) -> float:
        return float(self.model.predict([[quantity]])[0])