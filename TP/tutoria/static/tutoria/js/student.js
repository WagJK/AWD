var schedule_offset = 0;
var available_offset = 0;
var hover_restore_text = "";

function home() {
	$(".active").removeClass("active");
	$("#nav-home").parent().addClass("active");
}

function search() {
	$(".active").removeClass("active");
	$("#nav-search").parent().addClass("active");
	$.ajax({
		url : "/student/search/searchOption/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			//$('#searchButton').css("display", "none");
			$('#profile').css("display", "none");
		}
	});
}

function viewSchedule(delta_offset, reset=false){
	$(".active").removeClass("active");
	$("#nav-schedule").parent().addClass("active");
	
	if (reset) schedule_offset = 0;
	schedule_offset += delta_offset;
	$.ajax({
		url : "/student/schedule/", // the endpoint
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

function viewNotification(){
	$(".active").removeClass("active");
	$("#nav-conf").parent().addClass("active");
	$.ajax({
		url : "/student/message/notification/", // the endpoint
		type : "GET", // http method
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
		url : "/student/wallet/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}


function getShortProfiles() {
	$.ajax({
		url : "/student/search/shortProfile/", // the endpoint
		type : "POST", // http method
		data : {
			'university_list': $('.university:checked').map(function() {
				return this.value;
			}).get(),
			'course_list': $('.course:checked').map(function() {
				return this.value;
			}).get(),
			'tag_list': $('.tag:checked').map(function() {
				return this.value;
			}).get(),
			'min_rate': $('#min').val(),
			'max_rate': $('#max').val(),
			'type': $('.type:checked').map(function() {
				return this.value;
			}).get(),
			'limited': ($('.coverage:checked').map(function() {
				return this.value;
			}).get()).length,
			'last_name': $('#last').val(),
			'first_name': $('#first').val()
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
		}
	});
}

function getDetailedProfile(tutorID){
	$.ajax({
		url : "/student/search/detailedProfile/", // the endpoint
		type : "POST", // http method
		data : {
			'tutorID' : tutorID
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
		}
	});
}

function getAvailableSlots(tutorID, delta_offset, reset=false){
	if (reset) available_offset = 0;
	available_offset += delta_offset;
	$.ajax({
		url : "/student/search/availableSlot/", // the endpoint
		type : "POST", // http method
		data : {
			'tutorID' : tutorID,
			'offset' : available_offset
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
		}
	});
}

function bookSlot(slotID){
	var bookOrNot = confirm("Are you sure to book this timeslot?");
	if (bookOrNot){
		$.ajax({
			url : "/student/search/bookSlot/", // the endpoint
			type : "POST", // http method
			data : {
				'slotID' : slotID
			},
			// handle a successful response
			success : function(response) {
				$('#searchResult').html(response);
				$('#searchButton').css("display", "block");
			}
		});
	}
}

function hoverCancel(that){
	hover_restore_text = $(that).text()
	$(that).text("Cancel");
}

function unhoverCancel(that){
	$(that).text(hover_restore_text);
}

function cancelSlot(slotID){
	var cancelOrNot = confirm("Are you sure to cancel this timeslot?");
	if (cancelOrNot){
		$.ajax({
			url : "/student/schedule/cancelSlot/", // the endpoint
			type : "POST", // http method
			data : {
				'slotID' : slotID
			},
			// handle a successful response
			success : function(response) {
				$('#searchResult').html(response);
			}
		});
	}
}

function addValue(value) {
	$.ajax({
		url : "/student/wallet/addValue/", // the endpoint
		type : "POST", // http method
		data : {
			'value' : value
		},
		// handle a successful response
		success : function(response) {
			$('#balance').html("Balance: " + response + " HKD");
		}
	});
}

function sortProfile(option) {
	$.ajax({
		url : "/student/search/sort/", // the endpoint
		type : "POST", // http method
		data : {
			'option' : option,
			'id_list': $('.short').map(function () {
				return this.id;
			}).get()
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$("#sortMenu").text(option);
		}
	});
}

function loadProfile(){
	$('#profile').css("display", "block");
}