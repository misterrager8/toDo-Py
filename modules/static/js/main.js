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

function expandCard(elem, id) {
    $('#' + id).fadeToggle();
    if ($('#' + id).css('display') == 'none') {
        $(elem).parent().parent().parent().css('z-index', 1);
    } else {
        $(elem).parent().parent().parent().css('z-index', 2);
    }
}

function checkBox(elem, id) {
    if ($(elem).is(':checked')) {
        $('#' + id).show();
    } else {
        $('#' + id).hide();
    }
}