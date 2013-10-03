$(document).ready(function() {

    $(".menu").click(function (event) {
        $('.active').removeClass('active');
        $(event.target).parent().addClass('active')
//        $('#'+$(event.target).)

        var old_displayed = $('.displayed');
        old_displayed.removeClass('displayed');
        old_displayed.addClass('not_displayed');

        var id = '#'+$(event.target).text().toLowerCase();
        var displayed = $(id);

        displayed.removeClass('not_displayed');
        displayed.addClass('displayed');



    });

})