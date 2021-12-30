function changeTheme() {
    if (document.getElementById("site-content").classList.contains("other-theme")) {
        document.getElementById("site-content").classList.remove("other-theme");
    } else {
        document.getElementById("site-content").classList.add("other-theme");
    }
}

function expandDiv(parentId, divId) {
    $('#' + divId).fadeToggle();
}

function checkBox(elem, id) {
    if ($('#' + elem).is(':checked')) {
        $('#' + id).show();
    } else {
        $('#' + id).hide();
    }
}

$('#sessionCreate').on('submit', function(event) {
    $.post('/session_create', { start_time : $('#startTime').val(), stop_time : $('#stopTime').val() }, function(data) { $('#allSessions').load(location.href + ' #allSessions'); });
    event.preventDefault();
});

$('#taskCreate').on('submit', function(event) {
    $.post('/task_create',
    { name : $('#taskName').val(), folder : $('#taskFolder').val() },
    function(data) {
        $('#allTasks').load(location.href + ' #allTasks');
    });
    $('#taskName').val('');
    event.preventDefault();
});

$('#folderCreate').on('submit', function(event) {
    $.post('/folder_create',
    { name : $('#folderName').val() },
    function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
    $('#folderName').val('');
    event.preventDefault();
});

function taskEdit(taskId) {
    $.post('task_edit', {
        id_ : taskId,
        name : $('#name' + taskId).val(),
        note : $('#note' + taskId).val()
    }, function(data) {
        $('#taskContent').load(location.href + ' #taskContent');
    });
}

function taskToggle(taskId) {
    $.get('task_toggle', {
        id_: taskId
    }, function(data) {
        $('#allTasks').load(location.href + ' #allTasks');
    });
}

function taskDelete(taskId) {
    $.get('task_delete', { id_: taskId }, function(data) { $('#allTasks').load(location.href + ' #allTasks'); });
}

function folderDelete(folderId) {
    $.get('folder_delete', { id_: folderId }, function(data) { $('#allFolders').load(location.href + ' #allFolders'); });
}