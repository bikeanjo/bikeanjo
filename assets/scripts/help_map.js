jQuery(function(){
    var __log = console.log.bind(console);
    // load apis

    if($("#js-map").length !== 1) {
        return;
    }

    var tempMarker = null;
    var map = L.map('js-map').setView([-23.548991, -46.633328], 13);
    var geocoder = new google.maps.Geocoder();
    var $list = $("#js-addresses");
    var $addBtn = $("#js-add-address");
    var $addressInput = $('#geocoder-input');
    var $jsonPointsInput = $("#id_json_points");
    var points = [ ];

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

    function appendOnList(marker) {
        var $li = $('<li>').text(marker.address.formatted_address);
        $li.appendTo($list);
    }

    function addMarker(address) {
        var marker = L.marker([
            address.geometry.location.lat(), 
            address.geometry.location.lng(), 
        ]);
        marker.bindPopup(address.formatted_address);
        marker.addTo(map);
        marker.address = address;

        return marker;
    }

    function addTempMarker(address) {
        tempMarker = addMarker(address);
        return tempMarker;
    }

    function removeTempMarker() {
        if (tempMarker) {
            map.removeLayer(tempMarker);
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

    function selectAutocompleteAddress() {
        removeTempMarker();
        var address = $addressInput.val();
        geoCodeAddress(address)
            .then(panTo)
            .then(addTempMarker)
            .always(__log);
    }

    // setup autocomplete
    window.autocomplete = new google.maps.places.Autocomplete($addressInput.get(0),{
        types: ['address'],
        changed: selectAutocompleteAddress,
        componentRestrictions: {country: 'br'}
    });


    // setup elements and events
    $addBtn.click(function(){
        if(tempMarker) {
            points.push(tempMarker);
            appendOnList(tempMarker);
            tempMarker = null;
        }
        $addressInput.val('');
        $addressInput.focus();
        $addressInput.click();
        return false;
    });

    $('form').submit(function() {
        var json = points.map(function(marker){
            return {
                'address': marker.address.formatted_address,
                'lat': marker.address.geometry.location.lat(),
                'lon': marker.address.geometry.location.lng()
            };
        });
        $jsonPointsInput.val(JSON.stringify(json));
    });
});
