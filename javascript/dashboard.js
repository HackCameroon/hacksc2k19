var map;
var userLatitude;
var userLongitude;

getLocation();
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
  initMap();
}

function initMap() {


  map = new google.maps.Map(
      document.getElementById('map'),
      {center: new google.maps.LatLng(userLatitude, userLongitude), zoom: 16});

  var iconBase =
      './images/car_clipart_resized.png';

  
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