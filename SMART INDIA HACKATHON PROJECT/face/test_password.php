<?php
// Test script to verify password hashing and verification

// Test the lecture password from the database
$stored_hash = '$2y$10$/st06w2mh/4adxGE9yCxROHkqHp6SzRARGhfCIg95zC3cxqbmkpaW';
$test_password = '@mark_';

echo "Testing password verification:\n";
echo "Stored hash: " . $stored_hash . "\n";
echo "Test password: " . $test_password . "\n";

if (password_verify($test_password, $stored_hash)) {
    echo "✅ Password verification SUCCESSFUL\n";
} else {
    echo "❌ Password verification FAILED\n";
}

// Test if we can generate the same hash
$new_hash = password_hash($test_password, PASSWORD_DEFAULT);
echo "\nNew hash generated: " . $new_hash . "\n";

if (password_verify($test_password, $new_hash)) {
    echo "✅ New hash verification SUCCESSFUL\n";
} else {
    echo "❌ New hash verification FAILED\n";
}

// Test admin password as well
$admin_hash = '$2y$10$FIBqWvTOXRMoQOAB2FBz3uUbaCwRYTM1zQreFI6i/7v6Qi8y9R1i6';
$admin_password = '@admin_';

echo "\nTesting admin password:\n";
echo "Admin hash: " . $admin_hash . "\n";
echo "Admin password: " . $admin_password . "\n";

if (password_verify($admin_password, $admin_hash)) {
    echo "✅ Admin password verification SUCCESSFUL\n";
} else {
    echo "❌ Admin password verification FAILED\n";
}
?>
