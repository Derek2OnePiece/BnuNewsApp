$(function(){
    if ($.cookie('name')) {
        location.href='index.html';
    }

    $('#form-submit').click(function(event){
        event.stopPropagation();
        event.preventDefault();
        var name = $('#form-name').val(),
            pwd = $('#form-pwd').val(),
            check = $('#form-check').is(':checked');

        if (name && pwd) {
            $.ajax({
                type: 'POST',
                url: '/appserver/admin/user/login',
                data: {email:name, password:pwd},
                dataType: 'json',
                success: function(data){
                            if(data['code']==0) {
                                if (check) {
                                    $.cookie('name', name);
                                } else {
                                    $.cookie('name', name, { expires: 365 });
                                }
                                location.href='index.html';
                            } else {
                                alert('用户名或密码错误');
                            }
                        }
            });

        } else {
            alert('请填写用户名和密码');
        }

    });
});