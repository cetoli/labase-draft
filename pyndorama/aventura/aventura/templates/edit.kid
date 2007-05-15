<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Bem-vindo ao Pyndorama!</title>
</head>

<body>
  <div id="book">
         
        <APPLET CODE="freemind.main.FreeMindApplet.class" ARCHIVE="static/freemindbrowser.jar" WIDTH="100%" HEIGHT="80%">
	<PARAM NAME="type" VALUE="application/x-java-applet;version=1.4"/>
	<PARAM NAME="scriptable" VALUE="false"/>
	<PARAM NAME="toolbarVisible" VALUE="true"/>
	
	<PARAM NAME="modes" VALUE="freemind.modes.browsemode.BrowseMode"/>
	<PARAM NAME="browsemode_initial_map" VALUE="http://localhost:8080/static/ave.mm"/>
	
	<param NAME="initial_mode" VALUE="Browse"/>
	<param NAME="selection_method" VALUE="selection_method_direct"/>
	</APPLET>
        
  </div>
</body>
</html>
