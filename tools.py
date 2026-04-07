"""Custom tools cho TravelBuddy - Trợ lý Du lịch Việt Nam."""

import logging
from langchain_core.tools import tool

logger = logging.getLogger("travel_tools")

# ============================================================
# MOCK DATA
# ============================================================

FLIGHTS_DB: dict[tuple[str, str], list[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN156",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1450000,
            "class": "Economy",
        },
        {
            "airline": "VietJet Air",
            "flight_number": "VJ523",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890000,
            "class": "Economy",
        },
        {
            "airline": "Bamboo Airways",
            "flight_number": "QH202",
            "departure": "12:00",
            "arrival": "13:20",
            "price": 1100000,
            "class": "Economy",
        },
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN158",
            "departure": "18:00",
            "arrival": "19:20",
            "price": 2500000,
            "class": "Business",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN245",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 1800000,
            "class": "Economy",
        },
        {
            "airline": "VietJet Air",
            "flight_number": "VJ681",
            "departure": "10:30",
            "arrival": "12:45",
            "price": 1100000,
            "class": "Economy",
        },
        {
            "airline": "Bamboo Airways",
            "flight_number": "QH305",
            "departure": "14:00",
            "arrival": "16:15",
            "price": 1350000,
            "class": "Economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN201",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1600000,
            "class": "Economy",
        },
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN209",
            "departure": "14:00",
            "arrival": "16:10",
            "price": 3200000,
            "class": "Business",
        },
        {
            "airline": "VietJet Air",
            "flight_number": "VJ133",
            "departure": "09:00",
            "arrival": "11:10",
            "price": 990000,
            "class": "Economy",
        },
        {
            "airline": "Bamboo Airways",
            "flight_number": "QH101",
            "departure": "17:00",
            "arrival": "19:10",
            "price": 1200000,
            "class": "Economy",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN312",
            "departure": "07:30",
            "arrival": "08:50",
            "price": 1200000,
            "class": "Economy",
        },
        {
            "airline": "VietJet Air",
            "flight_number": "VJ452",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 650000,
            "class": "Economy",
        },
        {
            "airline": "Bamboo Airways",
            "flight_number": "QH150",
            "departure": "15:30",
            "arrival": "16:50",
            "price": 850000,
            "class": "Economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "flight_number": "VN405",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 950000,
            "class": "Economy",
        },
        {
            "airline": "VietJet Air",
            "flight_number": "VJ789",
            "departure": "12:00",
            "arrival": "13:00",
            "price": 550000,
            "class": "Economy",
        },
        {
            "airline": "Bamboo Airways",
            "flight_number": "QH410",
            "departure": "16:00",
            "arrival": "17:00",
            "price": 750000,
            "class": "Economy",
        },
    ],
}

HOTELS_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {
            "name": "Vinpearl Resort & Spa Đà Nẵng",
            "stars": 5,
            "price_per_night": 2500000,
            "area": "Bãi biển Non Nước",
            "rating": 4.8,
        },
        {
            "name": "Pullman Danang Beach Resort",
            "stars": 5,
            "price_per_night": 2200000,
            "area": "Bãi biển Mỹ Khê",
            "rating": 4.7,
        },
        {
            "name": "Sala Danang Beach Hotel",
            "stars": 4,
            "price_per_night": 1200000,
            "area": "Bãi biển Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Fivitel Danang Hotel",
            "stars": 3,
            "price_per_night": 650000,
            "area": "Trung tâm thành phố",
            "rating": 4.2,
        },
        {
            "name": "Memory Hostel Đà Nẵng",
            "stars": 2,
            "price_per_night": 250000,
            "area": "Gần cầu Rồng",
            "rating": 4.0,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort Phú Quốc",
            "stars": 5,
            "price_per_night": 3000000,
            "area": "Bãi Dài",
            "rating": 4.9,
        },
        {
            "name": "Sol Beach House Phú Quốc",
            "stars": 4,
            "price_per_night": 1800000,
            "area": "Bãi Trường",
            "rating": 4.6,
        },
        {
            "name": "Camia Resort & Spa",
            "stars": 4,
            "price_per_night": 1200000,
            "area": "Ông Lang",
            "rating": 4.4,
        },
        {
            "name": "Phu Quoc Dragon Hotel",
            "stars": 3,
            "price_per_night": 550000,
            "area": "Thị trấn Dương Đông",
            "rating": 4.1,
        },
        {
            "name": "9Station Hostel Phú Quốc",
            "stars": 2,
            "price_per_night": 200000,
            "area": "Thị trấn Dương Đông",
            "rating": 3.9,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel Saigon",
            "stars": 5,
            "price_per_night": 2800000,
            "area": "Quận 1",
            "rating": 4.7,
        },
        {
            "name": "Liberty Central Saigon",
            "stars": 4,
            "price_per_night": 1500000,
            "area": "Quận 1",
            "rating": 4.5,
        },
        {
            "name": "Alagon Saigon Hotel",
            "stars": 3,
            "price_per_night": 800000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Beautiful Saigon Hotel",
            "stars": 3,
            "price_per_night": 500000,
            "area": "Quận 3",
            "rating": 4.0,
        },
        {
            "name": "The Common Room Project",
            "stars": 2,
            "price_per_night": 180000,
            "area": "Quận 1",
            "rating": 4.2,
        },
    ],
}


