jQuery(function(){
    var __log = console.log.bind(console);
    // load apis

    if($("#js-map").length !== 1) {
        return;
    }

    var track = {
        'start': null,
        'end': null
    };

    var map = L.map('js-map').setView([-23.548991, -46.633328], 13);
    var geocoder = new google.maps.Geocoder();
    var $list = $("#js-addresses");
    var $addBtn = $("#js-add-address");
    var $addressInput = $('#departing-address,#destination-address');
    var $jsonPointsInput = $("#id_json_points");

    function insertInList(start, end) {
        return $('<li>')
            .append($('<i class="fa fa-times">'))
            .append($('<span class="departing-address">').text(start))
            .append($('<i class="fa fa-arrow-right"></i>'))
            .append($('<span class="destination-address">').text(end))
            .appendTo($list);
    }

    // basic geoCodeAddress
    function geoCodeAddress(address) {
        var defer = jQuery.Deferred();

        if(!address) {
            return defer.reject();
        }

        geocoder.geocode({'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                defer.resolve(results[0]);
            } else {
                defer.reject(status);
            }
        });
        return defer;
    }

    function addMarker(lat, lon, text) {
        var marker = L.marker([lat, lon]);
        marker.bindPopup(text);
        marker.addTo(map);

        return marker;
    }

    function addAddress(address) {
        return addMarker(
            address.geometry.location.lat(),
            address.geometry.location.lng(),
            address.formatted_address
        );
    }

    function insertInTrack(address, type) {
        track[type] = {
            address: address,
            marker: addAddress(address)
        };
        return track;
    }

    function removeTempMarker(type) {
        if (track && track[type]) {
            map.removeLayer(track[type].marker);
        }
    }

    function panTo(address) {
        map.panTo(L.latLng(
            address.geometry.location.lat(), 
            address.geometry.location.lng()
        ));
        return address;
    }

    /**
     * Setup
     */

    // setup leaflet
    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-i875mjb7'
    }).addTo(map);

    function selectAddress($input, type) {
        removeTempMarker(type);
        var address = $input.val();
        geoCodeAddress(address)
            .then(panTo)
            .then(function(a){ return insertInTrack(a, type); });
    }

    // setup autocomplete
    new google.maps.places.Autocomplete($addressInput.get(0),{
        types: ['address'],
        changed: selectAddress.bind(null, $addressInput.eq(0), 'start'),
        componentRestrictions: {country: 'br'}
    });

    new google.maps.places.Autocomplete($addressInput.get(1),{
        types: ['address'],
        changed: selectAddress.bind(null, $addressInput.eq(1), 'end'),
        componentRestrictions: {country: 'br'}
    });

    $('form').submit(function(evt) {
        try {
            var json = {
                start: {
                    address: $addressInput.eq(0).val(),
                    coords: {
                        lat: track.start.address.geometry.location.lat(),
                        lon: track.start.address.geometry.location.lng(),
                    }
                },
                end: {
                    address: $addressInput.eq(1).val(),
                    coords: {
                        lat: track.end.address.geometry.location.lat(),
                        lon: track.end.address.geometry.location.lng(),
                    }
                }
            };

            $jsonPointsInput.val(JSON.stringify(json));
        } catch (err) {
            console.error(err);
            evt.preventDefault();
        }
    });

    $addressInput.eq(0).focus();
    $addressInput.eq(0).click();

    // Desenha pontos se houverem na página
    if(window.TRACKS) {
        TRACKS.forEach(function(track){
            var p1 = track.coordinates[0];
            var p2 = track.coordinates[1];

            addMarker(p1[1], p1[0], track.properties.start);
            addMarker(p2[1], p2[0], track.properties.end);

            insertInList(track.properties.start, track.properties.end);
        });
        
        var lines = TRACKS.map(function(t){
            return {
                'type': 'LineString',
                'coordinates': t.coordinates
            };
        });

        var myStyle = {
            "color": "#ff7800",
            "weight": 5,
            "opacity": 0.65
        };

        L.geoJson(lines, {
            style: myStyle
        }).addTo(map);
    }

});
