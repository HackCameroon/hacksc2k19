var map;
var userLatitude = 34.040800499999996;
var userLongitude = -118.2557107;
var availableCars;


getAvailableCars();
getLocation();
function getAvailableCars(){
  console.log("Session storage: " + sessionStorage.getItem('user'));
$.ajax({
    url: 'https://34.212.86.167:80/available_cars',
    type: 'GET',
    data: 
    {
    },
    dataType: 'json',
    success: function(response) {
      console.log(response);
      availableCars = response;

      var divCol  = "<div class='col-sm-4 col-md-4'>";
        
        var divClose= "</div>";

        for(var prop in response) {
          console.log(response[prop].info);
           var make     = "<h3>"      + response[prop].info.make + " " + response[prop].info.model  + " " + 
            response[prop].info.year + "</h3>";
            var odometer = "<h3>" + response[prop].odometer.data.distance + " miles driven. </h3>";

            var linkStart = "<a href='" + response[prop] + "'>";
            var image     = "RENT NOW"
            var linkEnd   = "</a>";

            var div = divCol    +
                            make       +
                            odometer + 
                            linkStart       +
                            image       +
                            linkEnd +
                      divClose;

            $('.col-sm-12').append(div); // insert the div you've just created

        }

}

});

}




function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(setPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function setPosition(position) {
  userLatitude = position.coords.latitude;
  userLongitude = position.coords.longitude;
  
}

function initMap() {
getAvailableCars();
getLocation();
  
  map = new google.maps.Map(
      document.getElementById('map'),
      {center: new google.maps.LatLng(userLatitude, userLongitude), zoom: 16});

  var iconBase =
      './images/car_clipart_resized.png';

  
        for(var prop in response) {
          var contentString = 
          '<div id="content">' + 
          '<div id="siteNotice">' + 
          '</div>' + 
          '<h1 id="firstHeading" class="firstHeading">' +  + '</h1>'+
            '<div id="bodyContent">' +


        }

  var features = [
    {
      position: new google.maps.LatLng(-33.91721, 151.22630)
    }, {
      position: new google.maps.LatLng(-33.91539, 151.22820)
    }
  ];

  // Create markers.
  for (var i = 0; i < features.length; i++) {
    var marker = new google.maps.Marker({
      position: features[i].position,
      icon: iconBase,
      map: map
    });
  };
}