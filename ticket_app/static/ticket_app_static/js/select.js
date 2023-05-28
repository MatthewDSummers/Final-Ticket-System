

    //https://www.youtube.com/watch?v=Fc-oyl31mRI
export default class Select{

    constructor(element){

        //takes in a Select HTML select element
        this.element = element
        //this.element.id = "boo"
        this.options = getFormattedOptions(element.querySelectorAll('option'))
        this.customElement = document.createElement("div")
        this.labelElement = document.createElement("span")
        this.optionsCustomElement = document.createElement("ul")
        // this.customElement.style.zIndex ="999"
        setUpCustomElement(this)
        // resetOptions(this)
        // console.log(element.id)
        // console.log(element)
        element.style.display = "none"
        element.after(this.customElement)
    }
    get selectedOption(){
        return this.options.find(option => option.selected)
    }

    get selectedOptionIndex() {
        return this.options.indexOf(this.selectedOption)
    }
    selectValue(value){
        var newSelectedOption = this.options.find(option => {
            return option.value === value
        })
        var prevSelectedOption = this.selectedOption
        prevSelectedOption.selected = false
        prevSelectedOption.element.selected = false // not sure about this line 29:26 vid

        newSelectedOption.selected = true
        newSelectedOption.element.selected = true

        this.labelElement.innerText = newSelectedOption.label

        if (this.optionsCustomElement
            .querySelector(`[data-value="${prevSelectedOption.value}"]`) !== null){
                this.optionsCustomElement
                .querySelector(`[data-value="${prevSelectedOption.value}"]`)
                .classList.remove("selected")
            }

        const newCustomElement = this.optionsCustomElement
            .querySelector(`[data-value="${newSelectedOption.value}"]`)
        newCustomElement.classList.add("selected")
        newCustomElement.scrollIntoView({block: 'nearest'})
        //optionElement.classList.add("selected")
    }
}

