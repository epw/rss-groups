function make_body(group_id, name, rss, blog_type) {
    return "group_id=" + group_id + "&name=" + encodeURIComponent(name) + "&rss=" + encodeURIComponent(rss) + "&type=" + encodeURIComponent(blog_type);
}

function handle_response(response) {
    response.json().then(json => {
	if ("error" in json) {
	    console.error(json.error);
	} else {
	    location.reload();
	}
    });
}

function detect_blog_type(url) {
    if (url.indexOf("blogspot.com") != -1) {
	return "blogger";
    } else if (url.indexOf("wordpress.com") != -1) {
	return "wordpress";
    }
    return "rss";
}

function add_member() {
    const name = prompt("Name of the new member");
    if (name == null) {
	return;
    }
    const rss = prompt("New member's RSS feed");
    if (rss == null) {
	return;
    }
    let blog_type = detect_blog_type(rss);
    const type_correct = confirm("Is detected blog type " + blog_type + " correct?");
    if (!type_correct) {
	blog_type = prompt("Blog type ('rss', 'wordpress', or 'blogger')");
    }
    const urlparams = new URLSearchParams(window.location.search);
    console.log(make_body(urlparams.get("id"), name, rss, blog_type));
    fetch("add-member.cgi", {
	method: "POST",
	credentials: "same-origin",
	headers: {
	    "Content-Type": "application/x-www-form-urlencoded",
	},
	body: make_body(urlparams.get("id"), name, rss, blog_type),
    }).then(handle_response)
	.catch(response => console.error(response));
}

function checkbox_bool(selector) {
    if (document.querySelector(selector).checked) {
	return "1";
    }
    return "";
}

function show_hide_public_url() {
    if (document.getElementById("public").checked) {
	document.querySelector(".publicurl").setAttribute("style", "display: block");
    } else {
	document.querySelector(".publicurl").setAttribute("style", "display: none");
    }
}

function change_public() {	
    show_hide_public_url();
    const urlparams = new URLSearchParams(window.location.search);
    fetch("change-public.cgi", {
	method: "POST",
	credentials: "same-origin",
	headers: {
	    "Content-Type": "application/x-www-form-urlencoded",
	},
	body: "group_id=" + urlparams.get("id") + "&public=" + checkbox_bool("#public"),
    }).then(response => {
	response.json().then(s => console.log(s));
    }).catch(response => console.error(response));
    
}

function save_desc() {
    const urlparams = new URLSearchParams(window.location.search);
    fetch("change-desc.cgi", {
	method: "POST",
	credentials: "same-origin",
	headers: {
	    "Content-Type": "application/x-www-form-urlencoded",
	},
	body: "group_id=" + urlparams.get("id") + "&description=" + encodeURIComponent(document.getElementById("description").value),
    }).then(response => {
	response.json().then(s => console.log(s));
    }).catch(response => console.error(response));
}

function init() {
    document.getElementById("addmember").addEventListener("click",
							   add_member);
    document.getElementById("public").onchange = change_public;
    show_hide_public_url();

    document.getElementById("savedesc").onclick = save_desc;
}

init();
