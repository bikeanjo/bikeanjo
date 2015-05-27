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

        $('[data-dismiss=card]').click(function(evt){
            $(this).parents('.card').hide();
        });

        $('.form-group .radio .icons,:input:visible').each(function(i) {
            var $this = $(this);
            $this.prop('tabindex', i + 1);
        });

        $('[data-file-preview]').each(function(){
            var $image = $(this);
            var $target = $($image.attr('data-file-preview'));

            $target.change(function(evt){
                if (this.files && this.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        $image.attr('src', e.target.result);
                    };
                    reader.readAsDataURL(this.files[0]);
                }
            });
        });
    });
    $(document).on('keydown.radio.data-api', '[data-toggle^=radio], .radio', function (e) {
        if( e.type === 'keydown' && e.keyCode === 32 ){
            $(this).trigger('click.radio.data-api');
        }
    });

    window.onscroll = function() {
        if (window.scrollY >= 90) {
            $('.cbp-spmenu-open').css('top', '0');
        } else {
            $('.cbp-spmenu-open').css('top', '');
        }
    };

})();
