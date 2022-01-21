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

function stepCreate(taskId) {
    $.post('step_create', {
        id_: taskId,
        content : $('#stepFor' + taskId).val()
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

function eventCreate() {
    $.post('event_create', {
        content : $('#eventContent').val(),
        event_date : $('#eventDate').val()
    }, function(data) {
        refreshPage();
    });
}

function eventUpdate(eventId) {
    $.post('event_update', {
        id_ : eventId,
        content : $('#eventContent' + eventId).val(),
        event_date : $('#eventDate' + eventId).val()
    }, function(data) {
        refreshPage();
    });
}

function eventDelete(eventId) {
    $.get('event_delete', {
        id_ : eventId
    }, function(data) {
        refreshPage();
    });
}

function noteCreate() {
    $.post('note_create', {
        content : $('#noteContent').val()
    }, function(data) {
        refreshPage();
    });
}

function noteUpdate(noteId) {
    $.post('note_update', {
        id_ : noteId,
        content : $('#noteContent' + noteId).val()
    }, function(data) {
        refreshPage();
    });
}

function noteDelete(noteId) {
    $.get('note_delete', {
        id_ : noteId
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

function eventPin(eventId) {
    $.get('event_pin', {
        id_ : eventId
    }, function(data) {
        refreshPage();
    });
}

function notePin(noteId) {
    $.get('note_pin', {
        id_ : noteId
    }, function(data) {
        refreshPage();
    });
}

function habitCreate() {
    $.post('habit_create', {
        description : $('#description').val()
    }, function(data) {
        refreshPage();
    });
}

function habitDelete(habitId) {
    $.get('habit_delete', {
        id_ : habitId
    }, function(data) {
        refreshPage();
    });
}

function entryCreate(habitId) {
    $.get('entry_create', {
        id_ : habitId
    }, function(data) {
        refreshPage();
    });
}