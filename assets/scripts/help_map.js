jQuery(function(){
    // load apis
    var map = L.map('map').setView([51.505, -0.09], 13);
    var geocoder = new google.maps.Geocoder();

    // setup leaflet
    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-i875mjb7'
    }).addTo(map);

    function placeOnMap(address) {
        L.marker([
            address.geometry.location.lat(), 
            address.geometry.location.lng(), 
        ]).addTo(map)
          .bindPopup(address.formatted_address).openPopup();
    }

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

    // setup elements
    var $geocoderInput = $('#geocoder-input');
    $geocoderInput.keydown(function(e){
        if(e.which === 13) {
            var address = $(this).val();
            geoCodeAddress(address)
                .then(selectCorrectAddress)
                .then(placeOnMap);

            return false;
        }
    });

});
