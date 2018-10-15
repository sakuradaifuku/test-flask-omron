(function($) {

$(function() {
    MovieCentering.init();
});

var MovieCentering = {
    init: function(){
        $(window).on('load', function(){
            MovieCentering .resize();
        });

        $(window).on('resize', function(){
            MovieCentering .resize();
        });
    }

    ,resize: function(){
        var windowSizeHeight = $('window').outerHeight()
        ,windowSizeWidth = $('window').outerWidth();

        var windowMovieSizeWidth = $('.BackVideo').outerWidth()
        ,windowMovieSizeHeight = $('.BackVideo').outerHeight();

        if (windowSizeWidth < windowMovieSizeWidth) {
            var windowMovieSizeWidthLeftMargin = (windowMovieSizeWidth - windowSizeWidth) / 2;
            $('.BackVideo').css({left: -windowMovieSizeWidthLeftMargin});
        }else{
            $('.BackVideo').css({left: 0});
        }

        if (windowSizeWidth < windowMovieSizeWidth) {
            var windowMovieSizeWidthLeftMargin = (windowMovieSizeWidth - windowSizeWidth) / 2;
            $('.BackVideo').css({left: -windowMovieSizeWidthLeftMargin});
        }else{
            $('.BackVideo').css({left: 0});
        }
    }
}
})(jQuery);
