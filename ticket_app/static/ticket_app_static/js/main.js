$(document).ready(function(){
    window.setTimeout(function(){
        $("#success-new").fadeOut(500)
        $("#errors-new").fadeOut(500)
        window.setTimeout(function(){
            $("#see-messages-again").fadeIn(100)
        }, 600);
    }, 5000);


    $("#see-messages-again").on("click", function(){
        $(this).fadeOut(100)
        $("#close-messages").fadeIn(100)
        $("#success-new").fadeIn(100)
        $("#errors-new").fadeIn(100)
    });
    $("#close-messages").on("click", function(){
        $("#see-messages-again").fadeIn(100)
        $(this).fadeOut(100)
        $("#success-new").fadeOut(100)
        $("#errors-new").fadeOut(100)
    });
});