$(document).ready(function(){
    var tabs = document.querySelectorAll(".tab")

    if (darkMode =="enabled"){
        tabs[0].style.backgroundColor = "rgb(25, 100, 119)"
        tabs[0].style.color = "white"
    }else{
        tabs[0].style.backgroundColor = "#c4cfea"
        tabs[0].style.color = "black"
    }
    
});


$("body").on("click", ".tab", function(){
console.log("we did it")


    var optionSelected = $(this).attr("id")

    if (optionSelected == "tab-one"){
        if (darkMode =="enabled"){
            $(this).css("background-color", "rgb(25, 100, 119)")
            $(".tab").not($(this)).css("background-color", "rgb(97, 61, 109)")
        }else{
            $(".tab").not($(this)).removeClass("black");
            $(".tab").not($(this)).removeClass("white");

            $(this).css("background-color", "hsl(223,50%,83%)")
            $(".tab").not($(this)).css("background-color", "#314f9a")
            $(this).toggleClass("black");
            $(".tab").not($(this)).toggleClass("white");
        }    
    } else if ( optionSelected == "tab-two"){
        if (darkMode =="enabled"){
            $(this).css("background-color", "rgb(25, 100, 119)")
            $(".tab").not($(this)).css("background-color", "rgb(97, 61, 109)")
        }else{
            $(".tab").not($(this)).removeClass("black");
            $(".tab").not($(this)).removeClass("white");
            $(this).css("background-color", "hsl(223,50%,83%)")
            $(".tab").not($(this)).css("background-color", "#314f9a")
            $(this).toggleClass("black");
            $(".tab").not($(this)).toggleClass("white");
        }    
    } else if (optionSelected == "tab-three"){
        if (darkMode =="enabled"){
            $(this).css("background-color", "rgb(25, 100, 119)")
            $(".tab").not($(this)).css("background-color", "rgb(97, 61, 109)")
        }else{
            $(".tab").not($(this)).removeClass("black");
            $(".tab").not($(this)).removeClass("white");
            $(this).css("background-color", "hsl(223,50%,83%)")
            // $(this).css("background-color", "hsl(61, 100%, 91%)")
            $(this).toggleClass("black");
            $(".tab").not($(this)).toggleClass("white");
            $(".tab").not($(this)).css("background-color", "#314f9a")
        }
    }
    console.log(optionSelected)
    $.ajax({
        method: 'GET',
        url: '/ticket-easy/users/update-tabs',
        data: {
                'option':optionSelected,
            },
            
            success:function(response){
                $("#tab-content").html(response)
            }
    });
})
console.log(document.body.scrollHeight)

// $(window).scroll(function() {
//     var y = $(this).scrollTop();
//     if (y > 500) {
//         console.log("okmain")
//       $('#second-pane').fadeIn();
//     } else {
//       $('.bottomMenu').fadeOut();
//     }
//   });