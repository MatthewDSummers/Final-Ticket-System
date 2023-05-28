
$(document).ready(function() {


$("#reply").on("click", function(){
    $(this).hide()
    $(this).next().show()
})



// THE INPUT FOR THE FORM 
var the_message_recipients = [document.getElementById("the_message_recipients").value]

// CONCERNING VALIDATION AND FUNCTIONALITY:
var active_input_count = 0
var errors = 0

$("#recipients").on("click", function(e){
                
    
    if (document.getElementById("error-no-recipients") !== null){
        document.getElementById("error-no-recipients").style.display = "none";
    }
    if (errors < 1 && active_input_count < 1){
        // SET THIS TO 1 BECAUSE AN INPUT IS ACTIVE (to prevent new ones from being created if one is present)
        active_input_count = 1 

        // CREATE DIV FOR INPUT AND ERROR 
        var new_div = document.createElement("div")
        new_div.style.display = "inline-block";

        // CREATE INPUT FOR THE USER TO ENTER THE EMAIL 
        var new_input = document.createElement("input")
        new_input.setAttribute("type", "text");
        new_input.style.display = "inline-block"
        new_input.classList.add("message-recipient-input")
        new_input.classList.add("input-validation")
        // TO MATCH THIS INPUT WITH ITS ERROR
        new_input.dataset.input_id = active_input_count

        new_error = document.createElement("span")
        new_error.classList.add("recipient-errors")
        // TO MATCH THIS ERROR SPAN WITH ITS DIV
        new_error.dataset.error_id = active_input_count
        new_error.style.display = "none";
        new_error.style.color = "red";

        // APPEND THE INPUT AND ERROR SPAN TO THE DIV 
        new_div.appendChild(new_error);
        new_div.appendChild(new_input);
        e.target.parentNode.appendChild(new_div);

        //GIVE THE INPUT FOCUS FOR THE USER TO TYPE IN
        new_input.focus()
    }


    // const the_added_input = document.querySelector(".message-recipient-input");
    // the_added_input.addEventListener('keydown', function(e) {
    //     if (e.key === 'Tab') {
    //         createIfValid(e)
    //     }
    //     if(e.key === "Enter"){
    //         createIfValid(e)
    //     }
    // });



});

const recipientContainer = document.getElementById('to');

recipientContainer.addEventListener('keydown', function(e) {
    if (e.target.classList.contains('message-recipient-input')) {
        if (e.key === 'Tab' || e.key === 'Enter') {
        createIfValid(e);
        }
    }
});

function createIfValid(e){
    active_input_count = 0;
    // PASS OR FAIL, I SET active_input_count TO ZERO. 
        // If it passes, it needs to be zero so new inputs can be created afterward;
        // If it fails, the  `if (errors < 1 && active_input_count < 1)` from above prevents new inputs anyway 



    // THE ERROR SPAN 
    var error = document.querySelector(".recipient-errors")

    // THE FORM'S INPUT 
    var current_recipient_values = document.getElementById("the_message_recipients").value.split(",")

    // THE CURRENT INPUT THE USER IS TYPING IN 
    var attempted_recipient = document.querySelector(".message-recipient-input")

    // CASE OF FAILING EMAIL VALIDATION
    const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;



    if (attempted_recipient.value == ""){
        attempted_recipient.parentNode.remove(attempted_recipient)
            // RESET ERRORS and REMOVE PREVIOUS ERROR SPAN
            error.parentNode.remove(error);
            errors = 0;
            // document.getElementById("error-no-recipients").style.display = "none";

    }
    else{
        if(!emailRegex.test(document.querySelector(".message-recipient-input").value)){
            error.innerText = "*Must be an email"
            error.style.display = "block";
            errors += 1
            attempted_recipient.focus()
    
            if (e.key === "Tab"){
                console.log("tab")
                document.querySelector(".message-recipient-input").focus()
            }
            return
        }
        // CASE OF THE CURRENTLY TYPED EMAIL BEING ALREADY PRESENT IN THE FORM'S INPUT FIELD 
        if(current_recipient_values.includes(attempted_recipient.value)){
            if (attempted_recipient.dataset.input_id === error.dataset.error_id){
                error.innerText = "*Already in Recipient List"
                error.style.display = "block";
            }
            attempted_recipient.focus()
            errors += 1;
            return
    
            // CASE OF HAVING PASSED ALL VALIDATIONS
        }else{
            // RESET ERRORS and REMOVE PREVIOUS ERROR SPAN
            error.parentNode.remove(error);
            errors = 0;

            if (document.getElementById("error-no-recipients") !== null){
                document.getElementById("error-no-recipients").style.display = "none";
            }
            // DELETE OLD RECIPIENT INPUT 
            // e.target.remove()
            // e.target.remove()
            the_value = attempted_recipient.value
            attempted_recipient.parentNode.remove(attempted_recipient)
            // CREATE THE RECIPIENT DIV 
            var new_recipient = document.createElement("div");
            new_recipient.classList.add("added-recipient");
            // new_recipient.innerText = e.target.value;
            new_recipient.innerText = attempted_recipient.value
    
            // new_recipient.style.position = 'relative';
            new_recipient.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="delete-recipient-icon"><path d="m16.192 6.344-4.243 4.242-4.242-4.242-1.414 1.414L10.535 12l-4.242 4.242 1.414 1.414 4.242-4.242 4.243 4.242 1.414-1.414L13.364 12l4.242-4.242z"/></svg>';
            document.getElementById("to").append(new_recipient)
    
            // PUSH VALUE TO FORM'S INPUT
            the_message_recipients.push(attempted_recipient.value)
            var recipientsString = the_message_recipients.join(",");
            document.getElementById("the_message_recipients").value = recipientsString;
        }
    }
}


$(document).on("click", function(e){
    // if(e.target.id == "recipients"){
    //     console.log("this is the recipient intializer")
    // }
    var dynamic_input = document.querySelector(".message-recipient-input")
    if(!e.target.classList.contains("input-validation")){
        console.log("not the baby")
        if( dynamic_input !== null){
            // if(dynamic_input.value == ""){
                
            // }
            createIfValid(e)
        }
    }
})

$('.editable').each(function(){
    this.contentEditable = true;
});

$(".editable").on("input", function(){
    // don't do this 
    // var messageBody = this.textContent;

    // do this 
    var messageBody = this.innerHTML;
    document.getElementById("the_message_body").value = messageBody;
    // console.log(document.getElementById("the_message_body").value)
});


// Initialize the first one (sender's email)
// $(".added-recipient").css('position', 'relative');
// $(".added-recipient").css('padding', '0 2em 0 0;')
// $(".added-recipient").append('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="delete-recipient-icon"><path d="m16.192 6.344-4.243 4.242-4.242-4.242-1.414 1.414L10.535 12l-4.242 4.242 1.414 1.414 4.242-4.242 4.243 4.242 1.414-1.414L13.364 12l4.242-4.242z"/></svg>');


// Removing from the form's input
    $(document).on("click", ".delete-recipient-icon", function(){

        var current_recipient_values = document.getElementById("the_message_recipients").value.split(",")
        var index = current_recipient_values.indexOf($(this).parent().text().trim());
        if (index > -1) {
            console.log(the_message_recipients, "message recipient array")

            current_recipient_values.splice(index, 1);
            var recipientsString = current_recipient_values.join(",");
            document.getElementById("the_message_recipients").value = recipientsString;
            the_message_recipients =[recipientsString]
            console.log(the_message_recipients, "message recipient array")
        }
        console.log(document.getElementById("the_message_recipients").value, "removing value")
        $(this).parent().remove()

    })


    $(document).on("click", "#Compose", ".Compose", function(){

        console.log("clicked")
        window.location = `/ticket-easy/mail/new`;

    })

// $(document).on("click", ".arrow-container, .arrow-down", function(e){

//     if(!$(this).hasClass("arrow-down")){
//         $(this).next().toggle()
//         console.log("the DIV triggered it")
//     }else{
//         $(this).parent().next().toggle()
//         console.log("the arrow triggered it")
//     }

// });
// $(document).on("click", function(e) {
//     if (!$(e.target).is(".arrow-container") && !$(e.target).closest(".message-details-div").length) {
//         $(".message-details-div").hide();
//     }
// });

$(document).on("click", function(e) {
    if (!$(e.target).closest(".message-container").length) {
        $(".message-details-div").hide();
    }
});

$(document).on("click", ".arrow-container, .arrow-down", function(e){
    e.stopPropagation();
    var nearest_info_div = $(this).closest(".message-container").find(".message-details-div")
    nearest_info_div.toggle();
    $(".message-details-div").not(nearest_info_div).hide()
});


// RETRIEVE THE VALUE OF THE MESSAGE BODY IF VALIDATION FAILS 
//  and set it to be the visible message body's text content
    var visible_body = $('.editable');
    var hidden_input_body = $("#the_message_body");
    var retrieved_body = $('#retrieved_body');
    if (retrieved_body.length) {  // check if #retrieved_body element exists
        hidden_input_body.val(retrieved_body.text().trim());
        visible_body.text(retrieved_body.text().trim());
    }


// SHOW FULL PAGE TITLE 
    $("#email-title").on("mouseenter", function(){
        $("#full-title").fadeIn(500)
    })
    $("#email-title").on("mouseleave", function(e){
        // if(!$(e.target).is("#full-title")){
            $("#full-title").fadeOut(500)
        // }
    })



var form_subject_errors = 0;
var form_body_errors = 0;
var message_form_recipients_error = 0;
// THE EMAIL / REPLY FORM
    $(document).on("click", "#send-email", function(e){
        e.preventDefault()
        var new_message_form_recipients_input = document.querySelector(".new-message-form-recipients");

        var subject = document.getElementById("the_message_subject")
        // var no_subject_error = document.getElementById("error-no-subject");

        var body = document.getElementById("the_message_body")
        var no_body_error = document.getElementById("error-no-body");
        console.log("we did it")

        if (body.value == ""){
            no_body_error.style.display = "block";
            form_body_errors = 1;
        }else{
            form_body_errors = 0;
        }


        // NEW MESSAGE PAGE ONLY 
        if (subject !== null){
            if (subject.value == ""){
                // no_subject_error.style.display = "inline-block";
                subject.placeholder = "*Please add a subject"
                subject.classList.add("invalid");
                form_subject_errors = 1;
            }else{
                form_subject_errors = 0;
                subject.placeholder = "Subject"
                subject.classList.remove("invalid");
            }
        }

        // NEW MESSAGE PAGE 
        if (new_message_form_recipients_input !== null){
                if ( new_message_form_recipients_input.value == "" ){
                    message_form_recipients_error = 1;
                    document.getElementById("error-no-recipients").style.display = "inline-block";

                    var dynamic_recipient_input = document.querySelector(".message-recipient-input")
                    // Focus the recipient input if it exists 
                    if (dynamic_recipient_input !== null){
                        dynamic_recipient_input.focus()
                    }
                }else{
                    message_form_recipients_error = 0;
                }
            }

        // SEND IF NO ERRORS
        if (form_body_errors < 1 && form_subject_errors < 1 && message_form_recipients_error < 1){
            document.getElementById("message-form").submit();
        }
    })

    $(".editable").on("input click", function(){
        if (document.getElementById("error-no-body").style.display == "block"){
            document.getElementById("error-no-body").style.display = "none";
        }
    });

});




