<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Bem-vindo ao Pyndorama!</title>
</head>

<body>
  <div id="book">
         <PRE id="fabletext">
          ${text}
         </PRE>
         <img id="fableview" src='${image}'/>     
    <form action="acao" method="POST">
      <div id="fableaction">
        <input  type="text" name="query" value=""/>
        <input type="submit" value="Ação!!!"/>        
      </div>
    </form>
  </div>
</body>
</html>