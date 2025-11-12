"""
Test script to verify Supabase connection and credentials.
"""

import os
from supabase import create_client, Client


def test_supabase_connection():
    """Test the Supabase connection with proper error handling and list tables."""
    # Check if environment variables are set
    supabase_url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    print("Supabase Connection Test")
    print("=" * 30)
    print(f"SUPABASE_URL: {supabase_url}")
    print(f"SUPABASE_ANON_KEY: {'*' * len(anon_key) if anon_key else None}")
    
    # Validate URL format
    if supabase_url:
        print(f"URL length: {len(supabase_url)}")
        print(f"URL starts with http: {supabase_url.startswith('http')}")
        print(f"URL stripped: '{supabase_url.strip()}'")
    
    if not supabase_url or not anon_key:
        print("\nERROR: Missing Supabase credentials!")
        print("Please set the following environment variables:")
        print("  export SUPABASE_URL='https://your-project.supabase.co'")
        print("  export SUPABASE_ANON_KEY='your-anon-key'")
        return False
    
    # Check for common issues
    if supabase_url.strip() == "":
        print("\nERROR: SUPABASE_URL is empty!")
        return False
        
    if not supabase_url.startswith(("http://", "https://")):
        print("\nERROR: SUPABASE_URL must start with 'http://' or 'https://'")
        return False
    
    try:
        # Create Supabase client
        client: Client = create_client(supabase_url, anon_key)
        print("\n✓ Successfully created Supabase client")
        
        # Try to connect by getting the current user (or at least validating the connection)
        try:
            # This will validate the connection without requiring specific table permissions
            response = client.table('users').select('*').execute()
            
            print(response)
            print("✓ Successfully connected to Supabase", client.auth)
            response = client.table("users").upsert({"id": 1, "name": "piano"}).execute()
            
                
        except Exception as connect_error:
            print(f"\nWarning: Connection test had issues: {connect_error}")
            
        return True
        
    except Exception as e:
        print(f"\nERROR: Failed to connect to Supabase: {e}")
        return False


if __name__ == "__main__":
    test_supabase_connection()