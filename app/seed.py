from datetime import date, timedelta
import random
from app.database import Base, engine, SessionLocal
from app.models import Sale, Expense, Employee, WorkflowTask

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Sale).first():
            print("Database already contains data; skipping seed.")
            return
        random.seed(17)
        departments = ["Sales", "Marketing", "Operations", "Technology", "HR"]
        products = ["Platform", "Consulting", "Analytics", "Support"]
        today = date.today()
        for day in range(180):
            d = today - timedelta(days=179-day)
            for dep in departments:
                base = {"Sales": 7200, "Marketing": 3600, "Operations": 2100,
                        "Technology": 1800, "HR": 900}[dep]
                trend = 1 + day * 0.0012
                revenue = max(100, random.gauss(base * trend, base * 0.17))
                db.add(Sale(date=d, department=dep, product=random.choice(products),
                            revenue=round(revenue, 2), units=random.randint(3, 45)))
        vendors = ["Northstar Supplies", "Metro Services", "Cloudline", "Office Hub", "Rapid Logistics"]
        categories = ["Software", "Travel", "Supplies", "Logistics", "Training"]
        for i in range(420):
            amount = random.uniform(180, 4800)
            if i in (77, 211, 366):
                amount *= 8  # intentional outliers for the demo
            db.add(Expense(date=today-timedelta(days=random.randint(0,179)),
                          department=random.choice(departments), category=random.choice(categories),
                          vendor=random.choice(vendors), amount=round(amount, 2)))
        names = ["Aarav", "Diya", "Kabir", "Meera", "Ishaan", "Anaya", "Rohan", "Sara",
                 "Vivaan", "Ira", "Arjun", "Mira", "Dev", "Tara", "Neil"]
        for i, name in enumerate(names):
            target = random.uniform(70, 120)
            output = target * random.uniform(0.55, 1.25)
            db.add(Employee(name=name, department=departments[i % len(departments)],
                            monthly_target=round(target,2), monthly_output=round(output,2), active=1))
        stages = ["Request", "Approval", "Processing", "Quality Check", "Completion"]
        for i in range(160):
            stage = random.choice(stages)
            duration = random.uniform(1, 18)
            if stage == "Approval" and i % 4 == 0:
                duration *= 3.5
            db.add(WorkflowTask(process_name=random.choice(["Purchase Approval", "Customer Onboarding",
                        "Expense Reimbursement", "Order Fulfilment"]), stage=stage,
                        duration_hours=round(duration,2),
                        status=random.choice(["Completed", "Completed", "In Progress", "Delayed"]),
                        owner_department=random.choice(departments)))
        db.commit()
        print("Seeded demo database successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
