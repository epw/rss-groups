function make_body(group_id, name, rss) {
    return "group_id=" + group_id + "&name=" + encodeURIComponent(name) + "&rss=" + encodeURIComponent(rss);
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

function add_member() {
    const name = prompt("Name of the new member");
    if (name == null) {
	return;
    }
    const rss = prompt("New member's RSS feed");
    if (rss == null) {
	return;
    }
    const urlparams = new URLSearchParams(window.location.search);
    fetch("add-member.cgi", {
	method: "POST",
	credentials: "same-origin",
	headers: {
	    "Content-Type": "application/x-www-form-urlencoded",
	},
	body: make_body(urlparams.get("id"), name, rss),
    }).then(handle_response)
	.catch(response => console.error(response));
}

function init() {
    document.getElementById("addmember").addEventListener("click",
							  add_member);
}

init();
