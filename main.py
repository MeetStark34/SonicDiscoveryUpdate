import os
import sys
import subprocess

def check_setup():
    """Checks if .env exists and python version is compatible."""
    if sys.version_info >= (3, 13):
        print("❌ Error: Python 3.13+ is not supported yet.")
        print("   Please use Python 3.10, 3.11, or 3.12.")
        return False

    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("   Please copy .env.example to .env and fill in your Spotify credentials.")
        return False
    
    print("✅ .env file found.")
    return True

def run_streamlit():
    """Runs the Streamlit app."""
    print("🚀 Launching Streamlit App...")
    file_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", file_path])

if __name__ == "__main__":
    print("=== Spotify Music Recommendation System ===")
    if check_setup():
        run_streamlit()
    else:
        print("\nSetup incomplete. Please fix the issues above and try again.")
