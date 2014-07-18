$(function () {
    if (!$.cookie('name')) {
        location.href = 'login.html';
    }

    var app = $.sammy("#main", function () {
        this.use(Sammy.EJS);

        this.get('#', function () {
            this.load('/appserver/admin/user/get_user_summary', {json: true})
                .then(function (data) {
                    this.partial('tpl/user.ejs', {data: data});
                });
        });

        this.notFound = function (context) {
            this.runRoute('get', '#');
        }
    });

    app.run('#');
});