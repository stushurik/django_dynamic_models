$(document).ready(function() {
    $(".btn").click(function(event) {
        event.preventDefault();

        var form = $(event.target).parent().parent();

        var id = '#'+$(event.target).parent().attr('id');

        var url =form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function(data){
                $(id).empty();
                $(id).append(data);
                $('.dp').datepicker();
            }
         });

    });
})