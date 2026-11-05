"""Common validation and safe input helpers."""
import ipaddress, re
def valid_host(value):
    value = value.strip()
    if not value or len(value) > 253 or any(c.isspace() for c in value): return False
    try: ipaddress.ip_address(value); return True
    except ValueError: pass
    return bool(re.fullmatch(r"(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?))*", value))
def confirm_authorization():
    answer = input("I own this system or have written permission. Type YES to continue: ")
    return answer == "YES"
def pause(): input("\\nPress Enter to continue...")
