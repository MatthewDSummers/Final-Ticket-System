import Select from './select.js'

// $(document).ready(function(e){
export default function loadSelects(){
    console.log("select scenarios ready")
    const selectElements = document.querySelectorAll('[data-select]')

    selectElements.forEach(selectElement => {
    // make new custom select 
        new Select(selectElement)
    // delete old select 
        selectElement.remove()
    })
}
loadSelects()
console.log("hu")