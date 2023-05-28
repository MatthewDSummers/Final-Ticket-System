// const fors = Document.getElementById("registrationform");



var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

function toggleTheme() {
    var theme = document.getElementsByTagName('link')[0];

    if (theme.getAttribute('href') == 'light.css') {
        theme.setAttribute('href', 'dark.css');
        // theme.setAttribute('href') == 'dark.css');
    } else if (theme.getAttribute('href') == 'dark.css') {
        theme.setAttribute('href', 'light.css');
    }
}

function registrationForm(){
    var fors = document.getElementById("registrationform");
    // fors.className= "hidden";
    gsap.to('.gsap-content', { x: '-200%', ease: 'power3' })
    fors.classList.remove("hidden");
    gsap.to('.registration-form', { x: '-250%', ease: 'power3' })
}


// sliding nav

// https://www.quanzhanketang.com/howto/howto_js_sidenav.html



// function openNav() {
//     document.getElementById("sidenav").style.width = "250px";
//     document.getElementById("container").style.marginLeft = "250px";
//     document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
//     }
    
// function closeNav() {
//     document.getElementById("sidenav").style.width = "0";
//     document.getElementById("container").style.marginLeft= "0";
//     document.body.style.backgroundColor = "white";
//     }


