$(function () {
    if (!$.cookie('name')) {
        location.href = 'login.html';
    }

    var newsTypeList = {0:'图文',1:'视频'},
        moduleList = {1:'资讯',2:'教学',3:'学术',4:'课堂',5:'互动'},
        pCallback = function () {
            var file;

            $('#news_file').change(function(event){
                file = event.target.files[0];
            });

            $('input:text, textarea').click(function(){
                $(this).select();
            });

            $('.news_type').click(function(){
                var news_type_id = $(this).attr('data-newstypeid');
                $('#news_type').text(newsTypeList[news_type_id]).attr('data-newstypeid',news_type_id);
                if (news_type_id == 1) {
                    $('#news_video').parent().show();
                }else{
                    $('#news_video').parent().hide();
                }
            });

            $('.news_module').click(function(){
                var module_id = $(this).attr('data-moduleid');
                $('#news_module').text(moduleList[module_id]).attr('data-moduleid',module_id);
            });

            $('#news_submit').click(function(){
                var data = {
                    news_type: $('#news_type').attr('data-newstypeid'),
                    title: $('#news_title').val(),
                    abstract: $('#news_abstract').val(),
                    author: $('#news_author').val(),
                    module:$('#news_module').attr('data-moduleid'),
                    body: $('#news_body').val(),
                    inner_pic: file
                    },
                    form = new FormData(),
                    i;

                if (data['news_type'] == '1') {
                    data['video_target_url'] = $('#news_video').val();
                }

                for (i in data) {
                    form.append(i, data[i]);
                }

                $.ajax({
                    url: '/appserver/admin/news/add_news',
                    type: 'POST',
                    data: form,
                    cache: false,
                    dataType: 'json',
                    processData: false,
                    contentType: false,
                    success: function(data){
                        if (data['news_id']) {
                            alert('提交成功');
                            location.href = 'detail.html#'+data['news_id'];
                        } else {
                            alert('提交失败，请检查参数');
                        }
                    },
                    error: function(){
                        alert('提交失败，请检查参数');
                    }
                });
            });
        },

        app = $.sammy("#main", function () {
            this.use(Sammy.EJS);

            this.get('#:id', function () {
                var id = this.params['id'];
                var self =this;

                $.ajax({
                    url: '/appserver/admin/news/get_news_detail',
                    data: {news_id: id},
                    dataType: 'json',
                    type: 'get',
                    success: function(data) {
                        if (data['code'] === 0) {
                            self.partial('tpl/detail.ejs',
                                {data:data,edit:false,newsTypeList:newsTypeList,moduleList:moduleList},
                                function(){
                                    $('input:text, textarea').click(function(){
                                        $(this).select();
                                    });
                                }
                            );
                        } else {
                            self.redirect('#');
                        }
                    },
                    error: function(){
                        self.redirect('#');
                    }
                });

            });

            this.get('#', function () {
                this.partial('tpl/detail.ejs',
                    {data:{
                        title: '请输入标题',
                        abstract: '请输入摘要',
                        author: '请输入作者',
                        module:1,
                        news_type: 0,
                        body: '请输入正文'
                    },edit:true,newsTypeList:newsTypeList,moduleList:moduleList},
                    pCallback);
            });

            this.notFound = function (context) {
                this.runRoute('get', '#');
            };
    });

    app.run('#');
});