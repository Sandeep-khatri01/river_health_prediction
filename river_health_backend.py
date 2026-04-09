import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, HistGradientBoostingRegressor, VotingRegressor

def engineer_features(df):
    result = pd.DataFrame()
    pollutants = ['O2', 'NH4', 'NO2', 'NO3', 'BOD5']
    for p in pollutants:
        cols = [f'{p}_{i}' for i in range(1, 8)]
        data = df[cols]
        result[f'{p}_mean'] = data.mean(axis=1)
        result[f'{p}_std']  = data.std(axis=1)
        result[f'{p}_max']  = data.max(axis=1)
        result[f'{p}_trend'] = df[f'{p}_7'] - df[f'{p}_1']
    
    # Polynomial & Interaction features
    result['O2_1_sq'] = df['O2_1'] ** 2
    result['O2_1_sqrt'] = np.sqrt(df['O2_1'].clip(lower=0))
    result['O2_1_O2_2'] = df['O2_1'] * df['O2_2']
    result['O2_1_BOD5_1'] = df['O2_1'] * df['BOD5_1']
    result['O2_ratio'] = df['O2_1'] / (df['O2_2'] + 1e-6)
    return result

def classify_river_health(do_level):
    if do_level >= 8: return 'Excellent 🟢'
    elif do_level >= 6: return 'Good 🟡'
    elif do_level >= 4: return 'Fair 🟠'
    elif do_level >= 2: return 'Poor 🔴'
    else: return 'Critical ⚫ (Dead Zone)'

def predict_do(new_row_dict, model, feature_columns):
    row_df = pd.DataFrame([new_row_dict])
    feat = engineer_features(row_df)
    feat = feat.reindex(columns=feature_columns, fill_value=0)
    prediction = model.predict(feat)[0]
    health = classify_river_health(prediction)
    return prediction, health

# Initializing and training the model to be available globally
df = pd.read_csv('sample_submission.csv')
features_df = engineer_features(df)
X = features_df.copy()
y = df['target']
X_columns = X.columns

# Training the best model as per optimized notebook
reg1 = ExtraTreesRegressor(n_estimators=1000, max_depth=25, n_jobs=-1, random_state=42)
reg2 = RandomForestRegressor(n_estimators=1000, max_depth=25, n_jobs=-1, random_state=42)
reg3 = HistGradientBoostingRegressor(max_iter=1000, learning_rate=0.01, max_depth=15, random_state=42)

best_model = VotingRegressor([('et', reg1), ('rf', reg2), ('hgb', reg3)])
best_model.fit(X, y)
