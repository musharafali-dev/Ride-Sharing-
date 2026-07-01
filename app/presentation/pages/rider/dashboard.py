# type: ignore
# pyright: reportGeneralTypeIssues=false, reportOptionalSubscript=false, reportAttributeAccessIssue=false, reportArgumentType=false
import reflex as rx
from app.presentation.states.auth_state import AuthState
from app.presentation.states.booking_state import BookingState

def header() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.icon("car", size=28, color="indigo"),
            rx.heading("SwiftRent", size="7", color="indigo", weight="bold"),
            spacing="2",
            align="center"
        ),
        rx.spacer(),
        rx.hstack(
            rx.text("Customer Portal", size="2", color="gray"),
            rx.button("Logout", on_click=AuthState.logout, size="2", variant="soft", color_scheme="red"),
            align="center",
            spacing="3"
        ),
        padding="16px 24px",
        border_bottom="1px solid var(--gray-4)",
        width="100%",
        align="center",
        background_color="white"
    )

def vehicle_card(vehicle: rx.Var) -> rx.Component:
    category_badge_color = rx.cond(
        vehicle["category"] == "car", "blue",
        rx.cond(
            vehicle["category"] == "van", "orange",
            rx.cond(
                vehicle["category"] == "bike", "green", "purple"
            )
        )
    )
    
    status_badge_color = rx.cond(
        vehicle["status"] == "available", "green", "red"
    )

    return rx.card(
        rx.vstack(
            # Top row: Brand & category badge
            rx.hstack(
                rx.vstack(
                    rx.heading(f"{vehicle['make']} {vehicle['model']}", size="4", weight="bold"),
                    rx.text(f"License: {vehicle['license_plate']}", size="1", color="gray"),
                    spacing="0"
                ),
                rx.spacer(),
                rx.badge(vehicle["category"].to(str).upper(), color_scheme=category_badge_color, variant="surface"),
                width="100%",
                align="center"
            ),
            
            # Middle: Vehicle Image
            rx.box(
                rx.image(
                    src=vehicle["image_url"],
                    width="100%",
                    height="160px",
                    object_fit="cover",
                    border_radius="6px"
                ),
                width="100%",
                padding_y="2px"
            ),
            
            # Specs: Year, Color, Status
            rx.hstack(
                rx.text(f"Year: {vehicle['year']}", size="2", color="slate"),
                rx.text(f"Color: {vehicle['color']}", size="2", color="slate"),
                rx.spacer(),
                rx.badge(vehicle["status"].to(str).upper(), color_scheme=status_badge_color, variant="solid"),
                width="100%",
                align="center"
            ),
            
            # Divider
            rx.divider(),
            
            # Price & Button
            rx.hstack(
                rx.vstack(
                    rx.text("Price per hour", size="1", color="gray"),
                    rx.text(f"${vehicle['price_per_hour']}", size="5", weight="bold", color="indigo"),
                    spacing="0"
                ),
                rx.spacer(),
                rx.cond(
                    vehicle["status"] == "available",
                    rx.button(
                        "Book Now",
                        on_click=lambda: BookingState.select_vehicle(vehicle),
                        color_scheme="indigo",
                        cursor="pointer"
                    ),
                    rx.button(
                        "Unavailable",
                        disabled=True,
                        variant="soft",
                        color_scheme="gray"
                    )
                ),
                width="100%",
                align="center"
            ),
            spacing="3",
            width="100%"
        ),
        width="100%",
        padding="12px"
    )

