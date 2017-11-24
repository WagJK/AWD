function withdraw() {
	$.ajax({
		url : "/MyTutors/withdraw/", // the endpoint
		type : "POST", // http method
		data : {
			'value' : $('#value').val()
		},
		// handle a successful response
		success : function(response) {
			$('#balance').html("Balance: " + response + " HKD");
		}
	});
}