import subprocess
import os
import sys

def main():
    """
    Run the Streamlit debate bot application
    """
    # Print welcome message
    print("Starting AI Debate Bot...")
    print("=" * 50)
    print("Make sure you have set up your MISTRAL_API_KEY in the environment variables.")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("Streamlit is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("Streamlit installed successfully!")
    
    # Check for Mistral API key
    if not os.environ.get("MISTRAL_API_KEY"):
        print("\n⚠️ Warning: MISTRAL_API_KEY environment variable not found.")
        print("Please obtain an API key from https://console.mistral.ai/")
        print("You can still run the application, but the debate bot will not work without an API key.\n")
    
    # Run the Streamlit app
    print("Launching Streamlit application...")
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()