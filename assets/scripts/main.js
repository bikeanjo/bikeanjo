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

        $('[data-counter]').each(function(i){
            var $this = $(this);
            var value = parseInt($this.attr('data-counter'), 10) || 1;
            var duration = parseInt($this.attr('data-counter-duration'), 10) || 500;
            var timeout = duration / (value > 0 ? value : 1);
            var factor = Math.pow(10, Math.floor(Math.log10(value)));
            var current = 0;
            $this.text(current);

            function increment() {
                current += Math.ceil(Math.random() * factor);

                if(current < value) {
                    $this.text(current);
                    setTimeout(increment, timeout);
                } else {
                    $this.text(value);
                }
            }
            increment();
        });

        $('select[autocomplete]').each(function(i){
            var $select = $(this).hide();
            var $ac_results = $('<div class="ac_results">')
                .appendTo(document.body);

            var $input = $('<input type="text">')
                .attr('class', $select.attr('class'))
                .attr('tabindex', $select.attr('tabindex'))
                .val($select.find(':selected').text())
                .insertAfter($select);

            var options = $select.find('option').map(function(i,e){
                return {
                    label: $(e).text(),
                    value: $(e).attr('value'),
                    desc: $(e).attr('desc')
                };
            }).toArray();

            $(window).resize(function(){
                $ac_results.css('top', ($input.offset().top + $input.outerHeight(true)) + 'px');
                $ac_results.css('left', ($input.offset().left) + 'px');
            });
            $(window).trigger('resize');

            $input.autocomplete({
                'source': options,
                'minLength': 3,
                'appendTo': $ac_results,
                'focus': function( event, ui ) {
                    $input.val(ui.item.label);
                    return false;
                },
                'select': function( event, ui ) {
                    $select.val(ui.item.value);
                    return false;
                }
            }).autocomplete( "instance" )._renderItem = function( ul, item ) {
              return $( "<li>" )
                .append(item.label + (item.desc?" ("+item.desc+")":''))
                .appendTo( ul );
            };

            $input.blur(function(evt){
                var selected = $select.find('option:selected').text();
                if(selected !== $input.val()) {
                    $input.val(selected);
                }
            });
        });

        $('input[suggests]').each(function(i){
            var $input = $(this);
            var $ac_results = $('<div class="ac_results">')
                .appendTo(document.body);

            var filter_key = $input.attr('suggests-filter-key');
            var $filter_value = $($input.attr('suggests-filter-value'));
            var json_key = 'suggests-json-key';
            
            var url = $input.attr('suggests');
            var query = {};
            var suggests = [];
            query[filter_key] = $filter_value.val();

            $(window).resize(function(){setTimeout(function(){
                $ac_results.css('top', ($input.offset().top + $input.outerHeight(true)) + 'px');
                $ac_results.css('left', ($input.offset().left) + 'px');
            }, 500);}).trigger('resize');

            $filter_value.change(function(evt){
                suggests.splice(0);

                $.ajax({
                    'url': url,
                    'data': query
                }).success(function(response){
                    response.forEach(function(r){
                        suggests.push(r.name);
                    });
                });
            }).trigger('change');

            $input.autocomplete({
                'source': suggests,
                'minLength': 3,
                'appendTo': $ac_results
            });
        });

        $('a[target=_popup]').click(function(evt){
            var href = $(this).attr('href');
            var title = $(this).attr('title') || 'Share';
            var left = Math.floor(($(window).width() - 500) / 2);
            var top = Math.floor(($(window).height() - 300) / 2);
            var win = window.open(href, title, 'left='+left+',top='+top+',width=500,height=300,toolbar=no,location=no');

            if(win) {
                evt.preventDefault();
            }
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
