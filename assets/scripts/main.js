(function () {
   'use strict';

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

        $(':input[data-bind-to]').each(function(evt){
            var $self = $(this);
            var $target = $($self.attr('data-bind-to'));

            $target.on('keyup paste', function(evt1){
                $self.val($target.val());
            });
        });

        $(':input[data-composed-bind]').each(function(evt){
            var $self = $(this);
            var $targets = $($self.attr('data-composed-bind'));

            var format = $self.attr('data-composed-format');
            if(format){
                $targets.on('change paste', function(evt1){
                    var values = $targets.map(function(){ return $(this).val(); });
                    try {
                        $self.val(vsprintf(format, values));
                    } catch(e) { }
                });
                return;
            }

            var bitoptions = $self.attr('data-composed-bitoptions');
            if(bitoptions) {
                $targets.on('change', function(evt1){
                    var value = 0;
                    $targets.each(function(i,e){
                        var checked = e.checked || $(e).is(':checked');
                        var integer = parseInt(e.value, 10);
                        if(checked) {
                            value = value | integer;
                        }
                    });
                    $self.val(value);
                });
            }

        });

    });
    
})();
