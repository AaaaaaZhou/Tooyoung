<head>
    <meta charset="UTF-8">
</head>

<body>
<?php
include("conn.php");
$name = $_POST["UserName"];
$pw = $_POST["Password"];
$pw_check = $_POST["PasswordCheck"];
$searching = mysqli_query($link, "select UserName from UserInfo where UserName='$name'");
if ($name == NULL) {?>
    <h1>用户名不能为空</h1>
    <br/>
    <a href='register.html'>返回</a>
<?php
}
else  if ($pw == NULL) {?>
    <h1>密码不能为空</h1>
    <br/>
    <a href='register.html'>返回</a>
<?php
}
else if (mysqli_num_rows($searching) != 0) {?>
    <h1>用户名已存在</h1>
    <br/>
    <a href='register.html'>返回</a>
<?php
}
else if ($pw != $pw_check) {?>
    <h1>确认密码错误</h1>
    <br/>
    <a href='register.html'>返回</a>
<?php
}
else {
    $sql = "insert into UserInfo values('".$_POST["UserName"]."', '".$_POST["Password"]."', '".NULL."')";
    $result = mysqli_query($link, $sql);
    if($result) {?>
        <h1>注册成功</h1>
        <br/>
        <a href='homepage.php'>继续</a>
<?php
    }
    else {
        echo "Falied in SQL command: ";
        echo mysqli_error($link);
        echo "<br><a href='register.html'>continue</a>";
    }
}
mysqli_close($link);
?>
</body>
