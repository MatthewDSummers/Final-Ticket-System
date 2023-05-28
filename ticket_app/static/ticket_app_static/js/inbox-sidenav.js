$(document).ready(function(){


// STYLE THE INBOX NAVMENU'S ACTIVE ITEM 
    var name = $(".title").text()
    if (name !== "Blank"){
        var actives = document.querySelectorAll(`.${name}`)
        for (const active of actives){
            console.log(active, "activity ", name )
            active.classList.add("inbox-sidebar-active")
        }
    }

// HIDE / SHOW THE MENU 
    $(".inbox-sidebar-container").mouseover( function (){
        $("#inbox-sidebar-expanded").css("left", "4.75em")
    })
    $(".inbox-sidebar-container").mouseout( function (){
        $("#inbox-sidebar-expanded").css("left", "-200px")
    })

// HIGHLIGHT COLOR ON HOVER FOR MENU ITEMS 
    $(".menu-option").mouseover( function (){
        var x = $(this).data("menu")

        var menu = document.querySelectorAll(`[data-menu="${x}"]`)
        for (const option of menu){
            if (!option.classList.contains("inbox-sidebar-active")){
                // if (darkMode =="enabled"){
                //     option.style.backgroundColor = "blue"
                // }else{
                    option.style.backgroundColor = "hsl(221, 52%, 85%)"
                // }
            }else{
                // if (darkMode =="enabled"){
                //     option.style.backgroundColor = "red"
                // }else{
                    option.style.backgroundColor = "hsl(219, 52%, 70%)"
                // }
            }
        }
    })

// RESET COLOR 
    $(".menu-option").mouseout( function (){
        var x = $(this).data("menu")
        var menu = document.querySelectorAll(`[data-menu="${x}"]`)

        for (const option of menu){
            if (!option.classList.contains("inbox-sidebar-active")){
                // if (darkMode == "enabled"){
                //     option.style.backgroundColor = "black"
                // }else{
                    option.style.backgroundColor = "hsl(226, 48%, 94%)"
                // }
            }else{
                // if (darkMode == "enabled"){
                //     option.style.backgroundColor = "orange"
                // }else{
                    option.style.backgroundColor = "hsl(219, 74%, 80%)"
                // }
            }
        }
    })

// GET PAGE WHEN SELECTED
    $(".inbox-action-icon, .inbox-menu-option-div").on("click", function(){
        var selected_page = $(this).data("page")
        window.location = `/ticket-easy/mail/?title=${selected_page}`;
    })

// GET NEW MESSAGE PAGE 
    $(document).on("click", "#Compose", ".Compose", function(){
        console.log("clicked")
        window.location = `/ticket-easy/mail/new`;
    })
});