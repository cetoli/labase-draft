//pxver2.0 - using the mjx delivery engine
OAS_url = 'http://deliverparc.ads.uigc.net/RealMedia/ads/';
OAS_target = '_top';
OAS_version = 10;
OAS_rn = '001234567890'; OAS_rns = '1234567890';
OAS_rn = new String (Math.random()); OAS_rns = OAS_rn.substring (2, 11);
//Browser capability test
OAS_version = 11;
if (navigator.userAgent.indexOf('Mozilla/3') != -1 || navigator.userAgent.indexOf('Mozilla/4.0 WebTV') != -1)
  OAS_version = 10;
if (OAS_version >= 11)
  document.write('<SCRIPT LANGUAGE=JavaScript1.1 SRC="' + OAS_url + 'adstream_mjx.ads/' + OAS_sitepage + '/1' + OAS_rns + '@' + OAS_Page_Positions + '?' + OAS_query + '"></SCRIPT>');

function OAS_NORMAL(pos) {
  document.write('<A HREF="' + OAS_url + 'click_nx.ads/' + OAS_sitepage + '/1' + OAS_rns + '@' + OAS_Page_Positions + '!' + pos + '?' + OAS_query + '" TARGET=' + OAS_target + '>');
  document.write('<IMG SRC="' + OAS_url + 'adstream_nx.ads/' + OAS_sitepage + '/1' + OAS_rns + '@' + OAS_Page_Positions + '!' + pos + '?' + OAS_query + '" BORDER=0></A>');
}
document.write('');
function OAS_AD(pos, width, height) {
	try {
		if (OAS_version >= 11)
			OAS_RICH(pos);
		else
			OAS_NORMAL(pos);
	} catch(exception) {
	    document.write('<a href="http://www.ubbi.com.br/" target="_blank">\n');
	    document.write('<img src="http://static.br.uigc.net/oas/1x1.gif" border="0" width=1 height=1>\n');
	    document.write('</a>\n');
	}
}