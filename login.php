<head>
    <meta charset="UFT-8">
</head>

<body>
<?php
session_start();

include("conn.php");
mysqli_select_db($link, $dbname);
if(isset($_POST["submit"])) {
    $query = "select * from UserInfo where UserName='{$_POST['name']}' and Password='{$_POST['password']}'";
    $result = mysqli_query($link, $query);
    if(mysqli_num_rows($result) == 1) {
        $_SESSION["name"] = $_POST['name'];
        header("Location: homepage.php");
    }
    else if(empty($_POST["name"])) {?>
        <h1>请填写用户名</h1>
        <br/>
        <a href='login.html'>返回</a>
<?php
    }
    else if(empty($_POST["password"])) {?>
        <h1>请填写密码</h1>
        <br/>
        <a href='login.html'>返回</a>
<?php
    }
    else {?>
        <h1>用户名或密码错误</h1>
        <br/>
        <a href='login.html'>返回</a>
<?php
    }
}
mysqli_close($link);
?>
</body>
