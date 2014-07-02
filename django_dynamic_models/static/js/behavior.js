$(document).ready(function () {

    $(".menu").click(function (event) {
        event.preventDefault();

        if (!$(event.target).hasClass('menu')) {
            $('.active').removeClass('active');
            $(event.target).parent().addClass('active')

            var old_displayed = $('.displayed');
            old_displayed.removeClass('displayed');
            old_displayed.addClass('not_displayed');

            var model = $(event.target).text().toLowerCase();
            var id = '#' + model;
            var displayed = $(id);

            displayed.removeClass('not_displayed');
            displayed.addClass('displayed');

            var href = $(event.target).attr('href');

            $.ajax({
                url: href,
                success: function (data) {

                    var table_body = "";

                    var items = jsyaml.load(data);

                    var first_iteration = true;
                    var headers = "<tr>";
                    for (var i in items) {

                        var obj = items[i];
                        var row = "<tr id='" + obj.pk + "' class='" + obj.model + "'>";

                        for (key in obj.fields) {
                            row += "<td class='cell " + typeof obj.fields[key] + "' data-value='" + key + "'>" + obj.fields[key] + "</td>";

                            if (first_iteration) {
                                headers += "<th>" + key + "</th>";
                            }

                        }
                        first_iteration = false;
                        row += "</tr>";
                        headers += "</tr>";
                        table_body += row;
                    }

                    var table = '<table id="formset" class="form">' +
                        headers +
                        table_body +
                        '</table>';

                    $(id).empty();
                    $(id).append(table);
//                    $('.dp').datepicker();
                    $(".btn").hide();
                    $("." + model + "_submit").show();
                }
            });
        }

    });

});

$( document ).on( "click", "td.cell:not(:has(:input))", function() {

    var input;

    if ($(this).hasClass('string')) {
        input = $('<textarea>' + $(this).html() + '</textarea>');
    } else {
        if ($(this).hasClass('number')) {
            input = $('<input />', {'type': 'text', 'value': $(this).html()});
        } else {
            if ($(this).hasClass('boolean')) {
                input = $('<input />', {'type': 'checkbox', 'checked':  $(this).html() === "true" });
            } else {


                input = $('<div class="input-append date" id="dpYears" data-date="2012-12-02" data-date-format="yyyy-mm-dd" data-date-viewmode="years">' +
                '<input class="dp" type="text" value="' + $(this).html() + '">' +
                '</div>');


            }
        }
    }
    $(this).empty();
    $(this).append(input);
//    $(this).remove();
    input.focus();
    var td = $(this);
    $('.dp').datepicker().on('hide', function(ev){
        var val = ev.date;
        $('.dp').parent().remove();
        td.append(val);
    });
});

$( document ).on( "blur", ":input:not('.btn')", function(event) {
    var del = true;

    var element_for_remove = $(this);

    if ($(event.target).is(":checkbox")){
        $(this).parent().append(String($(event.target).is(':checked')));
    } else {
        if ($(event.target).hasClass('dp')){
            element_for_remove = $(this).parent();
            if ($('.datepicker').length > 0){
                del = false
            }
        }
        $(this).parent().append($(this).val());
    }

    if (del) {
        element_for_remove.remove();
    }
});

$( document ).on( "click", ".btn", function(event) {
        event.preventDefault();

        var form = $(event.target).parent();

        var url =form.attr('action');

        var yaml = []

        var obj = {
            fields: {},
            model: "",
            pk: ""
        };
        $('#formset th').each(function(k, header){
            obj.fields[$(header).text()] = ""
        });



        $('#formset tr:has(td)').each(function(i, row){

            var element = $.extend(true, {}, obj);

            var cells = $(row).find('td');


            cells.each(function(j, cell){

                var key = $(cell).attr('data-value');
                if ($(cell).hasClass('string')) {
                    element.fields[key] = $(cell).text();
                } else {
                    if ($(cell).hasClass('number')){
                        element.fields[key] = parseInt($(cell).text());
                    } else {
                        if ($(cell).hasClass('boolean')){
                            element.fields[key] = $(cell).text() === 'true';
                        } else {
                            element.fields[key] = new Date($(cell).text());
                        }
                    }
                }

            });

            element.pk = parseInt($(row).attr('id'));
            element.model = $(row).attr('class');

            yaml.push(element);
        });

        console.log(yaml);
        var yaml_data = jsyaml.dump(yaml);
        console.log(yaml_data);

        $.ajax({
            type: "POST",
            url: url,
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                value: yaml_data
            },
            success: function(data){
//                $(id).empty();
//                $(id).append(data);
//                $('.dp').datepicker();
            }
         });

});