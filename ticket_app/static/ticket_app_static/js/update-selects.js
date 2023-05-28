import Select from './select.js'


function removeFirstOption(){
    const newOptions = document.querySelectorAll(".custom-select-options")

    newOptions.forEach(option => {
        option.firstChild.remove()
    })
}
removeFirstOption()

function updateSelects(){
    const selectElements = document.querySelectorAll('[data-select]')
    selectElements.forEach(selectElement => {
        new Select(selectElement)
        selectElement.remove()
    });
}

export { removeFirstOption, updateSelects };
