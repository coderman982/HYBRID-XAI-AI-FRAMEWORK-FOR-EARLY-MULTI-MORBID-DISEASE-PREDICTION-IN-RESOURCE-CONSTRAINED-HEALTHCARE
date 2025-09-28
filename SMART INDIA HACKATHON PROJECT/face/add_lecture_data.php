<?php
require_once __DIR__ . "/database/database_connection.php";

echo "=== ADDING LECTURE DATA TO DATABASE ===\n\n";

try {
    // Check if lecture already exists
    $stmt = $pdo->prepare("SELECT * FROM tbllecture WHERE emailAddress = ?");
    $stmt->execute(['mark@gmail.com']);
    $existing = $stmt->fetch();
    
    if ($existing) {
        echo "❌ Lecture with email mark@gmail.com already exists\n";
        print_r($existing);
    } else {
        echo "Adding new lecture record...\n";
        
        // Hash the password
        $password = '@mark_';
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        
        echo "Original password: " . $password . "\n";
        echo "Hashed password: " . $hashed_password . "\n\n";
        
        // Insert the lecture record
        $sql = "INSERT INTO tbllecture (firstName, lastName, emailAddress, password, phoneNo, facultyCode, dateCreated) VALUES (?, ?, ?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        
        $result = $stmt->execute([
            'mark',
            'lila', 
            'mark@gmail.com',
            $hashed_password,
            '07123456789',
            'CIT',
            '2024-04-07'
        ]);
        
        if ($result) {
            echo "✅ Lecture record added successfully!\n";
            echo "New lecture ID: " . $pdo->lastInsertId() . "\n";
        } else {
            echo "❌ Failed to add lecture record\n";
        }
    }
    
    // Verify the data was added
    echo "\nVerifying lecture data...\n";
    $stmt = $pdo->query("SELECT * FROM tbllecture");
    $lectures = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    echo "Total lectures in database: " . count($lectures) . "\n";
    
    if (count($lectures) > 0) {
        echo "\nAll lecture records:\n";
        foreach ($lectures as $lecture) {
            echo "ID: " . $lecture['Id'] . "\n";
            echo "Name: " . $lecture['firstName'] . " " . $lecture['lastName'] . "\n";
            echo "Email: " . $lecture['emailAddress'] . "\n";
            echo "Password Hash: " . $lecture['password'] . "\n";
            echo "Phone: " . $lecture['phoneNo'] . "\n";
            echo "Faculty: " . $lecture['facultyCode'] . "\n";
            echo "Date Created: " . $lecture['dateCreated'] . "\n";
            echo str_repeat("-", 50) . "\n";
        }
    }
    
} catch (PDOException $e) {
    echo "❌ Database error: " . $e->getMessage() . "\n";
}
?>
