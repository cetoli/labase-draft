<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Bem-vindo ao Pyndorama!</title>
</head>

<body>
    <form action="acao" method="POST">
         <PRE>
          ${text}
         </PRE>
        <input type="text" name="query" value=""/>
        <input type="submit" value="Ação!!!"/>        
    </form>
    <img src='${image}'/>     
</body>
</html>
