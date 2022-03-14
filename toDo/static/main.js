function toggleDiv(divId) {
    $('#' + divId).toggle();
}

function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
    $('#navContent').load(location.href + ' #navContent');
}

function taskCreate() {
    $.post('task_create', {
        content : $('#taskContent').val()
    }, function(data) {
        refreshPage();
    });
}

function subtaskCreate(taskId) {
    $.post('subtask_create', {
        id_: taskId,
        content : $('#subtaskFor' + taskId).val()
    }, function(data) {
        refreshPage();
    });
}

function taskUpdate(taskId, event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        $.post('task_update', {
            id_ : taskId,
            content : $('#taskContent' + taskId).html()
        }, function(data) {
            refreshPage();
        });
    }
}

function taskDelete(taskId) {
    $.get('task_delete', {
        id_ : taskId
    }, function(data) {
        refreshPage();
    });
}

function userEdit() {
    $.post('user_edit', {
        username : $('#username').val()
    }, function(data) {
        refreshPage();
    });
}

function changePassword() {
    $.post('change_password', {
        old_password : $('#oldPassword').val(),
        new_password1 : $('#newPassword1').val(),
        new_password2 : $('#newPassword2').val()
    }, function(data) {
        refreshPage();
    });
}

function taskToggle(taskId) {
    $.get('task_toggle', {
        id_ : taskId
    }, function(data) {
        refreshPage();
    });
}

function taskPin(taskId) {
    $.get('task_pin', {
        id_ : taskId
    }, function(data) {
        refreshPage();
    });
}