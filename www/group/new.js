function make_body(name) {
    return "name=" + encodeURIComponent(name);
}

function handle_response(response) {
//    response.text().then(text => document.getElementById("output").innerHTML = text);
    response.json().then(json => {
	if ("error" in json) {
	    console.error(json.error);
	} else {
	    location.search = "?id=" + json.success;
	}
    });
}

function add_group() {
    const name = prompt("Name of the new group");
    if (name == null) {
	return;
    }
    fetch("new-group.cgi", {
	method: "POST",
	credentials: "same-origin",
	headers: {
	    "Content-Type": "application/x-www-form-urlencoded",
	},
	body: make_body(name),
    }).then(handle_response)
	.catch(response => console.error(response));
}

function init() {
    document.getElementById("new").addEventListener("click",
						    add_group);
}

init();
