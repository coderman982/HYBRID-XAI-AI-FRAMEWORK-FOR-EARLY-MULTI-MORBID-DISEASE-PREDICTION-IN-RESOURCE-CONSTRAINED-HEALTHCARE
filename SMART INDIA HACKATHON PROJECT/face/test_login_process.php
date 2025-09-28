<?php
session_start();
require_once __DIR__ . "/database/database_connection.php";

echo "=== COMPLETE LOGIN PROCESS TEST ===\n\n";

// Simulate the exact login process from login.php
$email = 'mark@gmail.com';
$password = '@mark_';
$userType = 'lecture';

echo "Testing login with:\n";
echo "Email: " . $email . "\n";
echo "Password: " . $password . "\n";
echo "User Type: " . $userType . "\n\n";

// Step 1: Validate email
echo "Step 1: Email validation\n";
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "❌ Invalid email format\n";
    exit();
} else {
    echo "✅ Email format is valid\n";
}

// Step 2: Check password not empty
echo "\nStep 2: Password validation\n";
if (empty($password)) {
    echo "❌ Password is empty\n";
    exit();
} else {
    echo "✅ Password is not empty\n";
}

// Step 3: Database query
echo "\nStep 3: Database query\n";
try {
    if ($userType == "lecture") {
        $stmt = $pdo->prepare("SELECT * FROM tbllecture WHERE emailAddress = :email");
        echo "Using lecture table query\n";
    } elseif ($userType == "administrator") {
        $stmt = $pdo->prepare("SELECT * FROM tbladmin WHERE emailAddress = :email");
        echo "Using admin table query\n";
    }
    
    $stmt->execute(['email' => $email]);
    $user = $stmt->fetch();
    
    if ($user) {
        echo "✅ User found in database\n";
        echo "User ID: " . $user['Id'] . "\n";
        echo "User Name: " . $user['firstName'] . "\n";
        echo "Stored Hash: " . $user['password'] . "\n";
    } else {
        echo "❌ No user found with email: " . $email . "\n";
        exit();
    }
} catch (PDOException $e) {
    echo "❌ Database error: " . $e->getMessage() . "\n";
    exit();
}

// Step 4: Password verification
echo "\nStep 4: Password verification\n";
if ($user && password_verify($password, $user['password'])) {
    echo "✅ Password verification successful\n";
    
    // Step 5: Session creation
    echo "\nStep 5: Session creation\n";
    $_SESSION['user'] = [
        'id' => $user['Id'],
        'email' => $user['emailAddress'],
        'name' => $user['firstName'],
        'role' => $userType,
    ];
    
    echo "✅ Session created successfully\n";
    echo "Session data:\n";
    print_r($_SESSION['user']);
    
    echo "\n🎉 LOGIN SHOULD BE SUCCESSFUL!\n";
    
} else {
    echo "❌ Password verification failed\n";
    echo "This is the problem!\n";
    
    // Debug information
    echo "\nDebug information:\n";
    echo "Input password: '" . $password . "'\n";
    echo "Password length: " . strlen($password) . "\n";
    echo "Stored hash: '" . $user['password'] . "'\n";
    echo "Hash length: " . strlen($user['password']) . "\n";
    
    // Test with different variations
    echo "\nTesting password variations:\n";
    $variations = [
        trim($password),
        rtrim($password),
        ltrim($password),
        $password . "\n",
        $password . "\r",
        $password . "\r\n",
        "\n" . $password,
        "\r" . $password,
        "\r\n" . $password
    ];
    
    foreach ($variations as $i => $variation) {
        if (password_verify($variation, $user['password'])) {
            echo "✅ Variation " . ($i + 1) . " works: '" . addslashes($variation) . "'\n";
        }
    }
}

echo "\n" . str_repeat("=", 60) . "\n";
echo "Session status: " . (session_status() === PHP_SESSION_ACTIVE ? "Active" : "Inactive") . "\n";
echo "Session ID: " . session_id() . "\n";
?>
