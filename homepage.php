<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>tooyoung</title>
    <style type="text/css">
        body {
            background-image: url(image/bg.jpg);
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
            background-size: cover;
        }
        div.logo {
            margin-top: 150px;
            text-align: center;
        }
        div.text_center {
            margin-top: 50px;
            text-align: center;
        }
        div.input_style {
            margin-top: 150px;
            text-align: center;
        }
        input.input_size {
            width: 1000px;
            height: 25px;
        }
        ul#nav {
            width: 100%;
            height: 60px;
            background: #00A2CA;
            margin: 0 auto;
        }
        ul#nav li {
            display: inline;
            height: 60px;
            float: right;
        }
        ul#nav li a {
            display: inline-block;
            padding: 0 20px;
            height: 60px;
            line-height: 60px;
            color: #FFF;
            font-size: 16px;
        }
        ul#nav li a: hover{background: #0095BB;}
        ul#nav li label {
            display: inline;
            padding: 0 20px;
            height: 60px;
            line-height: 60px;
            color: #FFF;
            font-size: 16px;
        }
    </style>
</head>

<body>
    <?php
    if(!isset($_SESSION["name"])) {?>
        <ul id="nav">
        <li><a href="register.html">注册</a></li>
        <li><a href="login.html">登录</a></li>
        <li><a href="image_search.html">以图搜图</a></li>
        <li><a href="homepage2.php">按访问量排序搜索</a></li>
        </ul>
        <?php
    }
    else {?>
        <ul id="nav">
        <li><label><?php echo $_SESSION["name"]; ?></label></li>
        <li><a href="logout.php">注销</a></li>
        <li><a href="image_search.html">以图搜图</a></li>
        <li><a href="homepage2.php">按访问量排序搜索</a></li>
        <li><a href="recommendation.php">猜你喜欢</a></li>
        
        </ul>
        <?php
    }
    ?>
    <div class="logo">
        <h1>图样</h1>
    </div>
    <div class="input_style">
        <form action="search_by_text.php" method="GET">
            <input class="input_size" maxlength="255" autocomplete="off" type="text" name="content" required placeholder="请输入检索内容"></input>
            <input type=submit value="搜索">
        </form>
    </div>
</body>
</html>
