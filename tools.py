"""Custom tools cho TravelBuddy - Trợ lý Du lịch Việt Nam."""

import logging
from langchain_core.tools import tool

logger = logging.getLogger("travel_tools")

# ============================================================
# MOCK DATA
# ============================================================

FLIGHTS_DB: dict[tuple[str, str], list[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
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
                f"{i}. {flight['airline']}\n"
                f"   Giờ bay: {flight['departure']} → {flight['arrival']}\n"
                f"   Hạng: {flight['class']}\n"
                f"   Giá: {format_price(flight['price'])}\n\n"
            )

        return result

    except Exception as e:
        logger.error("Lỗi search_flights: %s", e)
        return f"Đã xảy ra lỗi khi tìm chuyến bay: {str(e)}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Args:
        city: Tên thành phố (VD: Đà Nẵng, Phú Quốc, Hồ Chí Minh)
        max_price_per_night: Giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn.
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

        # Lọc theo giá
        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
        logger.info("Lọc theo giá <= %s: %d/%d khách sạn", format_price(max_price_per_night), len(filtered), len(hotels))

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
