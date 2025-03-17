### **RODS Compliance Tool**  
**SpotterRODS** is a **Django + React** web application designed to help **interstate truck drivers** and **motor carriers** comply with **FMCSA Hours of Service (HOS)** regulations. This tool simplifies tracking **Record of Duty Status (RODS)**, enforces **Electronic Logging Device (ELD)** requirements, and ensures adherence to **FMCSA** rules. Key features include real-time duty status logging, sleeper berth tracking, 30-minute break reminders, and automatic RODS generation. Dockerized for easy deployment, this app enhances road safety and reduces driver fatigue while streamlining compliance for motor carriers. 🚛💨  

---

### **Key Features**
- **Real-Time Duty Status Logging**: Track **On-Duty**, **Driving**, **Off-Duty**, and **Sleeper Berth** statuses.  
- **Sleeper Berth Provision**: Manage split rest periods (e.g., **7/3** or **8/2 splits**).  
- **30-Minute Break Reminder**: Get notified after **8 cumulative hours of driving**.  
- **60/70-Hour On-Duty Limit**: Track rolling **7-day or 8-day on-duty limits**.  
- **34-Hour Restart**: Reset the **60/70-hour clock** with a **34-hour restart**.  
- **Exceptions Handling**: Log **adverse driving conditions** and **short-haul exceptions**.  
- **RODS Generation**: Automatically generate **FMCSA-compliant RODS logs**.  

---

### **Technology Stack**
- **Frontend**: React (with **React Router** and **Axios**).  
- **Backend**: Django (with **Django REST Framework**).  
- **Database**: PostgreSQL.  
- **Deployment**: Dockerized for seamless deployment on **Heroku**, **AWS**, or **DigitalOcean**.  

---

### **Getting Started**
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/rods-compliance-tool.git
   ```
2. Run the app with Docker:  
   ```bash
   docker-compose up
   ```
3. Access the app:  
   - Backend: `http://localhost:8000`  
   - Frontend: `http://localhost:3000`  

---

### **Why Use This Tool?**
- **Simplify Compliance**: Automate HOS tracking and RODS generation.  
- **Enhance Safety**: Reduce driver fatigue with real-time alerts and reminders.  
- **Dockerized**: Easy to deploy and scale in any environment.  

---
