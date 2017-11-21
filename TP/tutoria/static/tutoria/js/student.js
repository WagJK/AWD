var schedule_offset = 0;
var available_offset = 0;
var hover_restore_text = "";

function home() {
	$(".active").removeClass("active");
	$("#nav-home").parent().addClass("active");
}

function loadProfile(){
	$('#profile').css("display", "block");
}

// ====================================================
// =================== Calendar =======================
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

// ===================================================
// ================== Notification ===================
function viewNotification(){
	$(".active").removeClass("active");
	$("#nav-notf").parent().addClass("active");
	$("#num-unread-notf").addClass("disable");
	$.ajax({
		url : "/notification/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}

function updateNumOfMsg() {
	$.ajax({
		url : "/student/homepage/getNumOfMsg", // the endpoint
		type : "POST", // http method
		// handle a successful response
		success : function(response) {
			if (response != "0") {
				$("#num-unread-msg").text(response);
				$("#num-unread-msg").removeClass("disable");
			} else {
				$("#num-unread-msg").addClass("disable");
			}
		}
	});
	
}

function updateNumOfNotf() {
	$.ajax({
		url : "/student/homepage/getNumOfUnreadNotf", // the endpoint
		type : "POST", // http method
		// handle a successful response
		success : function(response) {
			if (response != "0") {
				$("#num-unread-notf").text(response);
				$("#num-unread-notf").removeClass("disable");
			} else {
				$("#num-unread-notf").addClass("disable");
			}
		}
	});
}

// ==================================================
// ================== Messaging =====================
function viewMessage(){
	$(".active").removeClass("active");
	$("#nav-msg").parent().addClass("active");
	$("#num-unread-msg").addClass("disable");
	$.ajax({
		url : "/message/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}

function writeMessage(target) {
	$.ajax({
		url : "/message/write/", // the endpoint
		type : "POST", // http method
		data : {
			'target' : target
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
		}
	});
}

function sendMessage(target) {
	content = $("#content").val();
	$.ajax({
		url : "/message/send/", // the endpoint
		type : "POST", // http method
		data : {
			'target' : target,
			'content' : content
		},
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
		}
	});
}

// ==========================================================
// ======================== Wallet ==========================
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

// ============================================================
// ======================== Detail Info =======================
function viewBookingInfo(slotID){
	$.ajax({
		url : "/student/schedule/bookingInfo/", // the endpoint
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

function viewTimeslotInfo(slotID){
	$.ajax({
		url : "/student/search/timeslotInfo/", // the endpoint
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

// ============================================================
// ======================= Search =============================
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
			'limited': $('.coverage:checked').map(function() {
				return this.value;
			}).get(),
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

// ===============================================================
// ======================== Operations ===========================
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
				updateNumOfNotf();
			}
		});
	}
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
				updateNumOfNotf();
			}
		});
	}
}
// ===============================================================