def booking_item(booking: rx.Var) -> rx.Component:
    status_color = rx.cond(
        booking["status"] == "pending", "amber",
        rx.cond(
            booking["status"] == "active", "green",
            rx.cond(
                booking["status"] == "completed", "gray", "red"
            )
        )
    )

    return rx.card(
        rx.hstack(
            # Left side: Vehicle specs
            rx.vstack(
                rx.hstack(
                    rx.heading(booking.to(dict)["vehicle"].to(dict)["make"].to(str) + " " + booking.to(dict)["vehicle"].to(dict)["model"].to(str), size="4", weight="bold"),
                    rx.badge(booking.to(dict)["vehicle"].to(dict)["category"].to(str).upper(), color_scheme="indigo", variant="outline"),
                    align="center",
                    spacing="2"
                ),
                rx.text("License Plate: " + booking.to(dict)["vehicle"].to(dict)["license_plate"].to(str), size="1", color="gray"),
                rx.text("Period: " + booking["start_time"].to(str) + " to " + booking["end_time"].to(str), size="2", color="slate"),
                spacing="1"
            ),
            rx.spacer(),
            # Right side: Pricing and actions
            rx.hstack(
                rx.vstack(
                    rx.text("Total Paid", size="1", color="gray"),
                    rx.text(f"${booking['total_fare']}", size="5", weight="bold", color="green"),
                    spacing="0",
                    align="end"
                ),
                rx.badge(booking["status"].to(str).upper(), color_scheme=status_color, variant="solid", size="2"),
                rx.cond(
                    (booking["status"] == "pending") | (booking["status"] == "active"),
                    rx.button(
                        "Cancel",
                        on_click=lambda: BookingState.cancel_booking(booking["id"]),
                        color_scheme="red",
                        variant="soft",
                        cursor="pointer"
                    )
                ),
                align="center",
                spacing="3"
            ),
            width="100%",
            align="center"
        ),
        width="100%",
        margin_bottom="12px"
    )

def booking_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title("Confirm Vehicle Reservation"),
                rx.dialog.description("Choose your rental duration details below:"),
                
                # Selected vehicle short info
                rx.cond(
                    BookingState.selected_vehicle,
                    rx.hstack(
                        rx.icon("car", size=20, color="indigo"),
                        rx.text(
                            f"{BookingState.selected_vehicle['make']} {BookingState.selected_vehicle['model']} - ${BookingState.selected_vehicle['price_per_hour']}/hr",
                            weight="medium"
                        ),
                        spacing="2",
                        padding_y="4px"
                    )
                ),
                
                # Start date/time
                rx.vstack(
                    rx.text("Rental Start Time", size="2", weight="medium"),
                    rx.input(
                        type="datetime-local",
                        value=BookingState.start_date,
                        on_change=BookingState.update_start_date,
                        width="100%"
                    ),
                    width="100%",
                    spacing="1"
                ),
                
                # End date/time
                rx.vstack(
                    rx.text("Rental End Time", size="2", weight="medium"),
                    rx.input(
                        type="datetime-local",
                        value=BookingState.end_date,
                        on_change=BookingState.update_end_date,
                        width="100%"
                    ),
                    width="100%",
                    spacing="1"
                ),
                
                # Dynamic cost calculation display
                rx.cond(
                    BookingState.estimated_fare > 0,
                    rx.vstack(
                        rx.divider(),
                        rx.hstack(
                            rx.text("Estimated Cost:", size="3", weight="medium"),
                            rx.text(f"${BookingState.estimated_fare}", size="5", weight="bold", color="green"),
                            width="100%",
                            align="center"
                        ),
                        width="100%"
                    )
                ),
                
                # Error/feedback display
                rx.cond(
                    BookingState.error_message,
                    rx.text(BookingState.error_message, color="red", size="2", weight="bold")
                ),
                
                # Buttons
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancel", variant="soft", color_scheme="gray", on_click=BookingState.close_modal)
                    ),
                    rx.button(
                        "Confirm Rental",
                        on_click=BookingState.confirm_booking,
                        loading=BookingState.is_booking,
                        color_scheme="indigo"
                    ),
                    width="100%",
                    justify="end",
                    spacing="3"
                ),
                spacing="4",
                width="100%"
            ),
            max_width="450px"
        ),
        open=BookingState.is_modal_open,
        on_open_change=lambda _: BookingState.close_modal()
    )

