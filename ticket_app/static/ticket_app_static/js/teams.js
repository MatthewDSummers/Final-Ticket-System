import updateSelects from "./import-Select.js"

$(document).ready(function(){
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
    console.log("Teams loading")




    // ADDING MEMBERS
    $(document).on("click", ".submit-team", function(){
        var team = document.querySelector(".custom-select-value").innerText
        var checks = document.querySelectorAll(".check")
        var members = []
        for (const checkbox of checks){
            if (checkbox.checked == true){
                members.push(checkbox.dataset.member)
            }
        }

        if (team !== "Select a team"){
            console.log(members, "MEMBERS")
            $("#error").hide()
            $.ajax({
                method: 'POST',
                url: '/new-team',
                data: {
                        "adding-members": "yes",
                        "team":team,
                        "members":JSON.stringify(members)
                    },
                success:function(response){
                    // console.log(response)
                }
            });
        }else{
            $("#error").show()
        }

    })




    // FILTER TEAMS FOR SPECIFIC TEAM

    $(document).on("click", "#team-select > .custom-select-options > .custom-select-option", function(){
        var option = $(this).text()

            $.ajax({
                method: 'GET',
                url: `/teams?filter=specific&value=${option}`,
                data: {
                    "nothing": "nothing"
                    },
                success:function(response){
                    $("#specific-team").html(response)
                    // updateSelects()
                    // console.log(response)
                }
            });


    })


    // FILTER OPTIONS OF A SPECIFIC TEAM
    $(document).on("click", "#team-options > .custom-select-options > .custom-select-option", function(){
        var category = $(this).text()
        var team =  $("#team-select > .custom-select-options > .custom-select-option.selected").text()
        if (category !== "Add Task"){
            $.ajax({
                method: 'GET',
                url: `/teams?filter=specific&value=${team}&category=${category}`,
                data: {
                    "nothing": "nothing"
                    },
                success:function(response){
                    $("#specific-team").html(response)
                }
            });
        }else if(category == "Add Task"){
            console.log("showing tasks")
            $("#task-options").show()
        }
    })

    // ADDING A TASK TO A TEAM 
    $(document).on("click", "#task-options > .custom-select-options > .custom-select-option", function(e){
        var task_id = e.currentTarget.dataset.value
        var team =  $("#team-select > .custom-select-options > .custom-select-option.selected").text()
        console.log(team, "TEU")
        console.log(task_id, "task")
        $("#confirm").show()
        // do the ajax next 
    })
});