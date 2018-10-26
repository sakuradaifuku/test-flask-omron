$(function(){
    var tablist = $(".tab_area li")
    var tabbody = $(".panel_area li")

    tablist.click(function(){
        var idx = tablist.index($(this))
        tablist.removeClass("active").eq(idx).addClass("active")
        tabbody.removeClass("active").eq(idx).addClass("active")
    })
})