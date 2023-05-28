$("document").ready(function(){
    function setUpAjax(){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
    setUpAjax()


// AJAX FOR INBOX ACTIONS
    function sendInboxActionsAJAX(data){
        $.ajax({ 
            method: 'POST',
            url: '/ticket-easy/mail/',
            data: {
                    "action": data.action,
                    "message_id": data.message_id,
                    "inbox_id": data.inbox_id,
                    "title": data.title
                },
            success:function(response){
                $("body").html(response)
                setUpAjax()
            }
        });
    }

    // INBOX ACTIONS (Star, Trash, Delete, Restore, Mark as read, Mark as unread )
    $(".table-action-icon").on("click", function(e){
        var message_id = $(this).data("message")
        var inbox_id = $(this).data("inbox")
        var page_title = $(".title").attr("id")
        var action = $(this).data("action")

        var data = {
            action: action,
            message_id: message_id,
            inbox_id: inbox_id,
            title: page_title
        };

        if($(this).data("action") == "destroy"){
            var result = confirm("Permanently delete this message?");
            if (result == true){
                sendInboxActionsAJAX(data)
            }else{
                return result;
            }
        }else{
            sendInboxActionsAJAX(data)
        }

    });


// VIEW MESSAGE
    // Checks to make sure the TD element does not contain an action; if it doesn't, view message.
    $('.inbox-table').on('click', 'td', function(e) {
        var target_command = ["hoverable-actions-td", "table-actions"];

        if (!target_command.some(item => e.currentTarget.classList.contains(item))) {
            console.log("not the hoverable actions. this is the rest of the TR (the message)")
            var tr = $(this).closest("tr");
            var message_url = tr.data("url");
            var inbox_id = tr.data("inbox");
            window.location = `/ticket-easy/mail/${inbox_id}/${message_url}`;
        } 
    });

// Styles backgrounds etc. probably can just put it in CSS 
    $('.inbox-table').on('mouseenter', 'tr', function() {
        var message_id = $(this).attr("id")
        var action = document.getElementById(`${message_id}-actions`)

        if (!$(this).hasClass("viewed")){
            $(this).css("background-color", "hsl(214, 25%, 96%)")
            action.classList.remove("viewed")
            action.classList.add("unviewed")

        }else{
            action.classList.remove("unviewed")
            action.classList.add("viewed")
        }
        action.style.opacity = "1"
        $(this).css("box-shadow", "0px 2px 4px hsl(214, 25%, 90%), 0px 2px 4px hsl(214, 25%, 90%)")

    });

// Styles backgrounds etc. probably can just put it in CSS 
    $('.inbox-table').on('mouseleave', 'tr', function() {

        var message_id = $(this).attr("id")
        var action = document.getElementById(`${message_id}-actions`)

        if (!$(this).hasClass("viewed")){
            $(this).css("background-color", "white")
            action.classList.remove("viewed")
            action.classList.add("unviewed")
        }else{
            action.classList.remove("unviewed")
            action.classList.add("viewed")
        }

        action.style.opacity = "0"
        $(this).css("box-shadow", "none")

    });

    $('table').on('mouseover', function() {
        $(this).css("cursor", "pointer")
    });

    function getBrowserName(userAgent) {
        // The order matters here, and this may report false positives for unlisted browsers.

        if (userAgent.includes("Firefox")) {
        // "Mozilla/5.0 (X11; Linux i686; rv:104.0) Gecko/20100101 Firefox/104.0"
        return "Mozilla Firefox";
        } else if (userAgent.includes("SamsungBrowser")) {
        // "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G955F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/9.4 Chrome/67.0.3396.87 Mobile Safari/537.36"
        return "Samsung Internet";
        } else if (userAgent.includes("Opera") || userAgent.includes("OPR")) {
        // "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 OPR/90.0.4480.54"
        return "Opera";
        } else if (userAgent.includes("Trident")) {
        // "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
        return "Microsoft Internet Explorer";
        } else if (userAgent.includes("Edge")) {
        // "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
        return "Microsoft Edge (Legacy)";
        } else if (userAgent.includes("Edg")) {
        // "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Edg/104.0.1293.70"
        return "Microsoft Edge (Chromium)";
        } else if (userAgent.includes("Chrome")) {
        // "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        return "Google Chrome or Chromium";
        } else if (userAgent.includes("Safari")) {
        // "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1"
        return "Apple Safari";
        } else {
        return "unknown";
        }
    }

    var browserName = getBrowserName(navigator.userAgent);
    console.log(`You are using: ${browserName}`);

});

