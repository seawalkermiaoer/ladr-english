from dotenv import load_dotenv

from app.core.config import settings
load_dotenv()
from supabase import create_client, Client


def test_supabase_access():
    """Test Supabase access using environment variables."""
    # Get configuration from environment variables
    supabase_url = settings.SUPABASE_URL
    anon_key = settings.SUPABASE_ANON_KEY
    
    if not supabase_url or not anon_key:
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables")
        print("Example:")
        print("  export SUPABASE_URL='https://your-project.supabase.co'")
        print("  export SUPABASE_ANON_KEY='your-anon-key'")
        return
    supabase:Client = create_client(supabase_url=supabase_url, supabase_key=anon_key)
    response = supabase.functions.invoke("hello-world", invoke_options={"body": {"name": "Functions"}})
    print(response)
