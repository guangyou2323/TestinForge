from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io
import random

# 初始化 FastAPI 應用
app = FastAPI(
    title="FreshSafe Backend",
    description="API for meat freshness detection using pH paper",
    version="1.0.0"
)

# ==========================================
# 1. 配置跨域 (CORS) - 非常重要！
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 上線時建議改成具體的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. 定義返回給前端的數據格式
# ==========================================
class AnalysisResponse(BaseModel):
    status: str            # "Fresh", "Edible", "Spoiled"
    ph_value: float        # 具體 pH 值
    confidence_level: int  # 置信度 (0-100)
    rgb_sampled: dict      # 提取的 RGB，方便前端展示
    detected_meat: str     # 最終確定的肉類
    message: str           # 附加信息

# ==========================================
# 3. 核心業務邏輯 (預留給你們的 Model)
# ==========================================
def extract_rgb_from_image(image: Image.Image) -> dict:
    """
    TODO: 【替換為你們真實的圖像處理代碼】
    目前為 Mock 數據：隨機生成 RGB。
    """
    return {
        "r": random.randint(100, 200),
        "g": random.randint(80, 150),
        "b": random.randint(100, 200)
    }

def calculate_ph(rgb: dict) -> float:
    """
    TODO: 【替換為你們真實的 pH 匹配算法】
    目前為 Mock 邏輯：根據 R 和 B 的差異來模擬。
    """
    r, b = rgb["r"], rgb["b"]
    mock_ph = 6.5 + (b - r) / 100.0
    return round(max(4.0, min(9.0, mock_ph)), 1) # 限制在 4.0 - 9.0

def ai_detect_meat(image: Image.Image) -> tuple[str, float]:
    """
    TODO: 【替換為你們真實的 AI 識別模型】
    目前為 Mock 數據：隨機返回一種肉類和置信度。
    """
    meats = ["beef", "pork", "fish", "lamb", "chicken"]
    return random.choice(meats), 0.85

def calculate_final_confidence(is_kind: bool, is_time: bool, ai_conf: float) -> int:
    """
    根據 PRD 邏輯計算最終置信度
    """
    base_confidence = 60
    if is_kind:
        base_confidence += 15
    else:
        base_confidence += int(ai_conf * 15) 
    if is_time:
        base_confidence += 25
    return min(100, base_confidence)

# ==========================================
# 4. API 接口 (Endpoint)
# ==========================================
@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_meat(
    image: UploadFile = File(...),
    is_kind_stated: bool = Form(False),
    meat_type: str = Form(None),
    is_time_stated: bool = Form(False),
    purchase_date: str = Form(None)
):
    print(f"接收到請求: 圖片={image.filename}, 手動肉類={meat_type}, 是否手動={is_kind_stated}")
    
    # 1. 讀取圖片
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    
    # 2. 提取 RGB 
    rgb = extract_rgb_from_image(img)
    
    # 3. 計算 pH 值和狀態
    ph = calculate_ph(rgb)
    if ph < 6.0:
        status = "Fresh"
    elif ph <= 6.8:
        status = "Edible"
    else:
        status = "Spoiled"
        
    # 4. 如果用戶沒填肉類，調用 AI 識別
    detected_meat = meat_type
    ai_confidence = 0.0
    if not is_kind_stated or not meat_type:
        detected_meat, ai_confidence = ai_detect_meat(img)
        
    # 5. 計算最終置信度
    final_confidence = calculate_final_confidence(is_kind_stated, is_time_stated, ai_confidence)
    
    # 6. 返回結果
    return AnalysisResponse(
        status=status,
        ph_value=float(ph),
        confidence_level=final_confidence,
        rgb_sampled=rgb,
        detected_meat=detected_meat,
        message="Analysis successful (Mock Data)"
    )

# ==========================================
# 5. 健康檢查接口
# ==========================================
@app.get("/")
def read_root():
    return {"message": "Welcome to FreshSafe API. The server is running!"}

# ==========================================
# 6. 啟動服務
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
