function getCookie(Name) {
	var search = Name + "=" 
	if (document.cookie.length > 0) { // if there are any cookies
		offset = document.cookie.indexOf(search)
		if (offset != -1) { // if cookie exists 
			offset += search.length
			// set index of beginning of value
			end = document.cookie.indexOf(";", offset)
			// set index of end of cookie value
			if (end == -1)
				end = document.cookie.length
			return unescape(document.cookie.substring(offset, end))
		}
	}
}
function freqCapExpired(time) {
	//Time defined in hours

	expireDate = new Date();
	expireDate.setHours(expireDate.getHours() + time);
	//expireDate.setMinutes(expireDate.getMinutes() + time);
	dateNow = new Date();
	cookieExpire = getCookie('feqCap')

	if (cookieExpire) {
		cookieExpire = new Date(cookieExpire);
		if (cookieExpire <= dateNow){
			document.cookie = 'feqCap='+ expireDate +';expire='+ expireDate.toGMTString();
			return true;
		} else {
			return false;
		}
	} else {
		document.cookie = 'feqCap='+ expireDate +';expire='+ expireDate.toGMTString();
		return true;
	}
}


//Verifica se deve ser exibido
var expired = freqCapExpired(4)

if (expired){
	var popupUnder = window.open("http://www.cidade.com","cidade",'top=10,left=10,toolbar=no,location=no,status=no,menubar=no,directories=no,scrollbars=yes,resizable=yes,width=800,height=600');
	//var popupUnder = window.open("http://st.br.uigc.net/ubbi/hp/ubbidownloads.html","downloads",'top=10,left=10,toolbar=no,location=no,status=no,menubar=no,directories=no,scrollbars=no,resizable=no,width=503,height=387');
	//popupUnder.blur();
	//self.focus();

	//Publicidade de DigitalVentures veiculada em 11/04/2006
	//document.write("<SCRIPT TYPE='text/javascript' SRC='http://ad.directanetworks.com/imp?z=0&s=26302&y=29'></SCRIPT>");

}
