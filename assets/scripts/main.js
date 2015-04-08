(function () {
   'use strict';

    function setCarouselHeight(id) {
        var slideHeight = [];
        var max;

        $(id+' .item').each(function() {
            // add all slide heights to an array
            slideHeight.push($(this).height());
        });

        // find the tallest item
        max = Math.max.apply(null, slideHeight);

        // set the slide's height
        $(id+' .carousel-content').each(function() {
            $(this).css('height',max+'px');
        });
    }

    $(function () {
        var frm = $('#mailing');
        frm.submit(function () {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function (data) {
                    console.log(data);
                    if (data.success) {
                        $('.subscribe-form').hide();
                        $('.subscribe-success').show();
                        console.log('vai');
                    }
                },
                error: function(data) {
                    console.log(data);
                }
            });
            return false;
        });

        setCarouselHeight('#carousel-who-used');
    });

})();
