// If native datepicker unavailable falling back to jQuery UI’s
if (!Modernizr.inputtypes.date) {
    $(function (){
        $('input[type=date]').datepicker();
    });
}
