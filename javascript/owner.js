if(sessionStorage.getItem('user') == null)
  window.location.replace('/login.html');

var map;
var userLatitude = 34.040800499999996;
var userLongitude = -118.2557107;
var availableCars;

$("#new-button2").click(function() {
$.ajax({
    url: 'https://34.212.86.167:80/login',
    type: 'GET',
    data: 
    {
      "email": sessionStorage.getItem('user')
    },
    dataType: 'json',
    success: function(response) {console.log(response);}

});
});

getAvailableCars();

function getAvailableCars(){
  console.log("Session storage: " + sessionStorage.getItem('user'));
$.ajax({
    url: 'https://34.212.86.167:80/registered_vehicles',
    type: 'GET',
    data: 
    {
      "email": sessionStorage.getItem('user')
    },
    dataType: 'json',
    success: function(response) {
      console.log(response);
      availableCars = response;

      var divCol  = "<div class='profile col-md-4'>";
        
      var divClose= "</div>";

      for(var prop in response) {
        console.log(response[prop].info);
          var make     = "<h3>"      + response[prop].info.make + " " + response[prop].info.model  + " " + 
            response[prop].info.year + "</h3>";
          var odometer = "<p>" + Math.round(response[prop].odometer.data.distance).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " kilometers driven. </p>";
          var brand = response[prop].info.make;
          var image = "<img src='../images/" + brand.toLowerCase() + ".jpg' class='img-responsive pic2' />";
          var rented     = (response[prop].rented) ? "<p style = 'font-weight:500;'> RENTED</p>" : "<p style = 'font-weight:500;'> AVAILABLE </p>";


            var div = divCol    + image +
                            make       +
                            odometer + 
                            
                            rented       +
                            
                      divClose;

            $('.row').append(div); // insert the div you've just created

        }

}

});

}
