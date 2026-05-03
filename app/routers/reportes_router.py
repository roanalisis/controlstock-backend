from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date

from app.auth import get_current_user
from app.database import get_db
from app.models import Reporte, StockCritico, Usuario
from app.schemas import ReporteOut

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


@router.get("/", response_model=list[ReporteOut])
def obtener_reportes(
    fecha: Optional[date] = Query(None, description="Filtrar por fecha (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    query = db.query(Reporte)

    if fecha:
        # Filtrar por rango completo del día para evitar problemas de timezone
        fecha_inicio = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0)
        fecha_fin = fecha_inicio + timedelta(days=1)
        query = query.filter(Reporte.fecha >= fecha_inicio, Reporte.fecha < fecha_fin)

    query = query.order_by(Reporte.fecha.desc(), Reporte.producto)
    reportes = query.all()

    print(f"[DEBUG] fecha={fecha} total={len(reportes)}", flush=True)

    criticos = {
        sc.producto: float(sc.valor_critico)
        for sc in db.query(StockCritico).all()
    }

    return [
        ReporteOut(
            id=r.id,
            producto=r.producto,
            cantidad_vendida=float(r.cantidad_vendida),
            stock_actual=float(r.stock_actual),
            fecha=r.fecha,
            valor_critico=criticos.get(r.producto),
        )
        for r in reportes
    ]
