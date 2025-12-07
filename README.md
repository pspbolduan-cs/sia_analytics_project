# ✈️ Singapore Airlines Data Analytics System  
### CN6001 Enterprise Application & Cloud Computing – Coursework Project  
- **Team Leader:** Qian Zhu
- **Team Members:** Charles, Philippe, Ruitao He

---

## 📌 1. Project Overview  

This project implements a **cloud-based data analytics platform for Singapore Airlines**, built using:

- **Python**
- **Streamlit Web Framework**
- **Modular Service Architecture**
- **Cloud Execution (Streamlit Cloud)**

Because real SIA operational data is confidential, the system uses a synthetic dataset (`train.csv`) to simulate real airline operations and demonstrate the analytics pipeline.

The platform is fully interactive, visual, and deployed online so that instructors and stakeholders can run it without installing anything locally.

---

## 📌 2. System Features  

The application provides four key analytics modules:

### **1. Flight Performance Analytics**
- Fuel consumption trend analysis  
- Operational metrics visualisation  
- Flight performance indicators  

### **2. Customer Experience Analytics**
- Rating distribution  
- Satisfaction estimation  
- Customer segments analysis  

### **3. Risk & Scenario Simulation**
- Monte-Carlo risk modelling  
- Delay scenario simulation  
- Operational uncertainty analysis  

### **4. Cloud-Based Real-Time Analytics**
- Live processing through cloud resources  
- Demonstration of cloud execution capabilities  
- Scalability and serverless architecture  

Each module is implemented as an independent page under the `pages/` directory following Streamlit’s multi-page structure.

---

## 📌 3. Project Architecture  

```

sia_analytics_project/
│
├── main.py                    # Main homepage & navigation
├── assets/
│   ├── train.csv              # Synthetic dataset
│   └── singapore_airlines_logo.png
│
├── pages/
│   ├── 1_Flight_Performance.py
│   ├── 2_Customer_Experience.py
│   ├── 3_Risk_Simulation.py
│   └── 4_Cloud_Analytics.py
│
├── services/
│   ├── data_service.py        # Centralised data loading
│   └── simulation_service.py  # Simulation helpers
│
└── requirements.txt

```

The design follows a **clean modular architecture**:

- **main.py** – Acts as the front controller  
- **services/** – Business logic  
- **pages/** – Presentation layer (UI)  
- **assets/** – Data and static files  

This structure keeps the code organised and makes collaboration easier for all team members.

---

## 📌 4. Installation & Running Locally  

### **Step 1: Clone the repository**
```

git clone [https://github.com/ashlllll/sia_analytics_project.git](https://github.com/ashlllll/sia_analytics_project.git)
cd sia_analytics_project

```

### **Step 2: Install dependencies**
```

pip install -r requirements.txt

```

### **Step 3: Run Streamlit**
```

streamlit run main.py

```

The application will open automatically in your browser at:
```

[http://localhost:8501](http://localhost:8501)

```

---

## 📌 5. Cloud Deployment (Streamlit Cloud)

This project is fully deployable on **Streamlit Cloud**, which satisfies the coursework requirement:

> “The system must run in a cloud computing environment (e.g., Google Colab, AWS).”

Deployment steps:

1. Go to https://streamlit.io/cloud  
2. Select **New App**
3. Choose the GitHub repository:
```

ashlllll/sia_analytics_project

```
4. Set the entrypoint to:
```

main.py

```
5. Deploy

The platform will generate a public URL for access.

---

## 📌 6. Team Members & Responsibilities  

| Member | Responsibility |
|--------|----------------|
| **Qian Zhu (Leader)** | System architecture, project setup, main menu UI, GitHub setup, cloud deployment |
| Charles | Function 1 – Flight Performance Analytics |
| Ruitao He | Function 2 – Customer Experience Analytics |
| Philippe | Function 3 & 4 – Risk Simulation + Cloud Analytics |

---

## 📌 7. Dataset Information  

The dataset used in this project is **synthetic** and included under `assets/train.csv`.

Columns simulate realistic airline operational metrics such as:

- Fuel consumption  
- Delay minutes  
- Passenger satisfaction  
- Risk factors  
- Operational KPIs  

This dataset allows the team to demonstrate analytics logic without using confidential airline data.

---

## 📌 8. How to Contribute  

This repository is team-collaborative. To work on your module:

1. Create a new branch:
```

git checkout -b feature/your_module

```

2. Commit your changes:
```

git add .
git commit -m "Add my module"

```

3. Push:
```

git push origin feature/your_module

```

4. Create a Pull Request (PR)

---

## 📌 9. License  

This project is for **academic use only** under CN6001 coursework.  
Commercial use is not permitted.

---

## 📌 10. Acknowledgements  

- Singapore Airlines (concept only)  
- Streamlit Team  
- CN6001 Module Lecturers  

---

```

⭐ Thank you for reviewing our project!
