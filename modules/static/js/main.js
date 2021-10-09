function addInput(elem) {
    var nput = elem.previousElementSibling.cloneNode();
    elem.parentNode.insertBefore(nput, elem);
}

function changeTheme() {
    if (document.getElementById("site-content").classList.contains("other-theme")) {
        document.getElementById("site-content").classList.remove("other-theme");
    } else {
        document.getElementById("site-content").classList.add("other-theme");
    }
}