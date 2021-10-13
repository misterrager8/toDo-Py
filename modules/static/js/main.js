function addInput(elem) {
    var nput = elem.previousElementSibling.cloneNode();
    nput.value = null;
    elem.parentNode.insertBefore(nput, elem);
    nput.focus();
}

function changeTheme() {
    if (document.getElementById("site-content").classList.contains("other-theme")) {
        document.getElementById("site-content").classList.remove("other-theme");
    } else {
        document.getElementById("site-content").classList.add("other-theme");
    }
}

function expandDiv(parentId, divId) {
    $('#' + divId).fadeToggle();
    if ($('#' + divId).css('display') == 'none') {
        $('#' + parentId).css('z-index', 1);
    } else {
        $('#' + parentId).css('z-index', 2);
    }
}

function checkBox(elem, id) {
    if ($(elem).is(':checked')) {
        $('#' + id).show();
    } else {
        $('#' + id).hide();
    }
}