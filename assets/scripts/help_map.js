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
    var $geocoderInput = $('#geocoder-input');
    var $jsonPointsInput = $("#id_json_points");
    var points = [ ];

    // setup leaflet
    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-i875mjb7'
    }).addTo(map);


    // basic geoCodeAddress
    function geoCodeAddress(address) {
        var defer = jQuery.Deferred();

        if(!address) {
            return defer.reject();
        }

        geocoder.geocode({'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                defer.resolve(results);
            } else {
                defer.reject(status);
            }
        });
        return defer;
    }

    // let user select correct address
    function selectCorrectAddress(addresses) {
        if(addresses.length === 1) {
            return addresses[0];
        }

        var str = 'Escolha o endereço correto:\n\n';
        addresses.forEach(function(address, i){
            str += sprintf('(%3d) - ', i+1);
            str += address.formatted_address;
            str += '\n';
        });

        var index = parseInt(prompt(str), 10);
        if(index > 0) {
            return addresses[index - 1];
        }
        return addresses[0];
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

    // setup elements and events
    $addBtn.click(function(){
        if(tempMarker) {
            points.push(tempMarker);
            appendOnList(tempMarker);
            tempMarker = null;
        }
        $geocoderInput.val('');
        $geocoderInput.focus();
        $geocoderInput.click();
        return false;
    });

    $geocoderInput.keydown(function(e){
        if(e.which === 13) {
            removeTempMarker();
            var address = $(this).val();
            geoCodeAddress(address)
                .then(selectCorrectAddress)
                .then(addTempMarker)
                .then(__log);
            return false;
        }
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
