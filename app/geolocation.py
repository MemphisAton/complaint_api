import requests

def get_ip_location(ip: str) -> str:
    """Возвращает строку с локацией (страна, регион, город) по IP через ip-api.com."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            country = data.get("country", "")
            region = data.get("regionName", "")
            city = data.get("city", "")
            return ", ".join(filter(None, [country, region, city]))
        else:
            return "unknown"
    except Exception:
        return "unknown"
