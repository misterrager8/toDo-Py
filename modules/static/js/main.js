function addInput(elem) {
    var nput = elem.previousElementSibling.cloneNode();
    elem.parentNode.insertBefore(nput, elem);
}