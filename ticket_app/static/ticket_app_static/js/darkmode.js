let darkMode = localStorage.getItem('darkMode');
var icon = $("#dark-mode-toggle").find(":first-child").find(':first-child')

// LINE 226 OF INBOX.JS ETC ETC OTHER FILES ETC OTHER LINES >
// > > NEED TO PUT ALL THAT theme responsive code IN THIS FILE 
// > > > AND UPDATE THEM according to THESE functions / vice versa


$(document).ready(function(){

    console.log("THEME SCRIPT REAADY")

})
const disableDarkMode = () => {
    document.getElementById("container").classList.remove("darkmode")
    localStorage.setItem('darkMode', null)
}

const enableDarkMode = () => {
    document.getElementById("container").classList.add("darkmode")
    localStorage.setItem('darkMode', 'enabled')
}

if (darkMode == "enabled"){
    enableDarkMode();
    icon.remove()
    var z =     `<svg xmlns="http://www.w3.org/2000/svg" 
                    width="24" 
                    height="24"
                    viewBox="0 0 24 24"
                    style="fill: rgb(233, 226, 107);transform: ;msFilter:;"
                >
                    <path d="M6.993 12c0 2.761 2.246 5.007 5.007 5.007s5.007-2.246 5.007-5.007S14.761 6.993 12 6.993 6.993 9.239 6.993 12zM12 8.993c1.658 0 3.007 1.349 3.007 3.007S13.658 15.007 12 15.007 8.993 13.658 8.993 12 10.342 8.993 12 8.993zM10.998 19h2v3h-2zm0-17h2v3h-2zm-9 9h3v2h-3zm17 0h3v2h-3zM4.219 18.363l2.12-2.122 1.415 1.414-2.12 2.122zM16.24 6.344l2.122-2.122 1.414 1.414-2.122 2.122zM6.342 7.759 4.22 5.637l1.415-1.414 2.12 2.122zm13.434 10.605-1.414 1.414-2.122-2.122 1.414-1.414z">
                        
                    </path>
                </svg>`

    $("#dark-mode-toggle").find(":first-child").append(z)
}else{
    disableDarkMode();
    icon.remove()
    var z = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgb(233, 226, 107);transform: ;msFilter:;"><path d="M12 11.807A9.002 9.002 0 0 1 10.049 2a9.942 9.942 0 0 0-5.12 2.735c-3.905 3.905-3.905 10.237 0 14.142 3.906 3.906 10.237 3.905 14.143 0a9.946 9.946 0 0 0 2.735-5.119A9.003 9.003 0 0 1 12 11.807z"></path></svg>
    `
    $("#dark-mode-toggle").find(":first-child").append(z)
}

$("#dark-mode-toggle").on("click", function(){
    var x = $(this).find(':first-child').find(':first-child')

    x.remove()



    darkMode = localStorage.getItem('darkMode');
    if (darkMode == "enabled"){
        disableDarkMode();
        var z = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgb(233, 226, 107);transform: ;msFilter:;"><path d="M12 11.807A9.002 9.002 0 0 1 10.049 2a9.942 9.942 0 0 0-5.12 2.735c-3.905 3.905-3.905 10.237 0 14.142 3.906 3.906 10.237 3.905 14.143 0a9.946 9.946 0 0 0 2.735-5.119A9.003 9.003 0 0 1 12 11.807z"></path></svg>
        `

    }else{
        enableDarkMode();
        var z = `
        <svg xmlns="http://www.w3.org/2000/svg" 
                            width="24" 
                            height="24"
                            viewBox="0 0 24 24"
                            style="fill: rgb(233, 226, 107);transform: ;msFilter:;"
                        >
                            <path d="M6.993 12c0 2.761 2.246 5.007 5.007 5.007s5.007-2.246 5.007-5.007S14.761 6.993 12 6.993 6.993 9.239 6.993 12zM12 8.993c1.658 0 3.007 1.349 3.007 3.007S13.658 15.007 12 15.007 8.993 13.658 8.993 12 10.342 8.993 12 8.993zM10.998 19h2v3h-2zm0-17h2v3h-2zm-9 9h3v2h-3zm17 0h3v2h-3zM4.219 18.363l2.12-2.122 1.415 1.414-2.12 2.122zM16.24 6.344l2.122-2.122 1.414 1.414-2.122 2.122zM6.342 7.759 4.22 5.637l1.415-1.414 2.12 2.122zm13.434 10.605-1.414 1.414-2.122-2.122 1.414-1.414z">
                                
                            </path>
                        </svg>
        `
    }


    
    $(this).find(':first-child').append(z)
    // console.log(x[1].getAttribute('d'))
    // x[1].setAttribute('d', "M6.993 12c0 2.761 2.246 5.007 5.007 5.007s5.007-2.246 5.007-5.007S14.761 6.993 12 6.993 6.993 9.239 6.993 12zM12 8.993c1.658 0 3.007 1.349 3.007 3.007S13.658 15.007 12 15.007 8.993 13.658 8.993 12 10.342 8.993 12 8.993zM10.998 19h2v3h-2zm0-17h2v3h-2zm-9 9h3v2h-3zm17 0h3v2h-3zM4.219 18.363l2.12-2.122 1.415 1.414-2.12 2.122zM16.24 6.344l2.122-2.122 1.414 1.414-2.122 2.122zM6.342 7.759 4.22 5.637l1.415-1.414 2.12 2.122zm13.434 10.605-1.414 1.414-2.122-2.122 1.414-1.414z")
    // console.log(x[0])
    // console.log(x[1])
})


$(document).ready(function(){
    var named = document.getElementById("caption")
    var emailed = document.getElementById("caption")
    if (named !== null){
        var name = named.dataset.name
        var email = emailed.dataset.email
        console.log(name)
        localStorage.setItem("user-name", name)
        localStorage.setItem("user-email", email)
    }
})
