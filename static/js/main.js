$(function(){
    $(".tab_area li").click(function(){
        // パネル部分の取得
        var tabbody = $(".panel_area li")
        // 選択されたタブのインデックスを取得
        var idx = $(this).index()
        // タブの遷移処理
        $(this).removeClass("active").eq(idx).addClass("active")
        tabbody.removeClass("active").eq(idx).addClass("active")
    })


    $(".modal_open").click(function(){
        // モーダルウィンドウの黒背景のタグ挿入
        $("body").append('<div class="modal_bg"></div>')
        // 画面中央を算出
        modalResize()

        // モーダルウィンドウ出現
        $(".modal_bg, .modal_window").fadeIn("slow")
        // 閉じる処理
        $(".modal_bg").click(function(){
            $(".modal_bg, .modal_window").fadeOut("slow", function(){
                // 挿入したタグも一緒に消す
                $(".modal_bg").remove()
            })
        })


        // 画面中央を算出する処理
        $(window).resize(modalResize)
        function modalResize(){
            var w = $(window).width()
            var h = $(window).height()
            var modalW = $(".modal_window").outerWidth()
            var modalH = $(".modal_window").outerHeight()

            $(".modal_window").css({
                "left": ((w-modalW)/2) + "px",
                "top": ((h-modalH)/2) + "px"
            })
        }
    })


    $("input[name=category]:radio").change(function(){
        // 選択されたパラメータを取得
        var param = $(this).val()
        // URIの更新
        var btn = $(".startBtn")
        var href = btn.attr("href")
        href = href.split("=")[0] + "=" + param
        btn.attr("href", href)
    })


    $(".startBtn").click(function(){
        var href = $(this).attr("href")
        // パラメータcategoryのみ前提でその値を取得
        var param = href.split("=")[1]
        if(param==""){
            return false
        }
        return true
    })
})