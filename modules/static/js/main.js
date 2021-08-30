function addInput() {
    var form_ = document.getElementById("form_");
    var input_ = document.getElementById("input_");

    form_.insertBefore(input_.cloneNode(true), document.getElementById("add_button"));
}

function addInput2() {
    var form_2 = document.getElementById("form_2");
    var input_2 = document.getElementById("input_2");

    form_2.insertBefore(input_2.cloneNode(true), document.getElementById("add_button_2"));
}