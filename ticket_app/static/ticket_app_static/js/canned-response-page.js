$(document).ready(function(){

    $(".glossary-trigger").on("click", function(){
        $(this).find('.arrow').removeClass("up")
    
    
        if( $("#canned-response-glossary").css("display") == 'none'){
            $("#canned-response-glossary").show()
            $(this).find('.arrow').addClass("up")
        }else{
            $("#canned-response-glossary").hide()
        }

    })
});
