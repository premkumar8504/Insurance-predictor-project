from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION


app = FastAPI()

# Human readable
@app.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}

# Machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

# Main prediction route
@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    try:
        user_input = {
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }

        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})