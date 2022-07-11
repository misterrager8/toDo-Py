$(document).ready(function() {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('todo_theme'));
});

function changeTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('todo_theme', theme);
}

function toggleDiv(divId) {
    $('#' + divId).fadeToggle(250);
}

function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
}

function createTask() {
    $('#spinner').show();
    $.post('create_task', {
        description : $('#description').val(),
        list_id : $('#list_id').val()
    }, function(data) {
        refreshPage();
    });
}

function editTask(taskId) {
    $('#spinner').show();
    $.post('edit_task', {
        id_: taskId,
        description : $('#description' + taskId).val()
    }, function(data) {
        refreshPage();
    });
}

function toggleTask(taskId) {
    $('#spinner').show();
    $.get('toggle_task', {
        id_: taskId
    }, function(data) {
        refreshPage();
    });
}

function deleteTask(taskId) {
    $('#spinner').show();
    $.get('delete_task', {
        id_: taskId
    }, function(data) {
        refreshPage();
    });
}

function createList() {
    $('#spinner').show();
    $.post('create_list', {
        name : $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function editList(listId) {
    $('#spinner').show();
    $.post('edit_list', {
        id_: listId,
        name : $('#name' + listId).val()
    }, function(data) {
        refreshPage();
    });
}

function deleteList(listId) {
    $('#spinner').show();
    $.get('delete_list', {
        id_: listId
    }, function(data) {
        refreshPage();
    });
}

function copyToClipboard(taskId) {
    document.getElementById('description' + taskId).select();
    document.execCommand('copy');
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