import httpx


async def get_geo_info(ip_address: str) -> dict:
    """Look up geolocation info for an IP address using ip-api.com (free, no key needed).
    
    Returns country and city. Falls back gracefully on errors.
    """
    # Skip private/local IPs
    if not ip_address or ip_address in ("127.0.0.1", "::1", "localhost"):
        return {"country": "Local", "city": "Local"}

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"http://ip-api.com/json/{ip_address}",
                params={"fields": "status,country,city"}
            )
            data = response.json()

            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                }
    except Exception:
        pass

    return {"country": "Unknown", "city": "Unknown"}
