import pandas as pd
import numpy as np
import os

def generate_synthetic_data(samples_per_class=10000):
    print("Генерация синтетического датасета трафика...")
    np.random.seed(42)
    
    # Class 0: Web Surfing (Короткие запросы, долгие паузы на чтение)
    # Jitter: Экспоненциальное распределение
    web_jitter = np.random.exponential(scale=50.0, size=samples_per_class)
    web_padding = np.random.normal(loc=128.0, scale=30.0, size=samples_per_class)
    
    # Class 1: Video Streaming (Постоянный тяжелый поток данных)
    # Jitter: Нормальное распределение вокруг 15мс
    vid_jitter = np.random.normal(loc=15.0, scale=5.0, size=samples_per_class)
    vid_padding = np.random.normal(loc=1024.0, scale=100.0, size=samples_per_class)
    
    # Очистка (убираем отрицательные значения)
    web_jitter = np.clip(web_jitter, 1, 500)
    web_padding = np.clip(web_padding, 0, 1500)
    vid_jitter = np.clip(vid_jitter, 1, 50)
    vid_padding = np.clip(vid_padding, 0, 1500)
    
    df_web = pd.DataFrame({'jitter_ms': web_jitter, 'padding_bytes': web_padding, 'profile': 'web'})
    df_vid = pd.DataFrame({'jitter_ms': vid_jitter, 'padding_bytes': vid_padding, 'profile': 'video'})
    
    # Перемешиваем
    df = pd.concat([df_web, df_vid]).sample(frac=1).reset_index(drop=True)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_traffic.csv', index=False)
    print("✅ Датасет успешно сохранен: data/synthetic_traffic.csv")

if __name__ == '__main__':
    generate_synthetic_data()