# ============================================================
# HELPER
# ============================================================

def format_price(price: int) -> str:
    """Format giá tiền theo kiểu Việt Nam: 1.450.000đ"""
    return f"{price:,.0f}đ".replace(",", ".")


# ============================================================
# TOOLS
# ============================================================

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm chuyến bay giữa 2 thành phố Việt Nam.

    Args:
        origin: Thành phố xuất phát (VD: Hà Nội, Hồ Chí Minh)
        destination: Thành phố đến (VD: Đà Nẵng, Phú Quốc)
    """
    origin = origin.strip()
    destination = destination.strip()
    logger.info("search_flights called: origin='%s', destination='%s'", origin, destination)

    try:
        # Tìm theo chiều thuận
        flights = FLIGHTS_DB.get((origin, destination))

        # Nếu không tìm thấy, thử chiều ngược
        if flights is None:
            flights = FLIGHTS_DB.get((destination, origin))
            if flights is not None:
                logger.info("Tìm thấy tuyến ngược: %s → %s", destination, origin)

        if flights is None:
            available_routes = [f"{o} → {d}" for o, d in FLIGHTS_DB.keys()]
            logger.info("Không tìm thấy tuyến %s → %s", origin, destination)
            return (
                f"Không tìm thấy chuyến bay từ {origin} đến {destination}.\n"
                f"Các tuyến bay hiện có:\n"
                + "\n".join(f"  - {route}" for route in available_routes)
            )

        logger.info("Tìm thấy %d chuyến bay", len(flights))

        result = f"Các chuyến bay từ {origin} đến {destination}:\n\n"
        for i, flight in enumerate(flights, 1):
            result += (
                f"{i}. {flight['airline']} ({flight['flight_number']})\n"
                f"   Giờ bay: {flight['departure']} → {flight['arrival']}\n"
                f"   Hạng: {flight['class']}\n"
                f"   Giá: {format_price(flight['price'])}\n\n"
            )

        return result

    except Exception as e:
        logger.error("Lỗi search_flights: %s", e)
        return f"Đã xảy ra lỗi khi tìm chuyến bay: {str(e)}"


@tool
def search_hotels(city: str, max_price_per_night: int = 0) -> str:
    """Tìm khách sạn tại một thành phố Việt Nam.

    Args:
        city: Tên thành phố (VD: Đà Nẵng, Phú Quốc, Hồ Chí Minh)
        max_price_per_night: Giá tối đa mỗi đêm (VNĐ). Đặt 0 để không giới hạn.
    """
    city = city.strip()
    logger.info("search_hotels called: city='%s', max_price=%d", city, max_price_per_night)

    try:
        # Tìm thành phố (hỗ trợ tìm không phân biệt hoa thường)
        hotels = None
        for db_city, db_hotels in HOTELS_DB.items():
            if db_city.lower() == city.lower():
                hotels = db_hotels
                break

        if hotels is None:
            available_cities = ", ".join(HOTELS_DB.keys())
            logger.info("Không tìm thấy khách sạn tại %s", city)
            return (
                f"Không tìm thấy khách sạn tại {city}.\n"
                f"Các thành phố hiện có: {available_cities}"
            )

        # Lọc theo giá nếu có
        if max_price_per_night > 0:
            filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
            logger.info("Lọc theo giá <= %s: %d/%d khách sạn", format_price(max_price_per_night), len(filtered), len(hotels))
        else:
            filtered = hotels

        if not filtered:
            cheapest = min(hotels, key=lambda h: h["price_per_night"])
            return (
                f"Không có khách sạn nào tại {city} với giá dưới {format_price(max_price_per_night)}/đêm.\n"
                f"Khách sạn rẻ nhất hiện có: {cheapest['name']} - {format_price(cheapest['price_per_night'])}/đêm."
            )

        # Sắp xếp theo rating giảm dần (dùng sorted để không thay đổi data gốc)
        filtered = sorted(filtered, key=lambda h: h["rating"], reverse=True)

        result = f"Khách sạn tại {city}"
        if max_price_per_night > 0:
            result += f" (giá dưới {format_price(max_price_per_night)}/đêm)"
        result += ":\n\n"

        for i, hotel in enumerate(filtered, 1):
            stars = "⭐" * hotel["stars"]
            result += (
                f"{i}. {hotel['name']} {stars}\n"
                f"   Giá: {format_price(hotel['price_per_night'])}/đêm\n"
                f"   Khu vực: {hotel['area']}\n"
                f"   Đánh giá: {hotel['rating']}/5.0\n\n"
            )

        return result

    except Exception as e:
        logger.error("Lỗi search_hotels: %s", e)
        return f"Đã xảy ra lỗi khi tìm khách sạn: {str(e)}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách du lịch.

    Args:
        total_budget: Tổng ngân sách (VNĐ)
        expenses: Chuỗi các khoản chi, format: "hạng_mục:số_tiền,hạng_mục:số_tiền"
                  VD: "vé_máy_bay:1200000,khách_sạn:1500000,ăn_uống:500000"
    """
    logger.info("calculate_budget called: budget=%d, expenses='%s'", total_budget, expenses)

    try:
        # Parse chuỗi expenses
        expense_items: list[tuple[str, int]] = []
        parts = expenses.split(",")

        for part in parts:
            part = part.strip()
            if not part:
                continue
            if ":" not in part:
                return f"Lỗi format: '{part}' không đúng định dạng 'hạng_mục:số_tiền'. VD: vé_máy_bay:1200000"

            key, value = part.rsplit(":", 1)
            key = key.strip()
            try:
                amount = int(value.strip())
            except ValueError:
                return f"Lỗi: '{value.strip()}' không phải số hợp lệ trong mục '{key}'."
            expense_items.append((key, amount))

        if not expense_items:
            return "Không có khoản chi nào để tính toán."

        # Tính tổng
        total_expenses = sum(amount for _, amount in expense_items)
        remaining = total_budget - total_expenses

        logger.info("Tổng chi: %d, Còn lại: %d", total_expenses, remaining)

        # Format kết quả
        result = f"📊 BẢNG TÍNH NGÂN SÁCH DU LỊCH\n"
        result += f"{'=' * 40}\n\n"
        result += f"💵 Tổng ngân sách: {format_price(total_budget)}\n\n"
        result += f"📋 Chi tiết các khoản chi:\n"

        for key, amount in expense_items:
            display_key = key.replace("_", " ").title()
            result += f"   • {display_key}: {format_price(amount)}\n"

        result += f"\n{'─' * 40}\n"
        result += f"   Tổng chi: {format_price(total_expenses)}\n"

        if remaining >= 0:
            result += f"   ✅ Còn lại: {format_price(remaining)}\n"
            percentage = (total_expenses / total_budget * 100) if total_budget > 0 else 0
            result += f"   📈 Đã sử dụng: {percentage:.1f}% ngân sách\n"
        else:
            result += f"   ⚠️ VƯỢT NGÂN SÁCH: {format_price(abs(remaining))}\n"
            result += f"   Bạn cần tăng ngân sách hoặc giảm chi phí.\n"

        return result

    except Exception as e:
        logger.error("Lỗi calculate_budget: %s", e)
        return f"Đã xảy ra lỗi khi tính ngân sách: {str(e)}"
