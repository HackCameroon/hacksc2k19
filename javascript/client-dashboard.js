
function get_rented_vehicles()
{
$.ajax({
    url: 'https://34.212.86.167:80/rented_vehicles',
    type: 'GET',
    data: 
    {
    	"email": sessionStorage.getItem('user')
    },
    dataType: 'json',
    success: function(response) {
    	console.log(response);
    }

});

}