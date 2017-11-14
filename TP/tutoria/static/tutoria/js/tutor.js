function home() {
	$(".active").removeClass("active");
	$("#nav-home").parent().addClass("active");
}

function viewSchedule(delta_offset, reset=false){
	$(".active").removeClass("active");
	$("#nav-schedule").parent().addClass("active");
	
	if (reset) schedule_offset = 0;
	schedule_offset += delta_offset;
	$.ajax({
		url : "/tutor/schedule/", // the endpoint
		type : "POST", // http method
		data : {
			'offset' : schedule_offset
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}


function viewConfirmation(){
	$(".active").removeClass("active");
	$("#nav-schedule").parent().addClass("active");
	$.ajax({
		url : "/tutor/message/confirmation/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}

function withdraw() {
	$.ajax({
		url : "/tutor/wallet/withdraw/", // the endpoint
		type : "POST", // http method
		data : {
			'value' : $('#value').val()
		},
		// handle a successful response
		success : function(response) {
			$('#balance').html(response);
		}
	});
}

function loadProfile(){
	$('#profile').css("display", "block");
}