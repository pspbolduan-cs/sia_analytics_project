# ============================================
# Author: Qian Zhu
# Date: 2025-12-08
# Singapore Airlines Analytics System
# Main Application Entry (Streamlit UI + CLI)
# ============================================

import sys
import logging
from PIL import Image
import pandas as pd

logging.basicConfig(level=logging.INFO)


# =====================================================================
# STREAMLIT UI MODE
# =====================================================================
def run_streamlit_ui():
    """
    Main Streamlit user interface entry point.
    This version loads global UI styling and directs the user
    to the multi-page interface via sidebar navigation.
    """
    import streamlit as st
    from services.ui_service import apply_global_styles

    # ---- Streamlit Page Setup ----
    st.set_page_config(
        page_title="Singapore Airlines Analytics System",
        page_icon="✈️",
        layout="wide"
    )

    # ---- Apply Global Styling ----
    apply_global_styles()

    # ---- Header Section ----
    st.title("Singapore Airlines Data Analytics System")
    st.subheader("Enterprise Cloud-Based Analytics Platform")

    # ---- Logo ----
    try:
        logo = Image.open("assets/singapore_airlines_logo.png")
        st.image(logo, width=280)
    except:
        st.warning("⚠️ Logo not found. Please place 'singapore_airlines_logo.png' inside /assets/.")

    # ---- Welcome Text ----
    st.markdown("""
Welcome to the **Singapore Airlines Analytics System**, a cloud-enabled platform that provides:

- Flight Performance Insights  
- Customer Experience Metrics  
- Risk & Scenario Simulations  
- Cloud-based Data Analytics  

Use the **left sidebar** to navigate between modules.
    """)

    st.markdown("---")

    # ---- Sidebar Navigation Overview ----
    st.subheader("📊 Available Analytics Modules")
    st.write("""
1. **Flight Performance Analytics**  
2. **Customer Experience Analytics**  
3. **Risk & Scenario Simulation**  
4. **Cloud Analytics**  
    """)

    logging.info("Streamlit UI loaded successfully.")



# =====================================================================
# CUSTOMER EXPERIENCE — CLI MODE
# =====================================================================
def run_customer_experience_cli():
    """
    CLI version of the Customer Experience Analytics module.
    Displays basic analysis directly in the terminal.
    """
    print("\n=======================================")
    print("      Customer Experience Module")
    print("=======================================\n")

    # ---- Load dataset ----
    try:
        df = pd.read_csv("assets/train.csv")

        # Convert satisfaction label to numeric score
        mapping = {
            "neutral or dissatisfied": 0,
            "satisfied": 1
        }
        df["satisfaction_score"] = df["satisfaction"].map(mapping).fillna(-1)

    except Exception:
        print("❌ ERROR: Cannot load 'assets/train.csv'.")
        input("\nPress ENTER to return...")
        return

    # ---- Output Statistics ----
    print(f"\n⭐ Average Satisfaction Score: {df['satisfaction_score'].mean():.2f}")

    print("\n📊 Satisfaction Distribution:")
    print(df["satisfaction"].value_counts())

    print("\n✔ CLI Customer Experience Analysis Completed.")
    input("\nPress ENTER to return to main menu...")


# =====================================================================
# CLI MAIN MENU
# =====================================================================
def run_cli():
    """
    Stand-alone CLI interface for users who prefer terminal mode.
    """
    logging.info("CLI mode activated.")

    while True:
        print("===========================================")
        print("   Singapore Airlines Analytics System (CLI)")
        print("===========================================\n")
        print("1. Flight Performance Analytics")
        print("2. Customer Experience Analytics")
        print("3. Risk & Scenario Simulation")
        print("4. Cloud Analytics")
        print("5. Exit\n")

        choice = input("Enter option (1–5): ")

        if choice == "1":
            print("[CLI] Flight Performance module not implemented in CLI mode yet.\n")

        elif choice == "2":
            run_customer_experience_cli()

        elif choice == "3":
            print("[CLI] Risk Simulation module not implemented in CLI mode yet.\n")

        elif choice == "4":
            print("[CLI] Cloud Analytics module not implemented in CLI mode yet.\n")

        elif choice == "5":
            print("Exiting system. Goodbye!")
            break

        else:
            print("❌ Invalid input. Please choose a valid option.")

        input("\nPress ENTER to return to main menu...")


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    # Run CLI:  python3 main.py cli
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        run_cli()
    else:
        # Run Streamlit:  streamlit run main.py
        run_streamlit_ui()
