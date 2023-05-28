// import Select from './select.js'
// import updatePaginationsAndSelects from './update-table.js'
import {updateSelects, removeFirstOption} from './update-selects.js'
import updateCalendar from './update-calendar.js'
import {sendTableAJAX, getWhichTable} from './update-table.js'
import {getURL, updateURL, reloadOnPop} from './url-handling.js'
// import updateSelects from './import-select.js'



$(document).ready(function(e){
console.log("tickets SELECTS script is ready")
removeFirstOption()

// CUSTOM SELECT FILTERING AND AJAX
    $(document).on("click", "body .custom-select-option", function(){
        var url_value = $(this).text();
        var select = $(this).parent().parent()
    
        var table = getWhichTable($(this), true, true)

        if (select.attr("id") == "table-ticket-priority"){
            // var searched = `with ${url_value} priority`
            var url_filter = "Priority"
            console.log("prio")
        } 
        else if (select.attr("id") == "table-ticket-categories"){
            // var searched = `for ${url_value}`
            var url_filter = "Category"
        } 
        else if (select.attr("id") == "table-ticket-assigned"){
            // var searched = url_value
            var url_filter = "Assignment"
        } 
        else if (select.attr("id") == "table-ticket-status"){
            // var searched = url_value
            var url_filter = "Status"
        }
        else if (select.attr("id") == "table-ticket-assigned"){
            // var searched = url_value
            var url_filter = "Assignment"
        }
        var page = 1
        if (url_value !== "Specific Person"){
            var url = getURL(table[0], url_filter, url_value, table[1])
            sendTableAJAX(url, table[0], table[1], false)
        }else{
            $(this).parent().parent().parent().append(`<input type="text" class="ajax-person-input theme-text" placeholder="Search for a person..." data-which_table=${table[1]}>`)
            document.querySelector(".ajax-person-input").focus();

            var person_select = $(this).closest('.custom-select-container')
            person_select.hide()

            $(document).on('blur', '.ajax-person-input', function() {
                person_select.show()
                $(this).remove();
            });
        }
    });
});