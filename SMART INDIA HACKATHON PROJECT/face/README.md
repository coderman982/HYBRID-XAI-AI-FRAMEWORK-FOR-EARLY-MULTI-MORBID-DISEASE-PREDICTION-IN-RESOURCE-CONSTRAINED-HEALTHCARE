# Face Recognition Attendance System

## 📌 Overview

The **Face Recognition Attendance System** is a web-based application that automates attendance marking using facial recognition technology. It eliminates the need for manual attendance and provides a secure, efficient, and user-friendly platform for teachers and students.

This project is specially designed for **rural schools**, optimized to run on **low-resource computers** with minimal requirements. It ensures accessibility and ease of use even in areas with limited technical infrastructure.

The system leverages **PHP** for backend logic, **MySQL** for database management, and **face-api.js** models for face detection, recognition, and expression analysis.

---

## 🚀 Features

* 👩‍🎓 **Student & Teacher Authentication** (Login system)
* 🧑‍🏫 **Lecture & Course Management**
* 📸 **Real-Time Face Recognition** for attendance
* 🗂️ **Database-Backed Attendance Records**
* 📊 **Admin Dashboard** for viewing and managing attendance
* 🔐 Secure sessions (recommend replacing plaintext `passwords.txt` with hashed storage)
* ⚡ Lightweight and browser-based implementation using **face-api.js** models
* 🏫 **Optimized for Rural Schools** — Can run on entry-level PCs with basic webcams

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** PHP 7+
* **Database:** MySQL
* **Face Recognition:** [face-api.js](https://github.com/justadudewhohacks/face-api.js)
* **Models Included:**

  * SSD Mobilenet V1
  * Face Landmark 68 / Tiny
  * Face Expression
  * Face Recognition
  * Age & Gender Estimation

---

## 📂 Project Structure

```
face/
│── index.php                  # Main entry point
│── add_lecture_data.php       # Add lecture details
│── check_lecture_table.php    # Verify lecture records
│── test_login_process.php     # Login testing script
│── test_database.php          # DB connection test
│── database/
│   ├── attendance-db.sql      # Database schema
│   └── database_connection.php# DB connection config
│── models/                    # Face-api.js pretrained models
│── resources/
│   ├── assets/css/            # Stylesheets
│   └── assets/javascript/     # Frontend scripts
│── docs/
│   ├── FACE_RECOGNITION_TROUBLESHOOTING.md
│   └── SETUP_STUDENT_IMAGES.md
│── README.md                  # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd face
```

### 2. Setup Database

1. Create a MySQL database (e.g., `attendance_system`).
2. Import the schema:

   ```sql
   source database/attendance-db.sql;
   ```
3. Update **`database_connection.php`** with your DB credentials.

### 3. Configure Web Server

* Place project inside your PHP server root (e.g., `htdocs/` for XAMPP).
* Ensure **PHP 7+** and **MySQL** are running.

### 4. Setup Student Images

Follow [SETUP_STUDENT_IMAGES.md](./SETUP_STUDENT_IMAGES.md) for guidelines on preparing training images.

### 5. Access Application

Open in browser:

```
http://localhost/face/
```

---

## 🧑‍💻 Usage

1. **Admin/Teacher Login** → Manage courses & lectures.
2. **Students** → Authenticate via camera for attendance.
3. **Admin Dashboard** → Review attendance records.

---

## 🛡️ Security Notes

* ❌ Do **NOT** use `passwords.txt` for storing credentials. Replace with hashed passwords in the DB (`bcrypt` recommended).
* ✅ Always configure proper session handling.
* 🔒 Use HTTPS in production.

---

## 🐛 Troubleshooting

See [FACE_RECOGNITION_TROUBLESHOOTING.md](./FACE_RECOGNITION_TROUBLESHOOTING.md) for common setup and runtime issues.

---

## 📜 License

This project is for **educational purposes only**. Modify and extend as needed for your institution or personal projects.

---

## 🙌 Acknowledgements

* [face-api.js](https://github.com/justadudewhohacks/face-api.js)
* PHP & MySQL community
* Open-source contributors
