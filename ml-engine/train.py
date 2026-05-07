import pandas as pd
import numpy as np
import pickle
import os
from sklearn.neighbors import KernelDensity

def train_models():
    print("Загрузка датасета...")
    df = pd.read_csv('data/synthetic_traffic.csv')
    
    models = {}
    
    # Обучаем отдельную модель (Ядерную оценку плотности - KDE) для каждого профиля
    # KDE идеально подходит для генерации новых случайных значений, похожих на обучающую выборку
    for profile in ['web', 'video']:
        print(f"Обучение ML-модели (KDE) для профиля: {profile}...")
        data = df[df['profile'] == profile][['jitter_ms', 'padding_bytes']].values
        
        kde = KernelDensity(kernel='gaussian', bandwidth=5.0).fit(data)
        models[profile] = kde
        
    os.makedirs('models', exist_ok=True)
    with open('models/kde_profiles.pkl', 'wb') as f:
        pickle.dump(models, f)
        
    print("✅ ИИ-Модели успешно обучены и сохранены в models/kde_profiles.pkl")

if __name__ == '__main__':
    train_models()
