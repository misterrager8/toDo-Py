function toggleDiv(divId) {
    $('#' + divId).toggle();
}

function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
    $('#navContent').load(location.href + ' #navContent');
}

function taskCreate() {
    $('#spinner').show();
    $.post('task_create', {
        content : $('#taskContent').val()
    }, function(data) {
        refreshPage();
    });
}

function subtaskCreate(taskId) {
    $('#spinner').show();
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
        $('#spinner').show();
        $.post('task_update', {
            id_ : taskId,
            content : $('#taskContent' + taskId).html()
        }, function(data) {
            refreshPage();
        });
    }
}

function taskDelete(taskId) {
    $('#spinner').show();
    $.get('task_delete', {
        id_ : taskId
    }, function(data) {
        refreshPage();
    });
}

function userEdit() {
    $('#spinner').show();
    $.post('user_edit', {
        username : $('#username').val()
    }, function(data) {
        refreshPage();
    });
}

function changePassword() {
    $('#spinner').show();
    $.post('change_password', {
        old_password : $('#oldPassword').val(),
        new_password1 : $('#newPassword1').val(),
        new_password2 : $('#newPassword2').val()
    }, function(data) {
        refreshPage();
    });
}

function taskToggle(taskId) {
    $('#spinner').show();
    $.get('task_toggle', {
        id_ : taskId
    }, function(data) {
        refreshPage();
    });
}

function taskPin(taskId) {
    $('#spinner').show();
    $.get('task_pin', {
        id_ : taskId
    }, function(data) {
        refreshPage();
    });
}