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

function taskUpdate(taskId) {
    $('#spinner').show();
    $.post('task_update', {
        id_ : taskId,
        content : $('#taskContent' + taskId).val()
    }, function(data) {
        refreshPage();
        $('#spinner').hide();
    });
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