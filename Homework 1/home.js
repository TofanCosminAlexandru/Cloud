eventArray = [];

function getAddress() {
    var lat, lng;
    eventArray = [];
    select = document.getElementById('mySelect');
    address = document.getElementById('cityName').value;
    if (address.length > 0) {
        // url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyDrBJbizSYysEoyj-5ol6QgiPng4nepjOA";
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=AIzaSyDrBJbizSYysEoyj-5ol6QgiPng4nepjOA";
        fetch(url)
            .then((resp) => resp.json())
            .then(function (data) {
                lat = data.results[0].geometry.location.lat;
                lng = data.results[0].geometry.location.lng;
                console.log(lat, lng);

                url = "http://localhost:3000/events?lat=" + lat + "&lng=" + lng + "&distance=13000&sort=venue&accessToken=EAAFAZCZBtMuvABAGr86CZBAqsnRTwGMHIvrHntJ8wcKqTezHmzynzZAZBh716CWnh1KYTeDZCFZAemJlZCg4OT0ObiEwnuTTEwyBBUaYrwuXKlxN7Bz8kbvabNBsskHl20k5LPhrOZAqw6N8wl5AH4dV0sUA57mYFAASZBEV3G2UOnMgZDZD";
                // url = "http://localhost:3000/events?lat="+lat+"&lng="+lng+"&distance=1000&sort=venue&accessToken=EAAFAZCZBtMuvABAM5P1UTfQTl7waJi8ffns2iEv2fxTupJIgGbElMpxXBK6rA6wtwRG9e4NLgpxdJTokhwHWUeHRQCg8c7rWjZBuv3XiQId3nQzGjqSOOnoaZA73ZA6nURmpc5JJ4kyzaZCdKD1hyE1ko4Krel6hfNS8J9GRMy3x38UHbKOlOVZCnCFWfql4LQd5aWNcNZB0ZBAZDZD";
                // url = "https://graph.facebook.com/search?q=*&type=event&center="+lat+","+lng+"&distance=100&access_token=EAAFAZCZBtMuvABAGr86CZBAqsnRTwGMHIvrHntJ8wcKqTezHmzynzZAZBh716CWnh1KYTeDZCFZAemJlZCg4OT0ObiEwnuTTEwyBBUaYrwuXKlxN7Bz8kbvabNBsskHl20k5LPhrOZAqw6N8wl5AH4dV0sUA57mYFAASZBEV3G2UOnMgZDZD&limit=50";
                fetch(url)
                    .then((resp) => resp.json())
                    .then(function (data) {
                        console.log(data.events.length);
                        document.getElementById("mySelect").innerHTML = "-";
                        for (i = 0; i < data.events.length; i++) {
                            console.log(data.events[i]);
                            eventArray.push(data.events[i]);
                            var opt = document.createElement('option');
                            opt.value = data.events[i];
                            opt.innerHTML = data.events[i].name;
                            select.appendChild(opt);
                        }
                        console.log(eventArray.length);
                    })
            })
    }
    else {
        alert("Scrie ceva");
    }
}

var myLat, myLng;

eventAddressCity = "";

function getInfo() {
    document.getElementById("textInfo").innerHTML = eventArray[document.getElementById("mySelect").selectedIndex].description;
    var img = document.getElementById("img_cover");
    img.src = eventArray[document.getElementById("mySelect").selectedIndex].coverPicture;
    eventAddressStreetlat = eventArray[document.getElementById("mySelect").selectedIndex].place.location.latitude;
    eventAddressStreetlng = eventArray[document.getElementById("mySelect").selectedIndex].place.location.longitude;
    eventAddressCity = eventArray[document.getElementById("mySelect").selectedIndex].place.location.city;
    console.log(eventAddressCity);
    var src = document.getElementById("info");
    src.appendChild(img);
    navigator.geolocation.getCurrentPosition(function (position) {
        pos = [
            position.coords.latitude,
            position.coords.longitude
        ];

        url = "https://www.mapquestapi.com/geocoding/v1/reverse?key=NaQmrtISNmdOXt7iYOFL88BjGDObEUOX&location=" + pos[0] + "%2C" + pos[1] + "&outFormat=json&thumbMaps=false";
        fetch(url)
            .then((resp) => resp.json())
            .then(function (data) {
                myAddress = data.results[0].locations[0].street;
                myAddressCity = data.results[0].locations[0].adminArea3;
                console.log(data.results[0].locations[0].street);

                url = "https://www.mapquestapi.com/geocoding/v1/reverse?key=NaQmrtISNmdOXt7iYOFL88BjGDObEUOX&location=" + eventAddressStreetlat + "%2C" + eventAddressStreetlng + "&outFormat=json&thumbMaps=false";
                fetch(url)
                    .then((resp) => resp.json())
                    .then(function (data) {
                        eventAddress = data.results[0].locations[0].street;
                        eventAddressCity = data.results[0].locations[0].adminArea3;
                        console.log(data.results[0].locations[0].street);
                        console.log(eventAddressCity);


                        myAddress = myAddress.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
                        eventAddress = eventAddress.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
                        eventAddressCity = eventAddressCity.normalize('NFD').replace(/[\u0300-\u036f]/g, "");

                        console.log(myAddress);
                        console.log(eventAddress);
                        console.log(eventAddressCity);

                        L.mapquest.key = 'NaQmrtISNmdOXt7iYOFL88BjGDObEUOX';

                        document.getElementById("map").remove();
                        var div = document.createElement("div");
                        div.id = "map";
                        var map_pos = document.getElementById("info");
                        map_pos.appendChild(div);

                        var map = L.mapquest.map('map', {
                            center: [47.1584549, 27.6014418],
                            layers: L.mapquest.tileLayer('map'),
                            zoom: 5
                        });
                        map.addControl(L.mapquest.control());

                        L.mapquest.directions().route({
                            start: myAddress + " " + myAddressCity + ' Romania',
                            end: eventAddress + " " + eventAddressCity + ' Romania'
                        });

                        document.getElementById("from").innerHTML = myAddress + " " + myAddressCity + ' Romania';
                        document.getElementById("to").innerHTML = eventAddress + " " + eventAddressCity + ' Romania';
                    })
            })
    });
}