def rider_dashboard() -> rx.Component:
    return rx.vstack(
        header(),
        rx.box(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Browse Fleet", value="browse"),
                    rx.tabs.trigger("My Bookings", value="bookings"),
                ),
                rx.tabs.content(
                    # Browse Fleet tab content
                    rx.vstack(
                        # Search & Filter bar
                        rx.hstack(
                            rx.input(
                                placeholder="Search by brand, color, plate...",
                                on_change=BookingState.set_search_query,
                                width="300px",
                                size="2"
                            ),
                            rx.spacer(),
                            # Category pills
                            rx.hstack(
                                rx.button(
                                    "All",
                                    on_click=lambda: BookingState.set_category_filter("all"),
                                    color_scheme=rx.cond(BookingState.category_filter == "all", "indigo", "gray"),
                                    variant=rx.cond(BookingState.category_filter == "all", "solid", "soft"),
                                    size="2"
                                ),
                                rx.button(
                                    "Cars",
                                    on_click=lambda: BookingState.set_category_filter("car"),
                                    color_scheme=rx.cond(BookingState.category_filter == "car", "indigo", "gray"),
                                    variant=rx.cond(BookingState.category_filter == "car", "solid", "soft"),
                                    size="2"
                                ),
                                rx.button(
                                    "Vans",
                                    on_click=lambda: BookingState.set_category_filter("van"),
                                    color_scheme=rx.cond(BookingState.category_filter == "van", "indigo", "gray"),
                                    variant=rx.cond(BookingState.category_filter == "van", "solid", "soft"),
                                    size="2"
                                ),
                                rx.button(
                                    "Bikes",
                                    on_click=lambda: BookingState.set_category_filter("bike"),
                                    color_scheme=rx.cond(BookingState.category_filter == "bike", "indigo", "gray"),
                                    variant=rx.cond(BookingState.category_filter == "bike", "solid", "soft"),
                                    size="2"
                                ),
                                rx.button(
                                    "Coasters",
                                    on_click=lambda: BookingState.set_category_filter("coaster"),
                                    color_scheme=rx.cond(BookingState.category_filter == "coaster", "indigo", "gray"),
                                    variant=rx.cond(BookingState.category_filter == "coaster", "solid", "soft"),
                                    size="2"
                                ),
                                spacing="2"
                            ),
                            width="100%",
                            padding_y="12px"
                        ),
                        
                        # Catalog Grid
                        rx.cond(
                            BookingState.filtered_vehicles.length() > 0,
                            rx.grid(
                                rx.foreach(
                                    BookingState.filtered_vehicles,
                                    vehicle_card
                                ),
                                columns="3",
                                spacing="4",
                                width="100%"
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.icon("search", size=48, color="gray"),
                                    rx.text("No vehicles match your search or filter.", color="gray"),
                                    spacing="2",
                                    padding="48px"
                                ),
                                width="100%"
                            )
                        ),
                        width="100%"
                    ),
                    value="browse"
                ),
                rx.tabs.content(
                    # My Bookings tab content
                    rx.vstack(
                        rx.heading("Your Rental History", size="5", weight="bold", margin_bottom="12px"),
                        rx.cond(
                            BookingState.my_bookings.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    BookingState.my_bookings,
                                    booking_item
                                ),
                                width="100%"
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.icon("calendar", size=48, color="gray"),
                                    rx.text("You have no booking reservations yet.", color="gray"),
                                    spacing="2",
                                    padding="48px"
                                ),
                                width="100%"
                            )
                        ),
                        width="100%"
                    ),
                    value="bookings"
                ),
                default_value="browse",
                width="100%"
            ),
            width="100%",
            padding="24px"
        ),
        # Embed booking modal
        booking_modal(),
        on_mount=BookingState.on_load,
        min_height="100vh",
        background_color="var(--gray-2)",
        width="100%"
    )
