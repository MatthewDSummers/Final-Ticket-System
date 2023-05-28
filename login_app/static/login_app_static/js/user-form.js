$(document).ready(function(){

// user level change checkboxes
    $("#super-admin-check").on("click", function(){
        console.log("clicked")
        $("#admin-check").prop("checked", false);
        $("#admin-check").toggleClass("hidden");
        $("#admin-check-label").toggleClass("hidden");
    });

    $("#admin-check").on("click", function(){
        console.log("clicked")

        if ($("#super-admin-check").length > 0){
            $("#super-admin-check").prop("checked", false);
            $("#super-admin-check").toggleClass("hidden");
            $("#super-admin-check-label").toggleClass("hidden");
        }
    });

// For some reason, autocomplete="off" wasn't working to prevent the saved email/password from populating 
// (in seemingly, brutally random inputs)
// so I did this to counter it.
    function enableInput(inputs) {
        function removeReadOnly() {
            for (const input of inputs){
                input.removeAttribute("readonly");
            }
        }

        for (const input of inputs){
            input.addEventListener("click", removeReadOnly);
            input.addEventListener("focus", removeReadOnly);
        }
    }

    enableInput(document.querySelectorAll(".user-form-input"))


const EMAIL_REGEX = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

// USER FORM SUBMIT
var flag = 0;
    $("#user-form-submit").on("click", function(e){
        e.preventDefault();
        document.getElementById("email-error-regex").style.display = "none";
        document.getElementById("confirm-password-error-not-match").style.display = "none";

        flag = 0;

        // required fields empty error 
        for (const input of document.querySelectorAll(".required")){
            if(input.value == ""){
                console.log("whoa whoa whoa ")
                document.getElementById(`${input.id}-error`).style.display = "block";
                flag += 1;
            }else{
                document.getElementById(`${input.id}-error`).style.display = "none";
            }
        }

        // regex error if not empty input
        if (document.getElementById("email").value !== ""){
            if(!EMAIL_REGEX.test(document.getElementById("email").value)){
                document.getElementById("email-error-regex").style.display = "block";
                flag += 1;
            }else{
                document.getElementById("email-error-regex").style.display = "none";
            }
        }

        // if password and confirm password fields have a value, they must match 
        var password = document.getElementById("new-password").value;
        var confirmPassword = document.getElementById("confirm-password").value;

        if (password !== confirmPassword) {
            document.getElementById("confirm-password-error-not-match").style.display = "block";
            flag += 1;
        } else {
            document.getElementById("confirm-password-error-not-match").style.display = "none";
        }

        if (flag == 0){
            $("#user-form").submit()
        }
    })

// hide confirm-password-not-match error if password == confirm password 
    $("#confirm-password, #new-password").on("input", function() {
        var confirm_pw = $("#confirm-password").val();
        var pw = $("#new-password").val();
        if (pw === confirm_pw) {
            $("#confirm-password-error-not-match").hide();
        }
    });


// Hide input errors on input 
    $(".user-form-input").on("input", function(){
        $(`#${$(this).attr("id")}-error`).hide()
    })

// Hide email REGEX error if the input matches regex 
    $("#email").on("input", function(){
        if(EMAIL_REGEX.test($(this).val())){
            $("#email-error-regex").hide()
        }
    })

// toggle the change password div  (and reset password fields + hide errors, if user hides the div again)
    // (and check/uncheck password checkbox for user manager validator )
    $(document).on("click", ".dropdown-trigger", function(){
        var dropdown = $(this).next()
        var arrow = $(this).find('.arrow');
        arrow.removeClass("up")

        if( dropdown.css("display") == 'none'){
            dropdown.show()
            arrow.addClass("up")
            $("#password-checkbox").prop("disabled", false)
            $("#password-checkbox").prop("checked", true)
        }else{
            dropdown.hide()
            $("#new-password, #confirm-password").val("");
            $("#confirm-password-error-not-match, #confirm-password-error").hide()
            $("#password-checkbox").prop("disabled", true)
            $("#password-checkbox").prop("checked", false)

        }
    });

})


// REGEX EXPLANATION
// const EMAIL_REGEX = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

// ^ and $: Match the start and end of the string, respectively, ensuring the pattern matches the entire string.

// [a-zA-Z0-9.+_-] and \w: Match alphanumeric characters, plus the characters +, ., _, and -.

// [\.-]?: Match an optional dot or hyphen.

// \w+: Match one or more alphanumeric characters.

// ([\.-]?\w+)*: Match zero or more occurrences of an optional dot or hyphen followed by one or more alphanumeric characters.

// @: Match the @ symbol.

// (\.\w{2,3})+: Match one or more occurrences of a dot followed by two or three alphanumeric characters (to represent the top-level domain).

// *: Match zero or more occurrences of the preceding pattern.