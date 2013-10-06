$(document).ready(function() {

    $(".menu").click(function (event) {
        event.preventDefault();

        $('.active').removeClass('active');
        $(event.target).parent().addClass('active')

        var old_displayed = $('.displayed');
        old_displayed.removeClass('displayed');
        old_displayed.addClass('not_displayed');

        var id = '#'+$(event.target).text().toLowerCase();
        var displayed = $(id);

        displayed.removeClass('not_displayed');
        displayed.addClass('displayed');

        var href = $(event.target).attr('href');

        $.ajax({
            url: href,
            success: function(data, status, xhr){
            // append the response data in the HTML
                $(id).empty();
                $(id).append(data);
            }
        });

    });

})