function setUpCustomElement(select){
    //to pass in this custom select js class

    // give the custom select all the original select's classes
    var classes = select.element.className.split(' ')
    for (const alf of classes){
        select.customElement.classList.add(alf)
    }
    if (select.element.dataset.border == "radius"){
        select.customElement.dataset.border = "radius"
    }
    select.customElement.classList.add("custom-select-container")
    
    if (select.customElement.classList.contains("and-or-select")){
        select.customElement.classList.add("margin-block-md")
    }else{
        select.customElement.classList.add("margin-block-sm")
    }
    select.customElement.id = select.element.id
    select.customElement.tabIndex = 0

    select.labelElement.classList.add("custom-select-value")
    
    // bot pages dependen on this
    // var reset_options_trigger = document.querySelector(".remove-condition")
    // var reset_options_trigger = document.querySelector([`[data-reset-select=${select.customElement.id}]`])
    // // console.log(given, "given")
    // if (reset_options_trigger !== null){
    //     reset_options_trigger.addEventListener("click", function(e){
    //         select.labelElement.innerText = select.options[0].label
    //     })
    // }


    select.labelElement.innerText = select.selectedOption.label
    // select.labelElement.innerText = select.selectedOption.value
    select.customElement.append(select.labelElement)

    select.optionsCustomElement.classList.add("custom-select-options")
    // select.optionsCustomElement.classList.add("show-out")
    // select.customElement.style.zIndex = "9999"
    select.optionsCustomElement.style.zIndex = "9999"
    select.options.forEach(option =>{
        const optionElement = document.createElement("li")
        optionElement.classList.add("custom-select-option")
        optionElement.classList.toggle("selected", option.selected)
        optionElement.innerText = option.label
        optionElement.dataset.value = option.value
        select.optionsCustomElement.append(optionElement)


        optionElement.addEventListener("click", () => {

            if (option.value != "Select an Option..."){
                if (option.value != "And / Or ..."){
                    select.selectValue(option.value)
                    select.optionsCustomElement.classList.remove("show")
                }
            }

            if (select.customElement.dataset.border == "radius"){
                console.log("we have radius")
                select.labelElement.classList.remove("border-special")
                select.labelElement.classList.add("border-normal")
            }else{
                console.log("no radius")
            }

        })
    })

    select.customElement.append(select.optionsCustomElement)
    
    // select.customElement.addEventListener("click", () => {
    select.labelElement.addEventListener("click", () => {
        // console.log("clicked something 99999999240802984028094802984297846y0827y40782yh4072h40g274gb087bg087gb08b087b087b087b08b087b087b087v")
        // document.querySelector(".table-body").style.minHeight = "40vh";
        select.optionsCustomElement.classList.toggle("show")
        // select.parentElement.style.minHeight="40vh";
        if (select.customElement.dataset.border == "radius"){

            if (select.optionsCustomElement.classList.contains("show")){
                select.labelElement.classList.remove("border-normal")
                select.labelElement.classList.add("border-special")
            }
            else{
                select.labelElement.classList.remove("border-special")
                select.labelElement.classList.add("border-normal")
            }
        }else{
            console.log("not radius")
        }
        // specialBorder(select.labelElement)
        // select.optionsCustomElement.classList.toggle('show');
    })

    // $(document).on("click", function(e){
    //     console.log(e.target, "target IS")
    //     if (e.target != select.labelElement ){
    //         select.labelElement.classList.remove("border-special")
    //         select.labelElement.classList.add("border-normal")
    //     }
    // })


    select.customElement.addEventListener("blur", () => {

        if (select.customElement.dataset.border == "radius"){
            select.labelElement.classList.remove("border-special")
            select.labelElement.classList.add("border-normal")
        }
        select.optionsCustomElement.classList.remove("show")
        // select.optionsCustomElement.classList.toggle("show")
    })

    let debounceTimeout
    let searchTerm = ""
    select.customElement.addEventListener("keydown", e => {
        switch (e.code) {
            case "Enter":
            case "Space":
                select.optionsCustomElement.classList.toggle("show")
                break

            case "ArrowUp": {
                //e.preventDefault()
                const prevOption = select.options[select.selectedOptionIndex - 1]
                if (prevOption){
                    select.selectValue(prevOption.value)
                }
                break
            }
            case "ArrowDown": {
                //e.preventDefault()
                const nextOption = select.options[select.selectedOptionIndex + 1]
                if (nextOption){
                    select.selectValue(nextOption.value)
                }
                break
            }
                case "Escape": 
                    select.optionsCustomElement.classList.remove("show")
                    break
            default: {
                clearTimeout(debounceTimeout)
                searchTerm += e.key
                debounceTimeout = setTimeout(() => {
                    searchTerm = ""
                }, 500);
                const searchedOption = select.options.find(option =>{
                    return option.label.toLowerCase().startsWith(searchTerm)
                })
                if (searchedOption) {
                    select.selectValue(searchedOption.value)
                }
                break //need a break here? 
            }
        }
    })
}

function getFormattedOptions(optionElements){
    return [...optionElements].map(optionElement => {
        return {
            value: optionElement.value,
            label: optionElement.label,
            selected: optionElement.selected,
            element: optionElement
        }
    })
}


// function resetOptions(select){
//     var reset_options_trigger = document.querySelector([`[data-reset-select="${select.customElement.id}"]`])
//     // console.log(given, "given")


//     if (reset_options_trigger !== null){
//         reset_options_trigger.addEventListener("click", function(e){
//             select.labelElement.innerText = select.options[0].label
//             var supportive_select = document.getElementById(`${select.customElement.id}_supportive`)
//             console.log(supportive_select)
//             if (supportive_select !== null){
//                 supportive_select.remove()
//             }
//         })
//     }

// }
// function resetBorder(select){
//     select.labelElement.style.borderRadius = "7px";
// }
// function specialBorder(label){
//     label.style.borderRadius = "7px 7px 0px 0px";
// }