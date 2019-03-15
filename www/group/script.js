function add_member() {
    let name = prompt("Name of the new member");
    if (name == null) {
	return;
    }
    let email = prompt("New member's email address");
    if (email == null) {
	return;
    }
}

function init() {
    document.getElementById("addmember").addEventListener("click",
							  add_member);
}

init();
