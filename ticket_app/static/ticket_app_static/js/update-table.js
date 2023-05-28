import updateCalendar from './update-calendar.js'
import {updateSelects, removeFirstOption} from './update-selects.js'
import {getURL, updateURL, reloadOnPop} from './url-handling.js'
import { replacePlaceholder } from './all-tickets.js'

export function getWhichTable(target_element, table_is_present=true , from_custom_select=false){
    // console.log(table_is_present, "is table present?")
    // console.log(target_element, "target element")
    if(from_custom_select){
        var table_variant = target_element.parent().parent().next().data("table_variant")
        // console.log(table_variant, "getting the TABLE VAR from getWhichTable")

    }else{
        console.log("THERE IS NO CUSTOM SELECT INVOLVED")
        var table_variant = target_element.data("which_table")
        // console.log(table_variant, "xxxxxxxxx   the table variant from getWhichTable")
    }

    if(!table_is_present){
        var table_type = target_element.data("page")
        // console.log("table not present")
    }
    else{
        var type_parent = target_element.closest('div[data-table="' + table_variant + '"]');
        var table_type = type_parent.data("page")
        // console.log(table_type, "table is present -  and the Type is this")
    }

    return [table_type, table_variant]
}

export function sendTableAJAX(url, table_type, table_variant, refresh=true){
    // console.log(table_type, "the table TYPE from sendTableAJAX")
    // console.log(table_variant, "the table VARIANT from sendTableAJAX")

    if (refresh == true){
        var data = {'ajax': 'ajax'}
    }else{
        var data = {'ajax': 'ajax', 'not_main_page':'nope'}
    }

    $.ajax({
        method: 'GET',
        url: url,
        data: data,
        success:function(response){
            // console.log($('.table-body[data-table="' + table_variant + '"][data-page="' + table_type + '"]').data('table'), "THIS IS THE TABLE ATTR OF THE DIV")
            // console.log($('.table-body[data-table="' + table_variant + '"][data-page="' + table_type + '"]').data('page'), "THIS IS THE PAGE ATTRIBUTE OF THE DIV")
            $('.table-body[data-table="' + table_variant + '"][data-page="' + table_type+ '"]').html(response);
            updateCalendar("#table-ticket-date")
            updateSelects()
            removeFirstOption()
            updateURL(url)
            replacePlaceholder($(".table-ticket-description, .table-ticket-id"));
        }
    });
}
export function sendPOSTtableAJAX(url, ticket_context_url, table_type, table_variant, method){

    var data = {
        "ajax": "ajax", 
        "not_main_page":"nope",
        // "csrf_token": "{{csrf_token}}",
        "ticket_context_url": ticket_context_url,
        "method": method
    }

    $.ajax({
        method: 'POST',
        url: url,
        data: data,
        success:function(response){
            $('.table-body[data-table="' + table_variant + '"][data-page="' + table_type+ '"]').html(response);

            updateCalendar("#table-ticket-date")
            updateSelects()
            removeFirstOption()
            updateURL(ticket_context_url)
            replacePlaceholder($(".table-ticket-description, .table-ticket-id"));
        }
    });
}


$(document).ready(function(){

// Table Reset Button
        $("body").on("click", ".reset-table", function(e){
            e.preventDefault();
            var table = getWhichTable($(this), true, false)
            var url = getURL(table[0], null, null, table[1])
            sendTableAJAX(url, table[0], table[1], true)
        })

// Pagination AJAX
        $(document).on("click", ".paginate-command, .pagination-a", function(event){
            event.preventDefault();
            var url = $(this).attr("href")
            var table = getWhichTable($(this), true, false)
            // console.log(table[0], " <-----  is the table TYPE within PAGINATION COMMAND")
            // console.log(table[1], " <-----  is the table VARIANT within PAGINATION COMMAND")
            sendTableAJAX(url, table[0], table[1], false)
        })

        // AJAX button FOR DISPLAYING DIFFERENT TABLE TYPES 
    $("body").on("click", ".new-table-button", function(e){
        var table = getWhichTable($(this), false, false)

        if (table[0] == "Sent"){
            document.getElementById("table-sent").setAttribute('data-page', table[0])
            document.getElementById("table-sent").setAttribute('data-table', table[1])
        }else if(table[0] == "Assigned"){
            document.getElementById("table-assigned").setAttribute('data-page', table[0])
            document.getElementById("table-assigned").setAttribute('data-table', table[1])
        }

        var url = getURL(table[0], null, null, table[1])
        // console.log(url, " < ----  NEW TABLE BUTTON URL")
        sendTableAJAX(url, table[0], table[1], true);
    });

// ACTIONS
    // pin/unpin/archive/delete
    $(document).on("submit", ".ticket-actions", function(e){
        e.preventDefault()
        var variant = $(this).data("which_table")
        var type = $(this).data("page")
        var url = $(this).attr("action")

        var method = $(this).find(".which_action").val()
        var ticket_context_url = $(this).find(".url").val()

        console.log(ticket_context_url, "ticket context")
        if ($(this).hasClass("delete-ticket")){
            var result = confirm("Delete ticket forever? This action cannot be undone.");
             // allow or prevent form submission based on the result of the confirm dialog
            if (result == true){
                sendPOSTtableAJAX(url, ticket_context_url, type, variant, method)
            }else{
                return false
            }
        }else{
            sendPOSTtableAJAX(url, ticket_context_url, type, variant, method)
        }
    })

})

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