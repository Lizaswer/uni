# app/main.py
from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel, ConfigDict
import uvicorn

app = FastAPI(title="Report API", version="1.0.0")

# ========== МОДЕЛИ PYDANTIC ==========
class ReportCreateSimple(BaseModel):
    report_at: date
    order_id: int
    count_product: int

class ReportResponseSimple(ReportCreateSimple):
    id: int
    created_at: date
    model_config = ConfigDict(from_attributes=True)

# ========== БАЗОВЫЕ ЭНДПОИНТЫ ==========
@app.get("/")
async def root():
    return {"message": "Report API is running. Go to /docs for API documentation."}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "report-api"}

# ========== ЭНДПОИНТЫ ДЛЯ ОТЧЁТОВ ==========
@app.post("/report", response_model=ReportResponseSimple)
async def create_report_endpoint(report: ReportCreateSimple):
    """Создать новый отчёт"""
    try:
        # Здесь должна быть логика сохранения в БД
        # Для теста просто возвращаем данные
        return ReportResponseSimple(
            id=1,
            report_at=report.report_at,
            order_id=report.order_id,
            count_product=report.count_product,
            created_at=date.today()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
async def get_report(date_param: str = None):
    """Получить отчёты за указанную дату"""
    from datetime import datetime
    
    if date_param:
        try:
            report_date = datetime.strptime(date_param, "%Y-%m-%d").date()
        except:
            report_date = date.today()
    else:
        report_date = date.today()
    
    return {
        "date": report_date.isoformat(),
        "reports": [
            {
                "id": 1,
                "report_at": report_date.isoformat(),
                "order_id": 100,
                "count_product": 5,
                "created_at": date.today().isoformat()
            }
        ]
    }
@app.get("/reports/all")
async def get_all_reports(skip: int = 0, limit: int = 100):
    """Получить все отчёты"""
    return {
        "skip": skip,
        "limit": limit,
        "total": 2,
        "reports": [
            {
                "id": 1,
                "report_at": date(2024, 12, 14),
                "order_id": 100,
                "count_product": 5,
                "created_at": date.today()
            },
            {
                "id": 2,
                "report_at": date(2024, 12, 14),
                "order_id": 101,
                "count_product": 10,
                "created_at": date.today()
            }
        ]
    }

# Запуск сервера через uvicorn напрямую
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)