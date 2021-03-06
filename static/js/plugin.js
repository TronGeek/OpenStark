$(document).ready(function(){
    //保存配置
    $(".submit").click(function(){
        var act = $(this).attr('data-act'),
            $form = $("form."+act),
            url = $form.attr("action"),
            password = $("#password").val();
        $("#msg").addClass('sr-only');
        $("#password-enc").val(RSAUtils.pwdEncode(password));
        $.post(url, $form.serialize(), function(data){
            $("#msg").html(data.msg).removeClass('sr-only');
            if(data.result){
                $("#test-logs").addClass('sr-only');
            }
        }).error(function(data){
            if(data.status == 403){
                $("#tips-error #tips-error-msg").html("登录超时, 请重新登录!");
                $("#tips-error").modal();
                return
            }
        });
        //显示系统日志
        $('#test-logs').html("").removeClass('sr-only');
        var ws = $.websocket('ws://' + location.host + '/admin/websocket/weblogs', {
            open: function(){
                this.send('message', 'get_logs');
            },
            close: function(){
                $('#test-logs').append('WebSocket closed<br>');
                this.close();
            },
            events: {
                message: function(e){
                    for(i in e.data){
                        $('#test-logs').append(e.data[i] + '<br>');
                        var scrollTop = document.body.scrollHeight + $('#test-logs').scrollTop();
                        $('#test-logs').scrollTop(scrollTop);
                        if(scrollTop > 10800){
                            $('#test-logs').html("");
                        }
                    }
                }
            },
            error: function(){
                $('#test-logs').html('Connection WebSocket service error<br>');
                this.close();
            }
        });
    });
    //切换tab清除tips
    $('li>a[role="tab"]').click(function(){
        $("#msg").addClass('sr-only');
        $("#test-logs").addClass('sr-only');
    });
});