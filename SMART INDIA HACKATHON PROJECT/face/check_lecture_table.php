<?php
require_once __DIR__ . "/database/database_connection.php";

echo "=== CHECKING LECTURE TABLE ===\n\n";

try {
    // Get all lecture records
    $stmt = $pdo->query("SELECT * FROM tbllecture");
    $lectures = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    echo "Total lectures in database: " . count($lectures) . "\n\n";
    
    if (count($lectures) > 0) {
        echo "All lecture records:\n";
        echo str_repeat("-", 80) . "\n";
        foreach ($lectures as $lecture) {
            echo "ID: " . $lecture['Id'] . "\n";
            echo "Name: " . $lecture['firstName'] . " " . $lecture['lastName'] . "\n";
            echo "Email: " . $lecture['emailAddress'] . "\n";
            echo "Password Hash: " . $lecture['password'] . "\n";
            echo "Phone: " . $lecture['phoneNo'] . "\n";
            echo "Faculty: " . $lecture['facultyCode'] . "\n";
            echo "Date Created: " . $lecture['dateCreated'] . "\n";
            echo str_repeat("-", 80) . "\n";
        }
    } else {
        echo "❌ No lecture records found in the database!\n";
    }
    
    // Check specifically for mark@gmail.com
    echo "\nChecking specifically for mark@gmail.com:\n";
    $stmt = $pdo->prepare("SELECT * FROM tbllecture WHERE emailAddress = ?");
    $stmt->execute(['mark@gmail.com']);
    $mark = $stmt->fetch();
    
    if ($mark) {
        echo "✅ Found mark@gmail.com in database\n";
        print_r($mark);
    } else {
        echo "❌ mark@gmail.com NOT found in database\n";
        
        // Check for similar emails
        echo "\nChecking for similar emails:\n";
        $stmt = $pdo->query("SELECT emailAddress FROM tbllecture WHERE emailAddress LIKE '%mark%'");
        $similar = $stmt->fetchAll(PDO::FETCH_COLUMN);
        
        if (count($similar) > 0) {
            echo "Similar emails found:\n";
            foreach ($similar as $email) {
                echo "- " . $email . "\n";
            }
        } else {
            echo "No similar emails found\n";
        }
    }
    
} catch (PDOException $e) {
    echo "❌ Database error: " . $e->getMessage() . "\n";
}
?>
