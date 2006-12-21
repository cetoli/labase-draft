<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>
    <style type="text/css">
        #pageLogin
        {
            font-size: 10px;
            font-family: verdana;
            text-align: right;
        }
        #book
        {
            background-image:url(/static/images/book.jpg);
	padding: 20px 2% 20px 2%;
	margin: 10px 150px 10px 10px;
	border: 3px solid #eee;
	width: 750px;
	height: 400px;
        }
        #fabletext {
        float:left;
              /* top right bottom left */
	padding: 50px 10px 10px 10px ;
	margin: 50px 0px 10px 50px ;
	border: 0px solid #eee;
	width: 300px;
	height: 200px;
	}
        #fableview {
        float:left;
	padding: 50px 10px 10px 10px ;
	margin: 50px 0px 10px 20px ;
	border: 0px solid #eee;
	width: 250px;
	height: 200px;
	}
        #fableaction {
        float:left;
        background-color:transparent;
	padding: 30px 10px 10px 90px ;
	margin: 10px 60px 10px 50px ;
	border: 0px solid #eee;
	height: 20px;
	}
    </style>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
    <div py:if="tg.config('identity.on',False) and not 'logging_in' in locals()"
        id="pageLogin">
        <span py:if="tg.identity.anonymous">
            <a href="/login">Login</a>
        </span>
        <span py:if="not tg.identity.anonymous">
            Welcome ${tg.identity.user.display_name}.
            <a href="/logout">Logout</a>
        </span>
    </div>

    <!--<div py:if="tg_flash" class="flash" py:content="tg_flash"></div> -->

    <div id="book" py:replace="[item.text]+item[:]"/>

    <p align="center"><img src="/static/images/labase.gif" alt="Labase"/></p>
</body>

</html>
