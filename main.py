# ============================================
# Singapore Airlines Analytics System
# Main Application Entry (Streamlit UI + CLI)
# ============================================

import streamlit as st
import logging
from PIL import Image
import sys

logging.basicConfig(level=logging.INFO)


# ---------------------------------------------
# STREAMLIT UI
# ---------------------------------------------
def run_streamlit_ui():
    st.set_page_config(
        page_title="Singapore Airlines Analytics System",
        page_icon="✈️",
        layout="wide",
    )

    st.title("Singapore Airlines Data Analytics System")
    st.subheader("Enterprise Cloud-Based Analytics Platform")

    try:
        logo = Image.open("assets/singapore_airlines_logo.png")
        st.image(logo, width=300)
    except:
        st.warning("⚠️ Logo not found. Place it inside /assets/")

    st.markdown("""
Welcome to the **Singapore Airlines Analytics System**, built using:

- Python  
- Streamlit Web Framework  
- Cloud Execution  
- Data-Driven Analytics  

Use the **sidebar** to navigate between modules.
""")

    st.markdown("---")

    st.subheader("📊 Available Modules")
    st.write("""
1. **Flight Performance Analytics**  
2. **Customer Experience Analytics**  
3. **Risk & Scenario Simulation**  
4. **Cloud Analytics**  
""")

    logging.info("Streamlit UI rendered successfully.")


# ---------------------------------------------
# CLI MODE
# ---------------------------------------------
def run_cli():
    logging.info("CLI mode activated.")

    while True:
        print("===========================================")
        print(" Singapore Airlines Analytics System (CLI) ")
        print("===========================================")
        print("\nSelect an analytics module:")
        print("1. Flight Performance Analytics")
        print("2. Customer Experience Analytics")
        print("3. Risk & Scenario Simulation")
        print("4. Cloud Analytics")
        print("5. Exit\n")

        choice = input("Enter option (1–5): ")

        if choice == "1":
            print("[CLI] Running Flight Performance Module...")
        elif choice == "2":
            print("[CLI] Running Customer Experience Module...")
        elif choice == "3":
            print("[CLI] Running Risk Simulation Module...")
        elif choice == "4":
            print("[CLI] Running Cloud Analytics Module...")
        elif choice == "5":
            print("Exiting system...")
            break
        else:
            print("Invalid option. Try again.")

        logging.info(f"CLI selection: {choice}")
        input("\nPress ENTER to return to main menu...")


# ---------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------
if __name__ == "__main__":
    # Case 1: python main.py cli   → run CLI
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        run_cli()
    else:
        # Case 2: streamlit run main.py → run Streamlit
        run_streamlit_ui()
