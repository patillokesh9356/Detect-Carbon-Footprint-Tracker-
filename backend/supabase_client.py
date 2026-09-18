import os
import sys
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Patch httpx SSL only on Windows (Linux/Render has proper certificates)
if sys.platform == "win32":
    import httpx

    _original_init = httpx.Client.__init__
    def _patched_init(self, *args, **kwargs):
        kwargs["verify"] = False
        _original_init(self, *args, **kwargs)
    httpx.Client.__init__ = _patched_init

    _original_async_init = httpx.AsyncClient.__init__
    def _patched_async_init(self, *args, **kwargs):
        kwargs["verify"] = False
        _original_async_init(self, *args, **kwargs)
    httpx.AsyncClient.__init__ = _patched_async_init

from supabase import create_client

# Create Supabase client
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("Supabase connection initialized successfully!")
