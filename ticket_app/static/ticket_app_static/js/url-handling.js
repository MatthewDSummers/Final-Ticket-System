function reloadOnPop(){
    window.addEventListener('popstate', function(event) {
        // load the page when user clicks back or forward. had to do this because of below.
        location.reload();
    });
}

function getURL(page_type=null, filter=null, value=null, table_variant){

    const params = new URLSearchParams(window.location.search);
    // if (params.has('filter')) {
    if (page_type == null){
        var page_type = params.get('type');

    }

    
    var discerner = document.getElementById("discerner").value

    // }
    // if (table_variant == null && filter != null){
    if (discerner == "SingleTable"){
        if(filter != null){
            return `/ticket-easy/tickets/?type=${page_type}&filter=${filter}&value=${value}&table_variant=${table_variant}&page=1`
        }else{
            return `/ticket-easy/tickets/?type=${page_type}&table_variant=${table_variant}&page=1`
        }
    }
    else if (discerner == "MultiTable"){
        console.log(page_type, "page type")

        var user_id = window.location.pathname.match(/\/users\/(\d+)/)[1];

        console.log(typeof(user_id), " < -- - user id type")
        console.log(user_id, "user idjjjj")
        if (value !== null){
            console.log("we're doing it . gotthe URL for the USER ID", "---->", user_id)

            return `/ticket-easy/users/${user_id}?type=${page_type}&filter=${filter}&value=${value}&table_variant=${table_variant}&page=1`
        }else{
            return `/ticket-easy/users/${user_id}?type=${page_type}&table_variant=${table_variant}&page=1`
        }
    }
}

function updateURL(URL){
    var newUrl =  URL;
    history.pushState(null, null, newUrl);
}

export { reloadOnPop, getURL, updateURL };

