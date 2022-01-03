function changeTheme() {
    $('.btn-custom, .badge-custom, .navbar, body').addClass('other-theme');
}

function toggleDiv(divId) {
    $('#' + divId).toggle();
}

function refreshDiv(divId) {
    $('#' + divId).load(location.href + ' #' + divId);
}

function changeType() {
    if ($('#type_').val() == 'Event') {
        $('#eventDate').show();
    } else {
        $('#eventDate').hide();
    }
}

function styleText(style, val) {
    document.execCommand(style, false, val);
}

function bulletCreate() {
    $.post('bullet_create', {
        type_ : $('#type_').val(),
        content : $('#content').html()
    }, function(data) {
        $('#content').html('')
        refreshDiv('tiles');
    });
}

function bulletEdit(bulletId) {
    $('#saveSpinner').show();
    $.post('editor', {
        id_ : bulletId,
        content : $('#content').html()
    }, function(data) {
        $('#saveSpinner').hide();
    });
}

function userEdit() {
    $.post('user_edit', {
        first_name : $('#firstName').val(),
        last_name : $('#lastName').val(),
        email : $('#email').val()
    });
}

function bulletDelete(bulletId) {
    $.get('bullet_delete', {
        id_ : bulletId
    }, function(data) {
        refreshDiv('tiles');
    });
}

function taskToggle(bulletId) {
    $.get('task_toggle', {
        id_ : bulletId
    }, function(data) {
        refreshDiv('tiles');
    });
}

function pinToggle(bulletId) {
    $.get('pin_toggle', {
        id_ : bulletId
    }, function(data) {
        refreshDiv('tiles');
    });
}