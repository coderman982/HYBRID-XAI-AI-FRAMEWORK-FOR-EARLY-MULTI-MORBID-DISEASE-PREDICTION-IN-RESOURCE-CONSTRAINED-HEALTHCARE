<?php

require_once __DIR__ . "/../../database/database_connection.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $attendanceData = json_decode(file_get_contents("php://input"), true);

    if (!empty($attendanceData)) {
        foreach ($attendanceData as $data) {
            $studentID = $data['studentID'];
            $attendanceStatus = $data['attendanceStatus'];
            $course = $data['course'];
            $unit = $data['unit'];
            $date = date("Y-m-d"); 

            $sql = "INSERT INTO tblattendance(studentRegistrationNumber, course, unit, attendanceStatus, dateMarked)  
                    VALUES (:studentID, :course, :unit, :attendanceStatus, :date)";
            
            $stmt = $pdo->prepare($sql);
            if ($stmt->execute([
                ':studentID' => $studentID,
                ':course' => $course,
                ':unit' => $unit,
                ':attendanceStatus' => $attendanceStatus,
                ':date' => $date
            ])) {
                echo "Attendance data for student ID $studentID inserted successfully.<br>";
            } else {
                echo "Error inserting attendance data: " . implode(', ', $stmt->errorInfo()) . "<br>";
            }
        }
    } else {
        echo "No attendance data received.<br>";
    }
} else {
    echo "Invalid request method.<br>";
}

?>
