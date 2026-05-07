import pickle
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Adaptive Behavioral Stealth VPN - ML API")

# Предзагрузка обученных моделей при старте сервера
try:
    with open('models/kde_profiles.pkl', 'rb') as f:
        models = pickle.load(f)
    print("✅ ML Модели успешно загружены в память!")
except FileNotFoundError:
    print("⚠️ ВНИМАНИЕ: Файл моделей не найден. Сначала запустите train.py!")
    models = {}

@app.get("/pattern")
def get_pattern(profile: str = "web"):
    if profile not in models:
        raise HTTPException(status_code=404, detail="Profile not found. Use 'web' or 'video'.")
    
    # ИИ генерирует 1 новый уникальный сэмпл (тайминг и размер) на лету
    sample = models[profile].sample(1)[0]
    
    jitter_ms = max(1, int(sample[0]))
    padding_bytes = max(0, int(sample[1]))
    
    return {
        "profile": profile,
        "jitter_ms": jitter_ms,
        "padding_bytes": padding_bytes
    }

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
