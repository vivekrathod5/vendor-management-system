import random
import string
from vendors.models import Vendor

def generate_random_string(length=9):
    """Generate a random string of specified length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length)).upper()


def generate_vendor_code():
    """Generate a unique vendor code."""
    vendor_code = "V" + generate_random_string()
    if Vendor.objects.filter(vendor_code=vendor_code).exists():
        return generate_vendor_code()  # Call itself recursively until a unique vendor code is generated
    else:
        return vendor_code