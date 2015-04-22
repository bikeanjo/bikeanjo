(function($, L) {
    'use strict';

    var Geocoder = {
        _geocoder: new google.maps.Geocoder(),

        code: function(address) {
            var defer = jQuery.Deferred();

            if(!address) {
                return defer.reject();
            }

            this._geocoder.geocode({'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    defer.resolve(results);
                } else {
                    defer.reject(status);
                }
            });
            return defer;
        }
    };

    var Bikemap = function(el, cfg) {
        var config = $.extend({
            center: [-23.548991, -46.633328],
            zoom: 14
        }, cfg);
        
        var map;
        var layers = [];
        var bikemap = this;

        this.initialize = function(el) {
            map = L.map(el).setView(config.center, config.zoom);
            var layer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
            layer.addTo(map);
            return map;
        };

        this.addMarker = function(lat, lon, text) {
            var marker = L.marker([lat, lon]);
            marker.bindPopup(text);
            marker.addTo(this.map);
            
            marker.remove = function() {
                var idx = layers.indexOf(marker);
                layers.splice(idx, 1);
                map.removeLayer(marker);
                return marker;
            };

            layers.push(marker);
            return marker;
        };

        this.addLine = function(p1, p2) {
            var line = new L.Polyline([p1, p2], {
                color: '#' + Math.random().toString(16).slice(-6),
                weight: 5,
                opacity: 1
            });
            line.remove = function() {
                var idx = layers.indexOf(line);
                layers.splice(idx, 1);
                map.removeLayer(line);
                return line;
            };
            layers.push(line);
            line.addTo(map);
            return line;
        };

        this.clearMap = function() {
            var layer;
            while(layers.length > 0) {
                layer = layers.pop();
                map.removeLayer(layer);
            }
        };

        this.bindInputs = function() {
            var $inputs = $(':input[bikeanjo-track]');
            var $start = $inputs.filter('[bikeanjo-track=start]');
            var $end = $inputs.filter('[bikeanjo-track=end]');

            var markers = { };
            var line;

            // autocomplete
            $inputs.each(function(i, el){
                var $el = $(el);
                new google.maps.places.Autocomplete(el,{
                    types: ['address'],
                    changed: $el.trigger.bind($el, 'address-changed'),
                    componentRestrictions: {country: 'br'}
                });
            });

            $inputs.on('address-changed', function(){
                var address = $(this).val();
                var type = $(this).attr('bikeanjo-track');

                Geocoder.code(address).then(function(results){
                    if(results.length < 1) {return; }
                    var lat = results[0].geometry.location.lat();
                    var lon = results[0].geometry.location.lng();

                    if(!markers[type]) {
                        markers[type] = bikemap.addMarker(lat, lon, address);
                    }
                    markers[type].setLatLng({lat: lat, lon: lon});
                    markers[type].setPopupContent(address);

                    if(markers.start && markers.end) {
                        if(line) {
                            line.setLatLngs([markers.start.getLatLng(),
                                             markers.end.getLatLng()]);
                        } else {
                            line = bikemap.addLine(markers.start.getLatLng(),
                                                   markers.end.getLatLng());
                        }
                    }

                    if(line) {
                        var paddingTop = $('form.signup').offset().top + $('form.signup').height();
                        map.fitBounds(line.getBounds(), {paddingTopLeft: [0, paddingTop]});
                    } else {
                        map.panTo(markers[type].getLatLng());
                    }
                });
            });

            $inputs.keydown(function(evt){
                if(evt.which === 13){ evt.preventDefault(); }
            });

            return $inputs;
        };

        this.map = this.initialize(el);
        this.bindInputs();
        this.layers = layers;
    };

    $(function(){
        window.bikemap = new Bikemap(document.getElementById('js-map'));
    });

})(jQuery, L);
