# type: ignore
# pyright: reportGeneralTypeIssues=false, reportOptionalSubscript=false, reportAttributeAccessIssue=false, reportArgumentType=false
import reflex as rx
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.presentation.states.auth_state import AuthState

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

class BookingState(rx.State):
    # Fleet catalog
    vehicles: List[Dict[str, Any]] = []
    category_filter: str = "all"  # all, car, van, bike, coaster
    search_query: str = ""
    
    # Booking process
    selected_vehicle: Optional[Dict[str, Any]] = None
    start_date: str = ""
    end_date: str = ""
    estimated_fare: float = 0.0
    is_booking: bool = False
    is_modal_open: bool = False

    # Booking history
    my_bookings: List[Dict[str, Any]] = []
    
    # Feedback
    error_message: str = ""
    success_message: str = ""

    # Removed headers computed var

    @rx.var
    def filtered_vehicles(self) -> List[Dict[str, Any]]:
        result = []
        for v in self.vehicles:
            # Filter by category
            if self.category_filter != "all" and v["category"] != self.category_filter:
                continue
            # Filter by search query
            if self.search_query:
                query = self.search_query.lower()
                name = f"{v['make']} {v['model']}".lower()
                if query not in name and query not in v["color"].lower() and query not in v["license_plate"].lower():
                    continue
            result.append(v)
        return result

    async def fetch_vehicles(self):
        self.error_message = ""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE_URL}/vehicles")
                if response.status_code == 200:
                    self.vehicles = response.json()
                else:
                    self.error_message = "Failed to load vehicle catalog."
        except Exception as e:
            self.error_message = f"Connection failure: {str(e)}"

    async def fetch_bookings(self):
        self.error_message = ""
        try:
            auth_state = await self.get_state(AuthState)
            headers = {"Authorization": f"Bearer {auth_state.access_token}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{API_BASE_URL}/bookings/me",
                    headers=headers
                )
                if response.status_code == 200:
                    self.my_bookings = response.json()
                else:
                    self.error_message = "Failed to load booking history."
        except Exception as e:
            self.error_message = f"Connection failure: {str(e)}"

    def set_category_filter(self, val: str):
        self.category_filter = val

    def set_search_query(self, val: str):
        self.search_query = val

    def select_vehicle(self, vehicle: Dict[str, Any]):
        self.selected_vehicle = vehicle
        self.start_date = ""
        self.end_date = ""
        self.estimated_fare = 0.0
        self.error_message = ""
        self.success_message = ""
        self.is_modal_open = True

    def close_modal(self):
        self.is_modal_open = False
        self.selected_vehicle = None

    def update_start_date(self, val: str):
        self.start_date = val
        self.calculate_estimate()

    def update_end_date(self, val: str):
        self.end_date = val
        self.calculate_estimate()

    def calculate_estimate(self):
        if not self.selected_vehicle or not self.start_date or not self.end_date:
            self.estimated_fare = 0.0
            return
        try:
            # Reflex datetime-local returns "YYYY-MM-DDTHH:MM"
            start = datetime.fromisoformat(self.start_date)
            end = datetime.fromisoformat(self.end_date)
            if start >= end:
                self.estimated_fare = 0.0
                return
            duration = end - start
            hours = max(1.0, duration.total_seconds() / 3600.0)
            self.estimated_fare = round(hours * self.selected_vehicle["price_per_hour"], 2)
        except Exception:
            self.estimated_fare = 0.0

    async def confirm_booking(self):
        if not self.selected_vehicle or not self.start_date or not self.end_date:
            self.error_message = "Please fill in all booking details."
            return
            
        self.is_booking = True
        self.error_message = ""
        self.success_message = ""
        
        try:
            # ISO 8601 formatting for payload
            start_iso = datetime.fromisoformat(self.start_date).isoformat()
            end_iso = datetime.fromisoformat(self.end_date).isoformat()
            
            auth_state = await self.get_state(AuthState)
            headers = {"Authorization": f"Bearer {auth_state.access_token}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/bookings",
                    headers=headers,
                    json={
                        "vehicle_id": self.selected_vehicle["id"],
                        "start_time": start_iso,
                        "end_time": end_iso
                    }
                )
                if response.status_code == 201:
                    self.success_message = "Vehicle booked successfully!"
                    self.is_modal_open = False
                    await self.fetch_vehicles()
                    await self.fetch_bookings()
                else:
                    self.error_message = response.json().get("detail", "Failed to book vehicle.")
        except Exception as e:
            self.error_message = f"Connection error: {str(e)}"
        finally:
            self.is_booking = False

    async def cancel_booking(self, booking_id: str):
        self.error_message = ""
        self.success_message = ""
        try:
            auth_state = await self.get_state(AuthState)
            headers = {"Authorization": f"Bearer {auth_state.access_token}"}
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_BASE_URL}/bookings/{booking_id}/cancel",
                    headers=headers
                )
                if response.status_code == 200:
                    self.success_message = "Booking cancelled successfully!"
                    await self.fetch_vehicles()
                    await self.fetch_bookings()
                else:
                    self.error_message = response.json().get("detail", "Failed to cancel booking.")
        except Exception as e:
            self.error_message = f"Connection error: {str(e)}"

    async def on_load(self):
        # Triggered when dashboard page mounts
        await self.fetch_vehicles()
        await self.fetch_bookings()
