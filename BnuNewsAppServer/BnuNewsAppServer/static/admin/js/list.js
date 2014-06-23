$(function(){
    if ( ! $.cookie('name') ) {
        location.href='login.html';
    }

    var app = $.sammy("#main", function () {
        this.use(Sammy.EJS);

        this.get('#:pg', function () {
            var pg = parseInt(this.params['pg']),
                sn = 0,
                nu = 10;
            if ( pg > 0 ) {
                sn = 0 + (pg - 1)*nu;
                this.load('/appserver/admin/news/list_news?start=' + sn + '&k=' + nu, {json:true})
                    .then(function (data) {
                        this.partial('tpl/list.ejs', {data: data, sn: sn, pn: Math.ceil(data.count / nu), pg: pg },function(){
                            $('.btn-toggle').click(function(){
                                $(this).button('toggle');
                            })
                        });
                    });
            } else {
                this.redirect('#1');
            }
        });

        this.notFound = function (context) {
            this.runRoute('get', '#1');
        }
    });

    app.run('#1');
});