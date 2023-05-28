
// import Select from './select.js'
// import updatePaginationsAndSelects from './update-table.js'
import updateCalendar from './update-calendar.js'
import {updateSelects, removeFirstOption} from './update-selects.js'
import {getURL, updateURL, reloadOnPop} from './url-handling.js'
import { getWhichTable, sendTableAJAX } from './update-table.js';
// import updatePaginationsAndSelects from './update-table.js'


// ID # AND DESCRIPTION PLACEHOLDER UPDATE
export function replacePlaceholder(elements){
    var placeholders = {};

    elements.each(function() {
        let placeholder = $(this).attr("placeholder");
        let input = $(this).data("which_input");
        let table = $(this).data("which_table");
        let key = `${table}-${input}`;

        placeholders[key] = placeholder;

        $(document).on("focus", `[data-which_input="${input}"][data-which_table="${table}"]`, function(){
            $(this).removeAttr("placeholder");
        });

        $(document).on("blur", `[data-which_input="${input}"][data-which_table="${table}"]`, function(){
            let key = `${$(this).data("which_table")}-${$(this).data("which_input")}`;
            $(this).attr('placeholder', placeholders[key]);
        });
    });
}

replacePlaceholder($(".table-ticket-description, .table-ticket-id"));

$(document).ready(function(e){
    reloadOnPop();
    updateCalendar("#table-ticket-date");
    console.log("all tickets main script is ready")

// TABLE SUB-ROWS ANIMATION
    $(document).on("click", "body .sub-info-trigger", function(){
        $('.table-arrow').not($(this).find('.table-arrow')).removeClass("table-up")
        $(this).find('.table-arrow').removeClass("table-up")
        var sub_info_id = $(this).find('.table-arrow').attr('id');
        var sub_info_elements = $('tr[data-sub_info="' + sub_info_id + '"]');
    
        // hide all ticket-sub-info elements except the ones with the same sub_info_id
        $('tr.ticket-sub-info').not(sub_info_elements).hide();
    
        if( sub_info_elements.css("display") == 'none'){
            sub_info_elements.show()
            $(this).find('.table-arrow').addClass("table-up")
        }else{
            sub_info_elements.hide()
        }
    });


// ID #  Hide/Show
    $(document).on("mouseenter", ".table-ticket-id", function(){
        $(this).next().show()
    })
    $(document).on("mouseleave", ".ID", function(){
        $(".table-ticket-id").next().hide()
    })

// ID # FOCUS INPUT
    $(document).on("click", ".specific-id", function(){
        var $input = $(this).closest('th').find('.table-ticket-id');
        $input.focus()
        $input.attr("placeholder", "")
        $(this).parent().hide()
    });

// ID # ORDERING
    $(document).on("click", ".ascending-id, .descending-id", function(){
        var value = $(this).text()
        var table = getWhichTable($(this), true, false)
        var url = getURL(table[0], "OrderID", value, table[1])

        sendTableAJAX(url, table[0], table[1], true)
    })

// SPECIFIC ID #
    $(document).on("keyup", "body .table-ticket-id", function(event){
        if (event.which == "13") {
            var option_id = $(this).val()
            var table = getWhichTable($($(this)), true, false)
            var url = getURL(table[0], "ID", option_id, table[1])

            sendTableAJAX(url, table[0], table[1], true)
        }
    });


// PRIORITIES expanding
$(document).on("mouseover", "body #table-ticket-priority", function(){
    console.log("whoooo")
    $(this).parent().css("width", "70%")
    var span = $(this).find(".custom-select-value")
    $(this).toggleClass("priority-select")
    span.text("Priority")
    $(".crucial").text("Crucial")
    $(".high").text("High")
    $(".intermediate").text("Intermediate")
    $(".low").text("Low")
    $(".not-set").text("Not Set")
    $(".priority:not(.intermediate)").css("width", "7em")
    // $(".priority").css("width", "7em")
    $(".priority.intermediate").css("width", "7.8em")
    
    $(".priority").css("height", "1.5em")
});

// PRIORITIES contracting
$(document).on("mouseleave", "body #table-ticket-priority", function(){
    $(this).parent().css("width", "16%")
    var span = $(this).find(".custom-select-value")
    span.text("")
    $(this).toggleClass("priority-select")

    $(".crucial").text("")
    $(".high").text("")
    $(".intermediate").text("")
    $(".low").text("")
    $(".not-set").text("")
    $(".priority").css("width", "1em")
    $(".priority").css("height", "1em")
});

// DESCRIPTION FILTER
    $(document).on("keyup", ".table-ticket-description", function(event){
        if (event.which == "13") {
            var filter = "Desc"
            var value = $(this).val()

            var table = getWhichTable($(this), true, false)
            var url = getURL(table[0], filter, value, table[1])
            sendTableAJAX(url, table[0], table[1], null)
        }
    });

// PERSON FILTER
    $(document).on("keyup", ".ajax-person-input", function(event){
        var table = getWhichTable($(this), true, false)
        var page_type = $('.table-body[data-table="' + table[1] + '"]').data('data-page')
        if (event.which == "13"){
            var url_value = $(this).val()
            var url_filter = "Assignment"

            var url = getURL(table[0], url_filter, url_value, table[1])
            sendTableAJAX(url, table[0], table[1], false)
        }
    })

// DELETE TICKET
    // $(document).on("click", ".delete-ticket", function(){
    //     var result = confirm("Delete ticket forever? This action cannot be undone.");
    //     return result; // allow or prevent form submission based on the result of the confirm dialog
    // });


});
