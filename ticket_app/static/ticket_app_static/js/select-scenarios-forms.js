import Select from './select.js'



$(document).ready(function(e){
    // $("form").submit(function(e){
    //     e.preventDefault();
    // });
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                }
            }
        }
        return cookieValue;
    }
    $.ajaxSetup({
        headers:{
        'X-CSRFToken': getCookie("csrftoken")
        }
    });


    console.log("pickles")

    // ticket creation form .  see new-ticket-new-category.js 
    // $("#send-form").on("click", function(e){
    //     var priority = $(".new-ticket-priority").find(".custom-select-option.selected").text()
    //     var category = $(".new-ticket-category").find(".custom-select-option.selected").text()
    //     var description = $("#new-ticket-description").val()


    //     $.ajax({
    //         method: 'POST',
    //         url: '/create_ticket',
    //         data: {
    //                 "ajax":"ajax",
    //                 "priority": priority,
    //                 "category": category,
    //                 "desc": description,
    //             },
    //         success:function(response){
    //             $("body").html(response)
    
    //             const selectElements = document.querySelectorAll('[data-select]')
    //             selectElements.forEach(selectElement => {
    //                 // make new custom select 
    //                     new Select(selectElement)
    //                 // delete old select 
    //                     selectElement.remove()
    //             });
    //         }
    //     });
    
    // });
})
