import Select from './select.js'

$(document).ready(function(){

// model validator needs this checkbox
var checkbox = document.getElementById("checkbox-then")
if (checkbox !== null){
    checkbox.checked = true;
}

const selectElements = document.querySelectorAll('[data-select]')

selectElements.forEach(selectElement => {
// make new custom select 
    new Select(selectElement)
// delete old select 
    selectElement.remove()
})


$("body").on('click',".custom-select-option", function(e) {
    var the_custom_select = e.currentTarget.parentElement.parentElement
    var the_custom_select_parent_div = e.currentTarget.parentElement.parentElement.parentElement

    // CUSTOM SELECTS 
    var supportive_select = document.getElementById(`${the_custom_select.id}_supportive`)

    // Example: if `then_supportive` custom select is the target, this checks for `then_supportive_additional`
    var intermediate_supportive_select = document.getElementById(`${the_custom_select.id}_additional`)

    var additional_supportive_select = document.getElementById(`${the_custom_select.id}_supportive_additional`)

    // TO UPDATE INPUTS, I SET OPTIONSELECTED FIRST AS THE ACTUAL OPTION SELECTED
    var realOption = e.target.dataset.value 

    if (realOption !== "Select an Option..." && realOption !== ""){
        $(`#${the_custom_select.id}_input`).val(realOption);
    }
    // $(`#${the_custom_select.id}_input`).val(realOption);

    // FOR THE AJAX, I SET IT TO "SEND_CAN" TO GET CORRECT SUB-MENU SELECT 
    if (the_custom_select.classList.contains("make-canned-supportive")){
        var optionSelected = "send_can";

        // because setting it to "send_can" populates (or re-populates) the User select for canned messages,
        // i reset that input for its User ID straightaway since they have to choose again 
        document.getElementById("then_supportive_additional_input").value = "";
    }else{
        var optionSelected = e.target.dataset.value 
    }

    if (the_custom_select.id == "and-or"){
        $(".add-condition").hide()
    }

// GET DATA FROM PYTHON
    if (optionSelected !== "Select an Option..."){


    // RESET THE SELECTED OPTION SPAN'S COLOR (IN CASE IT WAS ERROR COLOR)
    $(this).parent().prev().attr("style", "color: var(--clr-dark) !important")

    // ONLY ALLOW ONE SUB-DROPDOWN 

            // if we have supportive selects ... 
            if (supportive_select !== null) {

                // Only allow one supportive select
                supportive_select.parentNode.removeChild(supportive_select);
            }

            // Example: if `then_supportive` custom select is the target, this checks for `then_supportive_additional`
            if (intermediate_supportive_select !== null){
                intermediate_supportive_select.parentNode.removeChild(intermediate_supportive_select);
            }


            // if we have additional supportive selects ... 
            if (additional_supportive_select !== null) {
                additional_supportive_select.parentNode.removeChild(additional_supportive_select);
            }


        $.ajax({
            method: 'GET',
            url: '/ticket-easy/get-info',
            data: {
                "option":optionSelected
            },
            success:function(response){

                var response_string = JSON.stringify(response);

                var then_supportive = document.getElementById("then_supportive")
                var then_supportive_additional = document.getElementById("then_supportive_additional")
                var then_div = document.getElementById("then-div")

                console.log(response_string, " THE STRINNNNNGG")
                if (response_string === '{"options":{}}') {
                    console.log("it's empty");

                    if (then_div.style.display === "block") {

                        // IF THERE IS A SUPPLEMENTAL SELECT 
                        if(then_supportive !== null){
                            var then_supportive_option = then_supportive.querySelector(".custom-select-option.selected");
    
                            if (then_supportive_additional == null){
                                if (then_supportive_option.dataset.value !== "Select an Option...") {
                                    $(".submit-bot").show();
                                }
                            }else if(then_supportive_additional !== null){
                                var addition_option = then_supportive_additional.querySelector(".custom-select-option.selected");
                                if (then_supportive_option.dataset.value !== "Select an Option..." && addition_option.dataset.value !== "Select an Option...") {
                                    $(".submit-bot").show();
                                }
                            }
                        }else{
                            // IT'S EMPTY, AND THERE ARE NO ADDITIONAL `THEN` SELECTS TO CHOOSE FROM
                            $(".submit-bot").show();
                        }
                    }
                }else{
            // IT'S NOT EMPTY . . . (THERE WILL BE AN ADDITIONAL SELECT TO CHOOSE FROM )
                    // $(".submit-bot").hide();
            // else, let's make some new selects 
                    const select = document.createElement("SELECT");
                    var option = document.createElement("option")
                    option.text = "Select an Option..."
                    select.add(option)
                    let send_can = false;

                    for (const key in response.options) {
                        if (response.options.hasOwnProperty(key)) {


                            if (key !== "send_can"){
                                const value = response.options[key];

                                // Create a new option element
                                const option = document.createElement('option');
                                option.value = value;
                                option.text = key;
        
                                // Append the option to the HTML select menu
                                // Replace 'custom-select' with the actual class name of your custom select menu
                                select.add(option);
                            }

                            if (key === 'send_can') {
                                send_can = true;
                            }

                        }
                    }

                // configure select 
                    if(send_can == true){
                        select.classList.add("make-canned-supportive")
                    }

                    // if (the_custom_select.hasClass("make-canned-supportive")){
                    if (the_custom_select.classList.contains("make-canned-supportive")){
                        select.id = `${the_custom_select.id}_additional`
                        select.classList.add(`${the_custom_select.id}_additional`)
                    }else{
                        select.id = `${the_custom_select.id}_supportive`
                        select.classList.add(`${the_custom_select.id}_supportive`)
                    }

                // append selected to desired div

                if (!(response.hasOwnProperty('options') && Object.keys(response.options).length === 0)) {

                    // }else{
                        the_custom_select_parent_div.append(select)
                        // make it a custom select 
                        new Select(select)
                        select.remove()

                        // the Select is a class I made which emulates an HTML element select. 
                    }
                }
            }
        }); 

    }
});


// $( document ).ready(function() {

    $("#bot-name-input").blur(function(e){
        if ( $(this).val() != "" ){
            var title = $("#bot-name-input").val()
            $("#title").text(title)
            $(".bot-container").show()
            var bot_name = document.querySelector(".bot-name-input-div")
            bot_name.style.borderRadius = "10px 10px 0px 0px";
            // $(".bot-container").show()
            $("#bot-name-real").val(title)
        }
    });

    $("#bot-name-input").on('keypress',function(e) {
        if(e.which == 13) {
            if ( $(this).val() != "" ){
                var title = $("#bot-name-input").val()
                $("#title").text(title)
                // $("#bot-name-real").val(title)
                console.log(title,"title")
                $("#bot-name-real").val(title)
                $(".bot-container").show()
            }
            var bot_name = document.querySelector(".bot-name-input-div")
            bot_name.style.borderRadius = "10px 10px 0px 0px";
        }
    });


// `WHEN` CUSTOM SELECT CLICK LISTENER 
    $('#when').on('click', function (e) {
        if ($("#condition-one-div").css("display") !== "block")
            if ($("#condition-or-div").css("display") !== "block" || $("#condition-inclusive-div").css("display") !== "block" ){
                $(".add-condition").show()
            }

        if ($("#then-div").css("display") !== "block"){
            $(".add-action").show()
        }


    });



// var condition_counter = 0
// REMOVE CONDITION 
    $(".remove-condition").on("click", function(e){
        // REDUCE COUNTER
        // condition_counter -= 1;

        // HIDE THE PARENT DIV 
        var parent_div = $(this).parent()
        parent_div.css("display", "none")

        // Show the condition trigger
        $(".add-condition").show()

        // GET THE PRIMARY CUSTOM SELECT
        var primary_custom_select = $(this).next();
        var the_id = primary_custom_select.attr("id");

        // Remove 'selected' class from all options
        primary_custom_select.find('.custom-select-option').removeClass('selected');

        // Add 'selected' class to the first option
        primary_custom_select.find('.custom-select-option:first-child').addClass('selected');

        // Reset the displayed option
        primary_custom_select.find('.custom-select-value').text("Select an Option...");

        // GET SUPPORTIVE SELECTS 
        var supportive_select = primary_custom_select.siblings(`#${the_id}_supportive`)
        var additional_supportive_select = primary_custom_select.siblings(`#${the_id}_supportive_additional`)

        // GET CUSTOM SELECT INPUTS
        var base_input = $(`#${the_id}_input`);
        var supportive_select_input = $(`#${the_id}_supportive_input`);
        var additional_supportive_select_input = $(`#${the_id}_supportive_additional_input`);

        // RESET INPUT VALUES  
            // (Although I only collect the data for the input values directly before the form submission, I reset them here anyway
            // in case the user tried to submit the form, it didn't pass validation, and they went back and edited the form and removed a condition)
        base_input.val("");

        // FOR CONDITIONS WITH MORE THAN ONE SELECT
        if (supportive_select.length > 0){
            //Reset input values
            supportive_select_input.val("");
            // Remove the supportive custom select 
            supportive_select.remove()
        }

        // FOR THINGS THAT HAVE AN EXTRA SELECT (CANNED RESPONSE RECIPIENT)
        if (additional_supportive_select.length > 0){
            // Reset input values 
            additional_supportive_select_input.val("");
            // Remove the additional custom select
            additional_supportive_select.remove()
        }

    // MAKE THE RELEVANT PLUS SIGN ICON VISIBLE AGAIN
        var which_option = $(this).data("reset-condition-option")
        document.querySelector(`.${which_option}`).style.display = "block";

    // IN THE EVENT OF THE USER GETTING RID OF THE "AND" or "OR" CONDITIONS
        if ($(this).data("condition-tracker") == "additional-conditional"){
            // Show the "IF" option's Remove trigger again
            $("[data-condition-tracker=if]").show()
        }


        var checkbox = $(this).data("checkbox")
        $(`#${checkbox}`).prop('checked', false);

    // IN THE EVENT OF THE USER GETTING RID OF THE `THEN` CONDITION
        if ($(this).data("condition-tracker") == "then-div"){
            // Hide form submission button
            $(".submit-bot").hide();
            // Show "Add action" trigger
            $(".add-action").show();
        }
    });


// ADD CONDITION 
    $(".add-condition-trigger-new").click(function(){
        // document.getElementById("condition-1").checked = true;

        var condition_or_div = document.getElementById("condition-or-div")
        var condition_inclusive_div = document.getElementById("condition-inclusive-div")

        var and_or_selection = document.querySelector(".and-or-select")

        if($("#condition-one-div").css("display")=="block"){

            // CHANGE COUNTER TO  `2` TO ALLOW FOR "AND.. + OR" / "OR.. + AND "
            // if (condition_counter < 2){

            if (and_or_selection == null){
                if (condition_or_div.style.display == "none" && condition_inclusive_div.style.display == "none"){
                // condition_counter += 1;

                condition_or_div.style.position = "relative"
                condition_inclusive_div.style.position = "relative"


            // AND/OR SELECT CREATION
                var select = document.createElement("SELECT");
                select.id = "and-or"
                select.classList.add("and-or-select")
                const opt1 = document.createElement("option");
                const opt2 = document.createElement("option");
                const opt3 = document.createElement("option");

                //opt1.value = "2";
                opt1.text = "And / Or ... ";
                opt1.selected ="true"
                opt1.disabled ="true"

                //opt2.value = "AND";
                opt2.text = "And...";

                //opt3.value = "OR";
                opt3.text = "Or...";

                select.add(opt1)
                select.add(opt2)
                select.add(opt3)

                var and_or_div = document.getElementById("and_or_div")
                and_or_div.style.position = "relative"

                and_or_div.append(select)
                new Select(select)

                and_or_div.style.display = "block"

                $("[data-condition-tracker=if]").hide()
                }

            }
            // }
        }
        else if($("#condition-one-div").css("display")=="none"){
            $("#condition-one-div").show()
            document.getElementById("condition-one-div").style.position = "relative"
            document.getElementById("checkbox-if").checked = true;

        }
    });

    // THE `ADD ACTION` TRIGGER CLICK LISTENER  
    $(".add-action").click(function(){
        var then_div = document.getElementById("then-div")
        then_div.style.display = "block";
        then_div.style.position = "relative";
        $(this).hide();
        // document.getElementById("checkbox-then").checked = true;
    });


// SHOW AND... / OR... DIVS 
    $(document).on('click', '.and-or-select > .custom-select-options li', function() {

        // if($("#condition-inclusive-div").css("display") == "block" || $("#condition-or-div").css("display") == "block"){
        //     $("#add-condition").hide();
        // }


        var option = $(this).text();
        if (option != "And / Or ...") {
            if (option == "And...") {
                $("#condition-inclusive-div").show();
                $("#add-condition").hide();
                document.getElementById("checkbox-and").checked = true;
            } else {
                $("#condition-or-div").show();
                $("#add-condition").hide();
                document.getElementById("checkbox-or").checked = true;
            }
            $(".and-or-select").remove();
            console.log(document.querySelector(".and-or-select"), "IS IT NULL??")
        }
    });
// });
// var form_flag = false;

// function validateForm(){

//     $(document).find(".custom-select-container").each(function() {
//         if (!$(this).hasClass("and-or-select")) {
//             const selectValue = $(this).find(".custom-select-value").text();
//             // SET ERRORS 
//             if (selectValue == "Select an Option...") {
//                 if ($(this).parent().css("display") === "block") {
//                     form_flag = true;
//                     var option = $(this).find(".custom-select-value")
//                     option.text("*Please select a value")
//                     option.attr("style", "color: var(--clr-error) !important")
//                 }
//             }
//         }

//         if(form_flag){
//             validateForm()
//         }
//         return form_flag
//     });

// }
// // $(document).ready(function(){
//     $(document).on("click", ".submit-bot", function(e){
//         e.preventDefault();
//         // $(document).find(".custom-select-container").each(function() {
//         //     if (!$(this).hasClass("and-or-select")) {
//         //         const selectValue = $(this).find(".custom-select-value").text();
//         //         // SET ERRORS 
//         //         if (selectValue == "Select an Option...") {
//         //             if ($(this).parent().css("display") === "block") {
//         //                 form_flag = true;
//         //                 var option = $(this).find(".custom-select-value")
//         //                 option.text("*Please select a value")
//         //                 option.attr("style", "color: var(--clr-error) !important")
//         //             }
                    
                    
//         //             // else{
//         //             //     // form_flag = false; DANG IT 
//         //             //     var the_id = $(this).attr("id")
//         //             //     if ( $(`#${the_id}_input`).val() !== ""){
//         //             //         form_flag = false;
//         //             //     }
//         //             // }
//         //         }
//         //     }
//         // });
//         var form_flag = validateForm()
//         // if (!form_flag){
//         if (form_flag == false){
//             $("#new-automator-form").submit();
//         }
//     })










// var form_flag = false;

// function validateForm() {
//     // var form_flag = false;

//     $(document).find(".custom-select-container").each(function() {
//         if (!$(this).hasClass("and-or-select")) {
//             const selectValue = $(this).find(".custom-select-value").text();
//             // SET ERRORS 
//             // if (selectValue === "Select an Option...") {
//                 if ($(this).parent().css("display") === "block") {
//                     if (selectValue === "Select an Option...") {
//                         form_flag = true;
//                         var option = $(this).find(".custom-select-value");
//                         option.text("*Please select a value");
//                         option.attr("style", "color: var(--clr-error) !important");
//                     }else{
//                         form_flag = false;
//                     }
//                 }
//             }
//         // }
//     });

//     return form_flag;
// }

    function validateBotForm() {
        var form_flag = false; // Initialize form_flag to false

        $(document).find(".custom-select-container").each(function() {
            if (!$(this).hasClass("and-or-select")) {
                let selectValue = $(this).find(".custom-select-value").text();

                if ($(this).parent().css("display") === "block") {
                    if (selectValue === "Select an Option..." || selectValue === "*Please select a value") {
                        form_flag = true;
                        let option = $(this).find(".custom-select-value");
                        option.text("*Please select a value");
                        option.attr("style", "color: var(--clr-error) !important");
                    }
                }
            }
        });

        return form_flag;
    }


    $(document).on("click", ".submit-bot", function(e) {
        e.preventDefault();
        var form_flag = validateBotForm();
        if (!form_flag) {
            $("#new-automator-form").submit();
        }
    });

})


