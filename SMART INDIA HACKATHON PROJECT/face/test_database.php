<?php
require_once __DIR__ . "/database/database_connection.php";

echo "Testing database connection and lecture login...\n\n";

// Test the exact query from the login.php
$email = 'mark@gmail.com';
$password = '@mark_';

echo "Testing with email: " . $email . "\n";
echo "Testing with password: " . $password . "\n\n";

try {
    $stmt = $pdo->prepare("SELECT * FROM tbllecture WHERE emailAddress = :email");
    $stmt->execute(['email' => $email]);
    $user = $stmt->fetch();
    
    if ($user) {
        echo "✅ User found in database:\n";
        echo "ID: " . $user['Id'] . "\n";
        echo "Name: " . $user['firstName'] . " " . $user['lastName'] . "\n";
        echo "Email: " . $user['emailAddress'] . "\n";
        echo "Stored password hash: " . $user['password'] . "\n\n";
        
        echo "Testing password verification:\n";
        if (password_verify($password, $user['password'])) {
            echo "✅ Password verification SUCCESSFUL\n";
            echo "Login should work!\n";
        } else {
            echo "❌ Password verification FAILED\n";
            echo "This is why login is failing!\n";
        }
    } else {
        echo "❌ No user found with email: " . $email . "\n";
    }
    
} catch (PDOException $e) {
    echo "❌ Database error: " . $e->getMessage() . "\n";
}

echo "\n" . str_repeat("=", 50) . "\n";
echo "Testing admin login as well...\n\n";

$admin_email = 'admin@gmail.com';
$admin_password = '@admin_';

try {
    $stmt = $pdo->prepare("SELECT * FROM tbladmin WHERE emailAddress = :email");
    $stmt->execute(['email' => $admin_email]);
    $admin = $stmt->fetch();
    
    if ($admin) {
        echo "✅ Admin found in database:\n";
        echo "ID: " . $admin['Id'] . "\n";
        echo "Name: " . $admin['firstName'] . " " . $admin['lastName'] . "\n";
        echo "Email: " . $admin['emailAddress'] . "\n";
        echo "Stored password hash: " . $admin['password'] . "\n\n";
        
        echo "Testing admin password verification:\n";
        if (password_verify($admin_password, $admin['password'])) {
            echo "✅ Admin password verification SUCCESSFUL\n";
        } else {
            echo "❌ Admin password verification FAILED\n";
        }
    } else {
        echo "❌ No admin found with email: " . $admin_email . "\n";
    }
    
} catch (PDOException $e) {
    echo "❌ Database error: " . $e->getMessage() . "\n";
}
?>
