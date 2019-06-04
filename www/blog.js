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
}

init();
