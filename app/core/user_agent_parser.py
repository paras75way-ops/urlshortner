from user_agents import parse as parse_ua


def parse_user_agent(ua_string: str) -> dict:
    """Parse a User-Agent string and return browser, OS, and device type info."""
    if not ua_string:
        return {
            "browser": "Unknown",
            "os": "Unknown",
            "device_type": "Unknown",
        }

    user_agent = parse_ua(ua_string)

    # Determine device type
    if user_agent.is_mobile:
        device_type = "mobile"
    elif user_agent.is_tablet:
        device_type = "tablet"
    elif user_agent.is_pc:
        device_type = "desktop"
    elif user_agent.is_bot:
        device_type = "bot"
    else:
        device_type = "unknown"

    return {
        "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}".strip(),
        "os": f"{user_agent.os.family} {user_agent.os.version_string}".strip(),
        "device_type": device_type,
    }
