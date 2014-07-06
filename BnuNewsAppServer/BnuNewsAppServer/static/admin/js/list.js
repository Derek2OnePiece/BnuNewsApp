$(function(){
    if ( ! $.cookie('name') ) {
        location.href='login.html';
    }

    var pCallback = function(){
            $('.btn-publish').click(function(){
                var pubStatus = $(this).hasClass('active'),
                    newsId = $(this).attr('data-newsid'),
                    btnText = pubStatus ? '发布' : '已发布',
                    self = this,
                    ajaxPara = {
                        data:{news_id:newsId},
                        dataType:'json',
                        type:'POST',
                        success: function(response){
                            if (response.code == 0) {
                                $(self).text(btnText);
                                $(self).button('toggle');
                            }
                        }
                    };
                if ( pubStatus ) {
                    ajaxPara['url'] = '/appserver/admin/news/cancel_pub_news';
                } else {
                    ajaxPara['url'] =  '/appserver/admin/news/pub_news';
                }
                $.ajax(ajaxPara);
            });

            $('.btn-delete').click(function(){
                var newsId = $(this).attr('data-newsid'),
                    self = $(this).parent().parent(),
                    ajaxPara = {
                        url:'/appserver/admin/news/delete_news',
                        data:{news_id:newsId},
                        dataType:'json',
                        type:'POST',
                        success: function(response){
                            if (response.code == 0) {
                                location.reload();
                            }
                        }
                    };
                $.ajax(ajaxPara);
            });

        },

        app = $.sammy("#main", function () {
            this.use(Sammy.EJS);

            this.get('#:pg', function () {
                var pg = parseInt(this.params['pg']),
                    sn = 0,
                    nu = 10;
                if ( pg > 0 ) {
                    sn = 0 + (pg - 1)*nu;
                    this.load('/appserver/admin/news/list_news?start=' + sn + '&k=' + nu, {json:true})
                        .then(function (data) {
                            this.partial('tpl/list.ejs', {data:data,sn:sn,pn:Math.ceil(data.count/nu),pg:pg}, pCallback);
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