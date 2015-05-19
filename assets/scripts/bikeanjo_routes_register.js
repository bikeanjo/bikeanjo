;(function($, L) {
    'use strict';

    var Geocoder = function() {
        var _geocoder = new google.maps.Geocoder();

        this.code = function(address) {
            var defer = jQuery.Deferred();

            if(!address) {
                return defer.reject();
            }

            _geocoder.geocode({'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    defer.resolve(results);
                } else {
                    defer.reject(status);
                }
            });
            return defer;
        };
    };

    var Bikemap = function(el, cfg) {
        var geocoder = new Geocoder();

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
            return map;
        };

        this.render_points = function() {
            var $line_output = $(':input[bikeanjo-geojson=points]');
            if(!$line_output.val()) {
                return map;
            }

            var points = JSON.parse($line_output.val());
            if(points.length === 0) {
                return map;
            }

            var bounds = new L.LatLngBounds();
            for(var i=0; i < points.length; i++) {
                var p = points[i];
                var marker = this.addMarker(p.coordinates[1],
                                            p.coordinates[0],
                                            p.properties.address);
                marker.id = p.properties.id;
                bounds.extend(marker.getLatLng());
            }
            var paddingTop = 10;
            if($('.card.signup').length > 0){
                paddingTop = $('.card.signup').offset().top + $('.card.signup').height();
            }
            map.fitBounds(bounds, {paddingTopLeft: [0, paddingTop]});
            return map;
        };

        this.render_lines = function() {
            var $line_output = $(':input[bikeanjo-geojson=lines]');
            if(!$line_output.val()) {
                return map;
            }

            var lines = JSON.parse($line_output.val());
            if(lines.length === 0) {
                return map;
            }

            var bounds = new L.LatLngBounds();

            for(var i=0; i < lines.length; i++) {
                var l = lines[i];
                var p1 = l.coordinates[0].reverse();
                var p2 = l.coordinates[1].reverse();

                var line = this.addLine(p1, p2);
                bounds.extend(line.getBounds());

                line.id = l.properties.id;
                line.related = [
                    this.addMarker(p1[0], p1[1], l.properties.start),
                    this.addMarker(p2[0], p2[1], l.properties.end)
                ];
            }
            var paddingTop = 10;
            if($('.card.signup').length > 0){
                paddingTop = $('.card.signup').offset().top + $('.card.signup').height();
            }
            map.fitBounds(bounds, {paddingTopLeft: [0, paddingTop]});
            return map;
        };

        this.write_lines_to_output = function() {
            var $line_output = $(':input[bikeanjo-geojson=lines]');
            var lines = bikemap.layers
                .filter(function(l){
                    return l.constructor === L.Polyline && l.related ;
                })
                .map(function(l){
                    console.log(l);
                    return $.extend(l.toGeoJSON().geometry, {
                        properties:{
                            id: l.id,
                            start: l.related[0].getPopup().getContent(),
                            end: l.related[1].getPopup().getContent()
                        }
                    });
                });
            $line_output.val(JSON.stringify(lines));
            return map;
        };

        this.write_points_to_output = function() {
            var $line_output = $(':input[bikeanjo-geojson=points]');
            var points = bikemap.layers
                .filter(function(m){
                    return m.constructor === L.Marker;
                })
                .map(function(marker){
                    return $.extend(marker.toGeoJSON().geometry, {
                        properties:{
                            id: marker.id,
                            address: marker.getPopup().getContent(),
                        }
                    });
                });
            $line_output.val(JSON.stringify(points));
            return map;
        };

        this.render_lines_list = function() {
            var $list = $('[bikeanjo-list="lines"]');
            if($list.length === 0) {
                return;
            }
            bikemap.layers
                .filter(function(l){
                    return l.constructor === L.Polyline &&
                           l.related &&
                           l.related.length == 2;
                })
                .forEach(function(line) {
                    var marker1 = line.related[0];
                    var marker2 = line.related[1];

                    var $li = $('<li>');
                    $li.append($('<i class="fa fa-times">')
                                    .click(marker1.remove)
                                    .click(marker2.remove)
                                    .click(line.remove)
                                    .click(bikemap.write_lines_to_output)
                                    .click(function(){ $li.remove(); })
                                    )
                       .append($('<span class="departing-address">')
                                   .text(marker1.getPopup().getContent())
                                   .click(marker1.openPopup.bind(marker1)))
                       .append($('<i class="fa fa-arrow-right">'))
                       .append($('<span class="destination-address">')
                                   .text(marker2.getPopup().getContent())
                                   .click(marker2.openPopup.bind(marker2)));

                    $list.append($li);
                });
            return map;
        };

        this.render_points_list = function() {
            var $list = $('[bikeanjo-list="points"]');
            if($list.length === 0) {
                return;
            }
            $list.html('');

            bikemap.layers
                .filter(function(m){
                    return m.constructor === L.Marker;
                })
                .forEach(function(marker) {
                    var $li = $('<li>');
                    $li.append($('<i class="fa fa-times">')
                                    .click(marker.remove)
                                    .click(function(){ $li.remove(); })
                                    )
                       .append($('<span>')
                                   .text(marker.getPopup().getContent()));

                    $list.append($li);
                });
            return map;
        };

        this.bindInputs = function() {
            var $inputs = $(':input[bikeanjo-track]');
            var $outputs = $(':input[bikeanjo-geojson]');
            var $button = $(':input[bikeanjo-add=point]');

            var markers = { };
            var line;

            $button.click(function(evt) {
                evt.preventDefault();
                $inputs.val('');
                $inputs.focus();
                markers.point = null;
                bikemap.render_points_list();
                bikemap.write_points_to_output();
            });

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

                geocoder.code(address).then(function(results){
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
                }).then(function() {
                    if(line) {
                        var json = $.extend(line.toGeoJSON().geometry, {
                            'properties': {
                                'start': markers.start.getPopup().getContent(),
                                'end': markers.end.getPopup().getContent()
                            },
                        });
                        $outputs.filter('[bikeanjo-geojson=lines]').val(JSON.stringify([json]));
                    }
                });
            });

            $inputs.keydown(function(evt){
                if(evt.which === 13){ evt.preventDefault(); }
            });

            return map;
        };

        this.layers = layers;
        this.map = this.initialize(el);
        this.bindInputs();
        this.render_lines();
        this.render_lines_list();
        this.render_points();
        this.render_points_list();
    };

    $(function(){
        var map_canvas = document.getElementById('js-map');
        if(map_canvas) {
            window.bikemap = new Bikemap(map_canvas);
        }
    });

})(jQuery, L);
