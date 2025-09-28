# **Face Recognition Attendance System**

A robust system designed to authenticate individuals and record attendance using **facial recognition technology** powered by deep learning. This project simplifies attendance tracking for classrooms, workplaces, or events.


---

## **📋 Features**

- Role-based access for **administrators**, **lecturers**.
- Manage courses, units, venues, and attendance records through an intuitive interface.
- Capture and store multiple images for accurate identification.

- Good for college project

## Project Structure

````
## Project Structure

```plaintext
face/
│── index.php # Main entry point
│── add_lecture_data.php # Add lecture details
│── check_lecture_table.php # Verify lecture records
│── test_login_process.php # Login testing script
│── test_database.php # DB connection test
│── database/
│ ├── attendance-db.sql # Database schema
│ └── database_connection.php# DB connection config
│── models/ # Face-api.js pretrained models
│── resources/
│ ├── assets/css/ # Stylesheets
│ └── assets/javascript/ # Frontend scripts
│── docs/
│ ├── FACE_RECOGNITION_TROUBLESHOOTING.md
│ └── SETUP_STUDENT_IMAGES.md
│── README.md # Project documentation


````

- 
**Select lecture user type, to be able to login as lecture**

  *if you have issues using this email and password, create your lecture on admin panel*

- **Email**: `mark@gmail.com`
- **Password**: `@mark_`

As a lecturer:

- Select a course, unit, and venue on the home page.
- Launch the **Face Recognition** feature to begin attendance.

### Additional Features for the Lecturer Panel

- You can also export the attendance to an **Excel** sheet.
- Other simple features are available for managing the lecture panel.

Usage

Admin/Teacher Login → Manage courses & lectures.

Students → Authenticate via camera for attendance.

Admin Dashboard → Review attendance records