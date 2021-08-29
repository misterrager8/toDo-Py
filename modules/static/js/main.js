function addInput() {
    var form_ = document.getElementById("form_");
    var input_ = document.getElementById("input_");

    form_.insertBefore(input_.cloneNode(true), document.getElementById("add_button"));
}