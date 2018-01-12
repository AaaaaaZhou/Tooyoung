<?php session_start(); ?>

<head>
    <meta charset="UTF-8">
    <style type="text/css">
        div.imgItem {
            margin: 10px;
            padding: auto;
            border: 2px;
            background: #FFF;
            height: 300px;
            width: 300px;
            float: left;
            text-align: center:
            display: inline;
        }
        div.imgItem img {
            display: inline;
            margin: 30x;
            border: 1px solid #bebebe;
        }
        div.imgCaption {
            text-align:center ;
            font-weight: normal;
            width: 150px;
            font-size: 12px;
            margin:auto;
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
        ul#nav li input {
            display: inline;
            padding: 0 20px;
            height: 50px;
            line-height: 60px;
        }
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
$img = $_FILES['pics']['name'];
$url = $_FILES['pics']['tmp_name'];
$uploaded_path = dirname(__FILE__);
if(!is_uploaded_file($_FILES['pics']['tmp_name'])) {
    die("Invalid image");
}
move_uploaded_file($url, $uploaded_path."/".$img);
$new_img = $uploaded_path."/".$img;
$source = exec("/home/sunknight/miniconda2/bin/python
 python search_img_match.py ".$new_img." 2>&1", $arr, $ret);

if(!isset($_SESSION['name'])) {
    $res = explode(' ', $source);
    $lim = count($res) / 6; ?>

    <ul>
    <li>
        <form action="search_by_text.php" method="GET">
            <input name="content" required placeholder="请输入检索内容"></input>
            <input type=submit value="搜索">
        </form>
    </li>
    </ul>
    <ul id="nav">
    <li><a href="homepage.php">返回</a></li>
    <li><a href="image_search.html">以图搜图</a></li>
    <li><a href="homepage2.php">按访问量排序搜索</a></li>
    </ul>

<?php
    if($source == "") { ?>
        <h1>非常抱歉，没有搜索到相关信息</h1>
<?php
    }
    else {
        for($index = 0; $index < $lim; $index++) { ?>
            <div class="imgItem">
                <a href=<?php echo $res[$index*6+2] ?>>
                    <div align="center"><img src=<?php echo $res[$index*6+1] ?> alt=<?php echo $res[$index*6+5] ?>></div>
                </a>
                <div class="imgCaption">
                    <a href=<?php echo $res[$index*6+2] ?>><?php echo $res[$index*6+5] ?></a>
                </div>
            </div>
<?php
        }
    } ?>

<?php
}
else {?>

    <ul>
    <li>
        <form action="search_by_text.php" method="GET">
            <input name="content" required placeholder="请输入检索内容"></input>
            <input type=submit value="搜索">
        </form>
    </li>
    </ul>
    <ul id="nav">
    <li><label><?php echo $_SESSION["name"]; ?></label></li>
    <li><a href="homepage.php">返回</a></li>
    <li><a href="image_search.html">以图搜图</a></li>
    <li><a href="homepage2.php">按访问量排序搜索</a></li>
    <li><a href="recommendation.php">猜你喜欢</a></li>
    </ul>

<?php
    include("conn.php");
    $res = explode(' ', $source);
    $lim = count($res) / 6;
    if($source == "") { ?>
        <h1>非常抱歉，没有搜索到相关信息</h1>
<?php
    }
    else {
        for($index = 0; $index < $lim; $index++) { ?>
            <div class="imgItem">
                <a href=<?php echo $res[$index*6+2] ?>>
                    <div align="center"><img src=<?php echo $res[$index*6+1] ?> alt=<?php echo $res[$index*6+5] ?>></div>
                </a>
                <div class="imgCaption">
                    <a href=<?php echo $res[$index*6+2] ?>><?php echo $res[$index*6+5] ?></a>
                </div>
            </div>
<?php
        }
    }
}

$remove = exec("rm ".$new_img." 2>&1", $arr, $ret);

?>

</body>

