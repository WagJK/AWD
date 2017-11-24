function home() {
	$("#alert").text('');
	$(".active").removeClass("active");
	$("#nav-home").parent().addClass("active");
}

function loadProfile(){
	$('#profile').css("display", "block");
}

// ==================================================
// ================== Notification ==================

function viewNotification(){
	$("#alert").text('');
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
			clearUnreadNotf();
		}
	});
}

function clearUnreadNotf(){
	$.ajax({
		url : "/notification/clearUnread/", // the endpoint
		type : "POST", // http method
		// handle a successful response
		success : function(response) {}
	});
}

function updateNumOfNotf() {
	$.ajax({
		url : "/notification/getNumOfUnreadNotf/", // the endpoint
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
	$("#alert").text('');
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
			clearUnreadMsg();
		}
	});
}

function clearUnreadMsg(){
	$.ajax({
		url : "/message/clearUnread/", // the endpoint
		type : "POST", // http method
		// handle a successful response
		success : function(response) {}
	});
}

function updateNumOfMsg() {
	$.ajax({
		url : "/message/getNumOfMsg/", // the endpoint
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

function writeMessage(target) {
	$("#alert").text('');
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
	$("#alert").text('');
	$(".active").removeClass("active");
	$("#nav-wallet").parent().addClass("active");
	$.ajax({
		url : "/wallet/", // the endpoint
		type : "GET", // http method
		// handle a successful response
		success : function(response) {
			$('#searchResult').html(response);
			$('#profile').css("display", "none");
		}
	});
}

function addValue() {
	var addOrNot = confirm("Are you sure to cancel this timeslot?");
	if (addOrNot){
		$.ajax({
			url : "/wallet/addValue/", // the endpoint
			type : "POST", // http method
			data : {
				'value' : $('#value').val()
			},
			// handle a successful response
			success : function(response) {
				viewWallet();
			}
		});
	}

}

function withdraw() {
	var withdrawOrNot = confirm("Are you sure to cancel this timeslot?");
	if (withdrawOrNot){
		$.ajax({
			url : "/wallet/withdraw/", // the endpoint
			type : "POST", // http method
			data : {
				'value' : $('#value').val()
			},
			// handle a successful response
			success : function(response) {
				viewWallet();
			}
		});
	}
}