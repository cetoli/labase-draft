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
        #item {
	float: left;
	padding: 2px 2% 2px 2%;
	margin: 2px 1% 2px 2%;
	background: #ccc;
	border: 1px solid #eee;
	width: 10%; /* ie5win fudge begins */
	voice-family: "\"}\"";
	voice-family:inherit;
	width: 10%;
	}
    #menuer {
	float: left;
	padding: 1px 2% 1px 2%;
	margin: 2px 0px 2px 1%;
	background: #aaa;
	border: 1px solid #ccc;
	width: 70%; /* ie5win fudge begins */
	voice-family: "\"}\"";
	voice-family:inherit;
	width: 70%;
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

    <div py:if="value_of('tg_flash',False)" class="flash" py:content="tg_flash"></div>
    <div id="menuer"> 
      <div py:for="link,menu in tg.main_menu()"> <a href='${link}' id="item" py:content="menu"/></div>
    </div>
    <br/>

    <div py:replace="[item.text]+item[:]"/>

    <p align="center"><img src="/static/images/tg_under_the_hood.png" alt="TurboGears under the hood"/></p>
</body>

</html>
