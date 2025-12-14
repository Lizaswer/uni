from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas

async def create_report(db: AsyncSession, report: schemas.ReportCreate):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    return db_report

async def get_reports_by_date(db: AsyncSession, date_param: date):
    result = await db.execute(
        select(models.Report).where(models.Report.report_at == date_param)
    )
    return result.scalars().all()