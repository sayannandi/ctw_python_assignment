import os

from sqlalchemy import create_engine
from sqlalchemy import Float, Integer, String
from sqlalchemy import select, and_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.sql import func


MYSQL_URI = os.environ['MYSQL_URI']
engine = create_engine(MYSQL_URI, pool_recycle=3600, echo=True)


class Base(DeclarativeBase):
    pass


class FinancialData(Base):
    __tablename__ = "financial_data"

    date: Mapped[str] = mapped_column(String(12), primary_key=True)
    symbol: Mapped[str] = mapped_column(String(30), primary_key=True)
    open_price: Mapped[float]  = mapped_column(Float)
    close_price: Mapped[float]  = mapped_column(Float)
    volume: Mapped[int] = mapped_column(Integer)

    @classmethod
    def bulk_upsert(cls, data):
        insert_stmt = insert(FinancialData).values(data)
        upsert_stmt = insert_stmt.on_duplicate_key_update(
            open_price=insert_stmt.inserted.open_price,
            close_price=insert_stmt.inserted.close_price,
            volume=insert_stmt.inserted.volume
        )
        with Session(engine) as session:
            session.execute(upsert_stmt)
            session.commit()
        return
    
    @classmethod
    def get_financial_data(cls, symbol=None, start_date=None, end_date=None, page=1, limit=5):
        select_stmt = select(FinancialData).order_by(FinancialData.date.asc())
        
        if symbol:
            select_stmt = select_stmt.where(FinancialData.symbol == symbol)
        if start_date:
            select_stmt = select_stmt.where(FinancialData.date >= start_date)
        if end_date:
            select_stmt = select_stmt.where(FinancialData.date <= end_date)

        with engine.connect() as conn:
            cnt = conn.execute(select(func.count()).select_from(select_stmt.subquery())).fetchone().count

        select_stmt = select_stmt.offset((page - 1) * limit).limit(limit)

        with engine.connect() as conn:
            results = conn.execute(select_stmt)
            return cnt, results.mappings().all()

    @classmethod    
    def get_statistics(cls, symbol, start_date, end_date):
        select_stmt = select(
            FinancialData.symbol,
            func.avg(FinancialData.open_price).label('average_daily_open_price'),
            func.avg(FinancialData.close_price).label('average_daily_close_price'),
            func.avg(FinancialData.volume).label('average_daily_volume')
        ).where(
            and_(
                FinancialData.symbol == symbol,
                FinancialData.date >= start_date,
                FinancialData.date <= end_date
            )
        ).group_by(FinancialData.symbol)

        with engine.connect() as conn:
            return conn.execute(select_stmt).fetchone()._mapping


# def init():
#     create_db()
#     create_table()

# def create_db():
#     """
#     Creates database if doesn't exist
#     """
#     if not database_exists(engine.url):
#         create_database(engine.url)

# def create_table():
#     Base.metadata.create_all(engine)


# init()