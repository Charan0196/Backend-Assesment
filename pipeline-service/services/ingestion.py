import requests
import dlt
from dlt.sources.helpers import requests as dlt_requests
from sqlalchemy.orm import Session
from database import SessionLocal, Customer
from datetime import datetime
import json

def fetch_all_customers_from_flask():
    """Fetch all customers from Flask API handling pagination"""
    base_url = "http://mock-server:5000/api/customers"
    customers = []
    page = 1
    limit = 10
    
    while True:
        response = requests.get(f"{base_url}?page={page}&limit={limit}")
        response.raise_for_status()
        data = response.json()
        
        customers.extend(data["data"])
        
        if len(data["data"]) < limit:
            break
        page += 1
    
    return customers

def ingest_to_postgres(customers):
    """Ingest customers to PostgreSQL using SQLAlchemy"""
    db: Session = SessionLocal()
    try:
        records_processed = 0
        for cust in customers:
            # Parse dates
            dob = datetime.strptime(cust['date_of_birth'], '%Y-%m-%d').date() if cust.get('date_of_birth') else None
            created_at = datetime.fromisoformat(cust['created_at'].replace('Z', '+00:00')) if cust.get('created_at') else None
            
            # Upsert
            customer = db.query(Customer).filter(Customer.customer_id == cust['customer_id']).first()
            if customer:
                # Update existing
                for key, value in cust.items():
                    if hasattr(customer, key):
                        if key == 'date_of_birth' and value:
                            setattr(customer, key, dob)
                        elif key == 'created_at' and value:
                            setattr(customer, key, created_at)
                        else:
                            setattr(customer, key, value)
            else:
                # Create new
                new_customer = Customer(
                    customer_id=cust['customer_id'],
                    first_name=cust['first_name'],
                    last_name=cust['last_name'],
                    email=cust['email'],
                    phone=cust.get('phone'),
                    address=cust.get('address'),
                    date_of_birth=dob,
                    account_balance=float(cust.get('account_balance', 0)),
                    created_at=created_at
                )
                db.add(new_customer)
            records_processed += 1
        db.commit()
        return records_processed
    finally:
        db.close()

def run_ingestion():
    customers = fetch_all_customers_from_flask()
    records = ingest_to_postgres(customers)
    return {"status": "success", "records_processed": records}
