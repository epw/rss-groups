/*
function on_google_sign_in(auth_result) {
    console.log("on_google_sign_in");
    console.log(auth_result);
    if (!auth_result["code"]) {
	console.error(["Error with auth_result", auth_result]);
	return;
    }
    $("#googlesignin").text("Signed in");
    $.ajax({
	type: "POST",
	url: "https://eric.willisson.org/rss-groups/google-login.cgi",
	headers: {
	    "X-Requested-With": "XMLHttpRequest",
	},
//	contentType: "application/octet-stream; charset=utf-8",
	contentType: "application/x-www-form-urlencoded; charset=utf-8",
	success: function(result, status) {
	    console.log(["Got blog: ", result]);
	    console.log(["Status", status]);
	},
	error: function(request, status, err) {
	    console.error("Error");
	    console.error(["request", request]);
	    console.error(["status", status]);
	    console.error(["err", err]);
	},
	processData: true,
	data: {idtoken: auth_result["code"],
	       id: document.forms[0].elements.id.value,
	       auth: document.forms[0].elements.auth.value,
	       url: document.forms[0].elements.rss.value},
    });
}

function old_sign_in(googleUser) {

    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();

    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://eric.willisson.org/rss-groups/google-login.cgi');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
       xhr.onload = function() {
	 console.log('Signed in for blog: ' + xhr.responseText);
       };
    xhr.send('idtoken=' + id_token + "&id=" + document.forms[0].elements.id.value
	     + "&auth=" + document.forms[0].elements.auth.value
	     + "&url=" + document.forms[0].elements.rss.value);
}
*/

function hide_instructions() {
    document.querySelector(".authentication .wordpress").setAttribute("style", "display: none");
    document.querySelector(".authentication .google").setAttribute("style", "display: none");
}

function show_instruction(class_name) {
    console.log(document.querySelector(".authentication ." + class_name));
    document.querySelector(".authentication ." + class_name).setAttribute("style", "display: block");
}

function type_changed() {
    console.log("type_changed");
    hide_instructions();
    var type = document.querySelector("#type").value;
    console.log(type);
    switch(type) {
    case "wordpress":
	show_instruction("wordpress");
	break;
    case "blogger":
	show_instruction("google");
	break;
    default:
	break;
    }
}

function copy_to_clipboard(str) {
    const el = document.createElement('textarea');

    el.value = str;
    el.setAttribute("style", "display: none");
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}

function copywpwebhook() {
    console.log("Copy");
    copy_to_clipboard(document.querySelector("#wpwebhook").value);
    return false;
}

function init() {
    document.forms[0].elements.type.value = document.forms[0].elements.blogtypehidden.value;

    document.querySelector("#type").onchange = type_changed;
    type_changed();

    document.querySelector("#copywpwebhookbutton").addEventListener("click", copywpwebhook);
    
    /*
    gapi.load("auth2", function() {
	auth2 = gapi.auth2.init({
	    client_id: "145363362327-tsvcsck1stldh89po1b1n68haehccc5h.apps.googleusercontent.com",
	    scope: "profile email https://www.googleapis.com/auth/blogger"
	});
    });
    $("#googlesignin").click(function() {
	auth2.grantOfflineAccess().then(on_google_sign_in);
	return false;
    });
    */
}

init();
