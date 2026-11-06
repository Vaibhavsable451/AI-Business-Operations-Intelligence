from sqlalchemy import String, Float, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Sale(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[object] = mapped_column(Date, index=True)
    department: Mapped[str] = mapped_column(String(80), index=True)
    product: Mapped[str] = mapped_column(String(120))
    revenue: Mapped[float] = mapped_column(Float)
    units: Mapped[int] = mapped_column(Integer)

class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[object] = mapped_column(Date, index=True)
    department: Mapped[str] = mapped_column(String(80), index=True)
    category: Mapped[str] = mapped_column(String(100))
    vendor: Mapped[str] = mapped_column(String(120))
    amount: Mapped[float] = mapped_column(Float)

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    department: Mapped[str] = mapped_column(String(80), index=True)
    monthly_target: Mapped[float] = mapped_column(Float)
    monthly_output: Mapped[float] = mapped_column(Float)
    active: Mapped[int] = mapped_column(Integer, default=1)

class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    process_name: Mapped[str] = mapped_column(String(120), index=True)
    stage: Mapped[str] = mapped_column(String(100))
    duration_hours: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30))
    owner_department: Mapped[str] = mapped_column(String(80))
