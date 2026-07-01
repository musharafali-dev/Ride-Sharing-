import asyncio
from sqlalchemy import select
from app.infrastructure.database.session import async_session_maker
from app.infrastructure.database.models.user_model import VehicleModel
import dotenv

async def seed_fleet():
    fleet_data = [
        # Cars
        {
            "make": "Toyota",
            "model": "Camry",
            "year": 2023,
            "color": "Silver",
            "license_plate": "XYZ-1234",
            "category": "car",
            "capacity": 4,
            "price_per_hour": 15.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fd?auto=format&fit=crop&q=80&w=1000",
        },
        {
            "make": "Porsche",
            "model": "911 Carrera",
            "year": 2024,
            "color": "Red",
            "license_plate": "FAST-001",
            "category": "car",
            "capacity": 2,
            "price_per_hour": 75.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1503376760367-1b612164ad40?auto=format&fit=crop&q=80&w=1000",
        },
        # Vans
        {
            "make": "Ford",
            "model": "Transit",
            "year": 2022,
            "color": "White",
            "license_plate": "VAN-9999",
            "category": "van",
            "capacity": 12,
            "price_per_hour": 35.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1549683935-7c57d7ddfb5e?auto=format&fit=crop&q=80&w=1000",
        },
        {
            "make": "Mercedes-Benz",
            "model": "Sprinter",
            "year": 2023,
            "color": "Black",
            "license_plate": "MB-VAN-1",
            "category": "van",
            "capacity": 15,
            "price_per_hour": 50.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1615783307525-ee9f6b9bc1f9?auto=format&fit=crop&q=80&w=1000",
        },
        # Bikes
        {
            "make": "Yamaha",
            "model": "YZF-R3",
            "year": 2021,
            "color": "Blue",
            "license_plate": "BIK-123",
            "category": "bike",
            "capacity": 2,
            "price_per_hour": 10.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&q=80&w=1000",
        },
        {
            "make": "Kawasaki",
            "model": "Ninja 400",
            "year": 2022,
            "color": "Green",
            "license_plate": "NIN-888",
            "category": "bike",
            "capacity": 2,
            "price_per_hour": 12.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&q=80&w=1000",
        },
        # Coasters
        {
            "make": "Toyota",
            "model": "Coaster",
            "year": 2020,
            "color": "White",
            "license_plate": "CST-001",
            "category": "coaster",
            "capacity": 30,
            "price_per_hour": 90.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?auto=format&fit=crop&q=80&w=1000",
        },
        {
            "make": "Mitsubishi",
            "model": "Rosa",
            "year": 2019,
            "color": "Silver",
            "license_plate": "RSA-555",
            "category": "coaster",
            "capacity": 29,
            "price_per_hour": 85.0,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=1000",
        },
    ]

    async with async_session_maker() as session:
        # Check if vehicles exist
        result = await session.execute(select(VehicleModel))
        existing_vehicles = result.scalars().all()
        if existing_vehicles:
            print("Fleet already seeded!")
            return

        for v_data in fleet_data:
            # Note: is_available is handled by the default status (AVAILABLE) in VehicleModel
            # so we pop it out.
            v_data.pop("is_available", None)
            vehicle = VehicleModel(**v_data)
            session.add(vehicle)
        
        await session.commit()
        print(f"Successfully seeded {len(fleet_data)} vehicles!")

if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(seed_fleet())
