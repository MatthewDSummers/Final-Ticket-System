
$(document).ready(function(){
    const checkboxes = document.querySelectorAll('.admin-checkbox');
    $('.initialize-disabled').attr("disabled", true); // initialze the user permission form's button as disabled
    
// CHECKBOX HANDLING FOR ADMIN FORM 
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            checkboxes.forEach(otherCheckbox => {
                if (otherCheckbox !== checkbox) {
                    otherCheckbox.disabled = checkbox.checked;
                    // effectively, this is "disabled = true"
                }
            });

            var button = checkbox.parentNode.querySelector("button[type='submit']");
            if (checkbox.checked) {
                button.textContent = checkbox.value;
                $('.initialize-disabled').attr("disabled", false); //enable form submission button it if checked
            } else {
            button.textContent = "Change User Permission Levels";
            $('.initialize-disabled').attr("disabled", true); // disable it if unchecked
            }
        });
    });

// ARROW ANIMATIONS 
    $(document).on("click", ".ticket-assignment-dropdown-trigger", function(){
        var dropdown = $(this).next()
        var arrow = $(this).find('.table-arrow');

        arrow.removeClass("table-up")


        if( dropdown.css("display") == 'none'){
            dropdown.show()
            arrow.addClass("table-up")
        }else{
            dropdown.hide()
        }
    });

// CHOOSING TO DELETE ACCOUNT
    $(document).on("click", "#delete-account", function(){
        var result = confirm("Delete account? You will be prompted to give your password, if you click OK.");
        if (result == true){
            $(this).hide()
            $("#delete-the-account-div").show();
        }else{
            return result;
        }
    });

// HIDING THE FORM 
    function hideDeleteForm(){
        $("#delete-the-account-div").hide();
        $("#delete-account").show();
        $("#password").val("");
        $("#pw-error").hide();
    }

// KEEPING ACCOUNT 
    $(document).on("click", "#keep-the-account-div", function(){
        hideDeleteForm()
    });

// HIDE PASSWORD ERROR UPON INPUT
    $(document).on("input", "#password", function(e){
        $("#pw-error").hide();
    });

// DELETE THE ACCOUNT FORM SUBMISSION HANDLING
    $("#delete-account-form").on("submit", function(e){
        e.preventDefault();
        if (form_submitted == true){
            return;
        }else{
            var result = confirm("Last chance! Delete the account forever? This action cannot be undone!");

            if (result == true){
                console.log("true")

                $(this).off('submit')
                if($("#password").val() == ""){
                    $("#pw-error").show()
                }else{
                    var target_id = $(this).data("target")
                    $(this).attr("action", `/ticket-easy/users/delete/${target_id}`)
                    var form_submitted = true;
                    $(this).submit();
                }
            }else{
                hideDeleteForm()
                return false;
            }
        }
    });
});