function changeTheme() {
    $('.btn-custom, .badge-custom, .navbar').addClass('other-theme');
}

function toggleDiv(divId) {
    $('#' + divId).toggle(250);
}

function taskCreate(folderId) {
    $.post('task_create', {
        id_: folderId,
        name : $('#taskName').val()
    }, function(data) {
        $('#allTasks').load(location.href + ' #allTasks');
    });
}

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
    $.get('task_delete', {
        id_: taskId
    }, function(data) {
        $('#allTasks').load(location.href + ' #allTasks');
    });
}

function folderCreate() {
    $.post('folder_create', {
        name : $('#folderName').val()
    }, function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
}

function folderEdit(folderId) {
    $.post('folder_edit', {
        id_ : folderId,
        name : $('#folderName' + folderId).val(),
        color : $('#color' + folderId).val()
    }, function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
}

function folderDelete(folderId) {
    $.get('folder_delete', {
        id_: folderId
    }, function(data) {
        $('#allFolders').load(location.href + ' #allFolders');
    });
}