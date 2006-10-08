<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title py:content="use_case">Use Case</title>
</head>

<body>
    <h4><a py:content="next_text" py:attrs="href=std.url('/'+next_url)">Proximo Passo</a></h4>

    <p py:content="form(submit_text='Confirma')">Use Case form</p>

</body>
</html>