// $(".submit-bot").click(function(){
//     // # I'LL ACTUALLY USE THE .FORM FUNCTION ABOVE WHEN I MAKE THIS A submit button INSTEAD Of a regular button. 



















// CKEDITOR NECESSARY 

// var message_body = document.querySelector("[data-type='ckeditortype']")
// message_body.setAttribute("name", "body")
// // THE ABOVE DOESN'T WORK FOR INBOX (ONLY FOR CAN CREATION PAGE. BLAME AJAX)
// $('label[for="id_body"]').hide();




// ALTERNATIVE IDEAS FOR CONFIG 
// console.log(message_body.dataset.config)

// var configs = JSON.parse(message_body.dataset.config)
// Object.keys(configs).forEach(value => {
//     // console.log(configs[value] = "s");
//     if (configs[value] == "835"){
//         configs[value] = "650"
//     }
// })
// message_body.dataset.config = JSON.stringify(configs)












// var actual_body = document.querySelector("#cke_1_contents")
// actual_body.style.backgroundColor = "blue"
// document.querySelector("#cke_1_contents").style.backgroundColor = "red"
// // console.log(message_body.dataset.config, "Data")
// document.querySelector("#cke_id_body > div").style.backgroundColor ="blue"
// document.querySelector("#content-1 > form > div.django-ckeditor-widget").style.backgroundColor ="blue"
// document.querySelector("#cke_id_body").style.width = "10000px"



// document.querySelector("#cke_1_top")
// TOOLBAR 