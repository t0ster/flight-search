// If native datepicker unavailable falling back to jQuery UI’s
if (!Modernizr.inputtypes.date) {
    $(function (){
        $('input[type=date]').datepicker();
    });
}

$(function (){
    if ($('.search_results_page').length){
        $.get(window.location.pathname + window.location.search, function(data) {
            setTimeout(function() {$('#help_alert').modal()}, 5000);  // Help alert
            $(".inner_content").html(data);
        });
    }
});
