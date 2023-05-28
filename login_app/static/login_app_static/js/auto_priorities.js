setInterval(function() {
    $.ajax({
        method: 'GET',
        url: '/get-priorities',
        // data: $this.serialize(),
        success: function(response){
            // $('.prios').html(`${ticket.auto_priority}`)
            // let x = response.priority
            // for (let i=0; i < response.priority.length; i++){
            //     x = $('.prios').html(response.priority[2])
                $('.update_table').html(response)

                // console.log(x)
            // }
        }
    })
}, 10000); // 10 seconds

// this only works when someone is online 