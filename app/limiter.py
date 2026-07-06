from slowapi import Limiter
from slowapi.util import get_remote_address

# Ограничение частоты заявок с одного IP — защита от спама.
limiter = Limiter(key_func=get_remote_address, default_limits=["60/hour"])
