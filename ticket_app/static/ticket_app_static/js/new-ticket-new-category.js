$(document).ready(function(){
    $(document).on("click", ".custom-select-option", function(){
        var the_select = $(this).parent().parent();
        var select_id = the_select.attr('id');
        $('input[data-delegate="' + select_id + '"]').val($(this).data("value"));
    })


// DELETE CATEGORY FORM 
    var flag = 0;
    $(document).on("submit", "#delete-category-form", function(e){

        // when the page reloads, it sets it back to 0 so the confirmations work again 
        if(flag === 0){
            e.preventDefault();
            var result = confirm("Delete this category forever? This action cannot be undone. \nAny tickets associated with this category will also be permanently deleted!");

            if (result == true){
                var final_confirmation = confirm("Are you absolutely certain you want to delete this category? \nAny tickets associated with this category will also be permanently deleted!");
                if (final_confirmation == true){
                    flag = 1;
                    $(this).submit();
                }else{
                    flag = 0;
                    return result;
                }
            }else{
                flag = 0;
                return result;
            }
        }else if(flag === 1){
            flag = "send it";
            $(this).submit()
        }
    });
})

