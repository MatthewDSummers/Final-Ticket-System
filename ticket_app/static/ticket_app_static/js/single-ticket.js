// DROPDOWN TRIGGERS 
$(document).ready(function(){
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

// CUSTOM SELECTS FOR FORMS
    $(document).on("click", ".custom-select-option", function(){
        var custom_select = $(this).parent().parent()
        var option_selected = $(this).data("value")
        var form = $(this).closest('form')
        var ticket_id =  form.find('[data-ticket]').data("ticket");

        if (option_selected !== "none"){
            if (custom_select.hasClass("assignment-form-custom-select")){
                form.attr("action", "/ticket-easy/assignment")
                form.attr("action", `${form.attr("action")}/${ticket_id}/${option_selected}`)

            } else if(custom_select.hasClass("priority-form-custom-select")){
                form.attr("action", "/ticket-easy/priority")
                form.attr("action", `${form.attr("action")}/${ticket_id}/${option_selected}`)
                form.submit()
            }
        }
    });

// ASSIGNMENT FORM 
    $(document).on("click", ".admin-form-button", function(e){
        e.preventDefault()
        var form = $(this).closest('form')
        if (form.attr("action") == ""){
            console.log("no action")
        }else{
            form.submit()
        }
    });
});