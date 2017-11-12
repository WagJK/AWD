var schedule_offset = 0;
var available_offset = 0;

function search() {
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
    if (reset) available_offset = true;
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

function viewSchedule(delta_offset, reset=false){
    if (reset) schedule_offset = true;
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

function viewConfirmation(){
    $.ajax({
        url : "/student/message/confirmation/", // the endpoint
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

function sortProfile() {
   $.ajax({
        url : "/student/search/sort/", // the endpoint
        type : "POST", // http method
        data : {
            'option' : $('#sortOption').val(),
            'id_list': $('.short').map(function () {
                return this.id;
            }).get()
        },
        // handle a successful response
        success : function(response) {
            $('#searchResult').html(response);
        }
    });
}

function loadProfile(){
    $('#profile').css("display", "block");
}