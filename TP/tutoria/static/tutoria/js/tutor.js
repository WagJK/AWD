var schedule_offset = 0;
var hover_restore_text = "";

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

function viewWallet() {
	$(".active").removeClass("active");
	$("#nav-wallet").parent().addClass("active");
	$.ajax({
		url : "/tutor/wallet/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}

function viewNotification(){
	$(".active").removeClass("active");
	$("#nav-schedule").parent().addClass("active");
	$.ajax({
		url : "/tutor/message/notification/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}

function activate(that, time) {
	$.ajax({
		url : "/tutor/schedule/activate/", // the endpoint
		type : "POST", // http method
		data : {
			'time' : time
		},
		// handle a successful response
		success : function(response) {
			$(that).removeClass("timeslot-activate");
			$(that).addClass("timeslot-available");
			$(that).text("available");
			$(that).attr("onclick", "deactivate(this, '" + response +"')");
			$(that).attr("onmouseover", "hoverDeactivate(this)");
			$(that).attr("onmouseout", "unhoverDeactivate(this)");
		}
	});
}

function hoverActivate(that){
	hover_restore_text = $(that).text()
	$(that).text("activate");
}

function unhoverActivate(that){
	$(that).text("unavailable");
}

function deactivate(that, slotID) {
	$.ajax({
		url : "/tutor/schedule/deactivate/", // the endpoint
		type : "POST", // http method
		data : {
			'slotID' : slotID
		},
		// handle a successful response
		success : function(response) {
			$(that).removeClass("timeslot-available");
			$(that).addClass("timeslot-activate");
			$(that).text("unavailable");
			$(that).attr("onclick", "activate(this, '" + response +"')");
			$(that).attr("onmouseover", "hoverActivate(this)");
			$(that).attr("onmouseout", "unhoverActivate(this)");
		}
	});
}

function hoverDeactivate(that){
	hover_restore_text = $(that).text()
	$(that).text("blackout");
}

function unhoverDeactivate(that){
	$(that).text("available");
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
			$('#balance').html("Balance: " + response + " HKD");
		}
	});
}

function loadProfile(){
	$('#profile').css("display", "block");
}