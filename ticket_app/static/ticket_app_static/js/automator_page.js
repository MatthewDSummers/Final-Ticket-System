// import Select from './select.js'

// const selectElements = document.querySelectorAll('[data-select]')


$(document).on("click", ".bot-trigger", function(){
    $(this).next().toggle();
})

// selectElements.forEach(selectElement => {
// // make new custom select 
//     new Select(selectElement)
// // delete old select 
//     selectElement.remove()
// })


// $(".pickle").on("click", function(e){
//     var text = $(this).text()
//     $(this).hide()
//     var parent = e.currentTarget.parentElement
//     var optionSelected = e.currentTarget.id
//     console.log(optionSelected)
//     $.ajax({
//         method: 'POST',
//         url: '/get-info',
//         data: {
//                 "option":optionSelected
//             },
//         success:function(response){
//             var response_string = JSON.stringify(response);
//             if (response_string ==="{}"){
//                 console.log("it's empty")
//             }

//     // else, let's make some new selects 
//             else {
//                 const resp = response
//                 const select = document.createElement("SELECT");
//                 var option = document.createElement("option")
//                 option.text = text
//                 select.add(option)
//                 for (let key in resp) {
//                     // if (resp.hasOwnProperty(key)) {
//                     if (key !== "category" && key !== "person" && key !== "priority"){
//                         var option = document.createElement("option");
//                         var value = resp[key].slice(0, resp[key].indexOf('|'));
//                         option.text = value;
//                         var option_value = resp[key].slice(resp[key].indexOf('|'));
//                         option.value = option_value.replace("|", "")
//                         select.add(option);
//                     }
//                     // }
//                 }
//             // setup select 
//                 select.id = `${parent.id}_supportive`
//                 select.classList.add(`${parent.id}_supportive`)
//                 select.add(option);
//             // append selected to desired div
//                 var desired = document.getElementById(parent.id)
//                 desired.append(select)
//             // make it a custom select 
//                 new Select(select)
//                 select.remove()
//             }
//         }
//     }); 

// })