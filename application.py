import sys
from flask import Flask, render_template, request
from Customer.exception import CustomerException
from Customer.predictor import ModelResolver
from Customer.pipeline.training_pipeline import start_training_pipeline
import warnings
warnings.filterwarnings('ignore')

application = Flask(__name__)


@application.route('/', methods=['GET'])
def homePage():
    try:
        return render_template("index.html")
    except Exception as e:
        raise CustomerException(e, sys)


@application.route('/train', methods=['POST', 'GET'])
def train():
    if request.method == 'POST':
        try:
            training = start_training_pipeline()
            return render_template("index.html")
        except Exception as e:
            raise CustomerException(e, sys)
    else:
        return render_template("index.html")


@application.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            Income = float(request.form['Income'])
            Recency = int(request.form['Recency'])
            Age = int(request.form['Age'])
            TotalSpendings = int(request.form['TotalSpendings'])
            Children = int(request.form['Children'])
            MonthEnrollement = int(request.form['MonthEnrollement'])

            model = ModelResolver()
            output = model.predict([[Income, Recency, Age, TotalSpendings, Children, MonthEnrollement]])[0]
            print(output)
            return render_template('result.html', prediction=str(output))
        except Exception as e:
            raise CustomerException(e, sys)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    application.run(port=5000, debug=True)
