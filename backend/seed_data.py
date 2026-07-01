from sqlalchemy.orm import Session
from app.db.session import SessionLocal, Base, engine
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.tour import Tour
from app.core.security import get_password_hash

def seed_db():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if admin already exists
    if db.query(User).filter(User.email == "admin@ridesphere.com").first():
        print("Database already seeded.")
        db.close()
        return
        
    print("Seeding database...")
    
    # Create default users
    admin_pw = get_password_hash("admin123")
    admin = User(
        email="admin@ridesphere.com",
        hashed_password=admin_pw,
        full_name="RideSphere Admin",
        role="admin",
        is_verified=True,
        wallet_balance=1000.0
    )
    
    owner_pw = get_password_hash("owner123")
    owner = User(
        email="owner@ridesphere.com",
        hashed_password=owner_pw,
        full_name="Fleet Owner John",
        role="owner",
        is_verified=True,
        wallet_balance=0.0
    )
    
    customer_pw = get_password_hash("customer123")
    customer = User(
        email="customer@ridesphere.com",
        hashed_password=customer_pw,
        full_name="Jane Doe",
        role="customer",
        is_verified=True,
        wallet_balance=500.0
    )
    
    db.add(admin)
    db.add(owner)
    db.add(customer)
    db.commit()
    db.refresh(owner)
    
    # Create default vehicles
    vehicles = [
        Vehicle(
            owner_id=owner.id,
            category="car_rental",
            make="Toyota",
            model="Corolla",
            year=2022,
            color="Silver",
            license_plate="LEC-5566",
            price_per_day=50.0,
            price_per_hour=8.0,
            seats=5,
            transmission="automatic",
            fuel_type="hybrid",
            image_url="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=600&q=80",
            is_available=True
        ),
        Vehicle(
            owner_id=owner.id,
            category="luxury",
            make="Mercedes-Benz",
            model="S-Class",
            year=2023,
            color="Black",
            license_plate="VIP-777",
            price_per_day=250.0,
            price_per_hour=35.0,
            seats=5,
            transmission="automatic",
            fuel_type="petrol",
            image_url="https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=600&q=80",
            is_available=True
        ),
        Vehicle(
            owner_id=owner.id,
            category="bike_rental",
            make="Honda",
            model="CB500X",
            year=2021,
            color="Red",
            license_plate="BIKE-9922",
            price_per_day=35.0,
            price_per_hour=5.0,
            seats=2,
            transmission="manual",
            fuel_type="petrol",
            image_url="https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=600&q=80",
            is_available=True
        ),
        Vehicle(
            owner_id=owner.id,
            category="bus_coaster",
            make="Toyota",
            model="Coaster",
            year=2020,
            color="White",
            license_plate="BUS-8800",
            price_per_day=150.0,
            price_per_hour=25.0,
            seats=29,
            transmission="manual",
            fuel_type="diesel",
            image_url="https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=600&q=80",
            is_available=True
        )
    ]
    
    for v in vehicles:
        db.add(v)
        
    # Create default tours
    tours = [
        Tour(
            title="Hunza Valley Adventure",
            description="Explore the scenic landscapes of Hunza Valley, Attabad Lake, and Karimabad bazaar. Includes hotel stay and standard meals.",
            price=399.0,
            duration_days=7,
            itinerary="Day 1: Islamabad to Chilas, Day 2: Hunza Arrival, Day 3: Karimabad sights, Day 4: Khunjerab Pass excursion, Day 5: Attabad lake boat ride, Day 6: Travel back to Besham, Day 7: Return to Islamabad.",
            is_active=True
        ),
        Tour(
            title="Lahore Cultural Day Tour",
            description="Experience the history of Lahore: Badshahi Mosque, Lahore Fort, Shalimar Gardens, and traditional food street.",
            price=45.0,
            duration_days=1,
            itinerary="Morning: Badshahi Mosque & Lahore Fort, Afternoon: Shalimar Gardens, Evening: Food Street dinner.",
            is_active=True
        )
    ]
    
    for t in tours:
        db.add(t)
        
    db.commit()
    db.close()
    print("Database seeding completed.")

if __name__ == "__main__":
    seed_db()
