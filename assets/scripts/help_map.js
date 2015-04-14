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

    function addMarker(address) {
        var marker = L.marker([
            address.geometry.location.lat(), 
            address.geometry.location.lng(), 
        ]);
        marker.bindPopup(address.formatted_address);
        marker.addTo(map);

        return marker;
    }

    function addTempMarker(address, type) {
        track[type] = {
            address: address,
            marker: addMarker(address)
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
            .then(function(a){ return addTempMarker(a, type); });
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
                    address: $addressInput.val(),
                    coords: {
                        lat: track.start.address.geometry.location.lat(),
                        lon: track.start.address.geometry.location.lng(),
                    }
                },
                end: {
                    address: $addressInput.val(),
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
});
