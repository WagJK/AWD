var schedule_offset = 0;
var hover_restore_text = "";

// ====================================================
// =================== Calendar =======================
function viewTutorSchedule(delta_offset, reset=false){
	$(".active").removeClass("active");
	$("#nav-tutor-schedule").parent().addClass("active");
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
			$(that).text("blackout");
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

// ============================================================
// ======================== Detail Info =======================
function viewTutorBookingInfo(slotID){
	$.ajax({
		url : "/tutor/schedule/bookingInfo/", // the endpoint
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

// ==============================================================
// ======================== Edit profile =========================
function editTutorProfile(){
	$.ajax({
		url : "/tutor/homepage/editProfile/",
		type : "GET",
		success : function(response) {
			$('#searchResult').html(response);
			$('#searchResult').css("display","block");
			$('#profile').css("display","none");
		}
	});
}

function postTutorProfile(){
	$.ajax({
		url : "/tutor/homepage/editProfile/",
		type : "POST",
		data : {
			'firstname' : $("#firstname").val(),
			'lastname' : $("#lastname").val(),
			'email' : $("#email").val(),
			'phone' : $("#phone").val(),
			'availability' : $("#availability").val(),
			'tutortype' : $("#tutortype").val(),
			'hourlyrate' : $("#hourlyrate").val(),
			'university' : $("#university").val(),
			'course_list': $('.course:checked').map(function() {
				return this.value;
			}).get(),
			'newcourses' : $("#newcourses").val(),
			'tag_list': $('.tag:checked').map(function() {
				return this.value;
			}).get(),
			'newtags' : $("#newtags").val(),
			'username' : $("#username").val(),
			'oldpassword' : $("#oldpassword").val(),
			'password' : $("#password").val(),
			'confirmpassword' : $("#confirmpassword").val(),
			'biography' : $("#biography").val()
		},
		success : function(response) {
			$('#searchResult').html(response);
			$('#searchResult').css("display","block");
			$('#profile').css("display","none");
		}
	});
}
/*
function flushCourse(){
	var university = $("#university").val()
	$.ajax({
		url : "/tutor/homepage/editProfile/flushCourse/",
		type : "POST",
		data : {
			'university' : university
		},
		success : function(response) {
			$('#CourseDiv').html(response);
		}
	});
}*/
function flushCourse(){
	$('#CourseDiv').html("<div id=\"CourseDiv\" class=\"form-group\"><label class=\"col-lg-3 control-label\">Courses:</label><div class=\"col-lg-8\"></div></div>");
}

function flushHourlyrate(){
	var tutor_type = $("#tutortype").val()
	if (tutor_type == "Private"){
		$("#HourlyrateDiv").css("display","block")
	} else {
		$("#HourlyrateDiv").css("display","none")
		$("#hourlyrate").val(0)
	}
}
// ===============================================================