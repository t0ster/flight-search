// If native datepicker unavailable falling back to jQuery UI’s
if (!Modernizr.inputtypes.date) {
    $(function (){
        $('input[type=date]').datepicker();
    });
}

// Help alert
$(function (){
    setTimeout(function() {$('#help_alert').modal()}, 5000);
});
