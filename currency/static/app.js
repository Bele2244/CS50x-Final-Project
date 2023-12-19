
// Button variables
const addBtnOne = document.querySelector('#add-btn-1');
const addBtnTwo = document.querySelector('#add-btn-2');
const deleteBtnOne = document.querySelector('#delete-btn-1');
const deleteBtnTwo = document.querySelector('#delete-button-2');
const convertBtn = document.querySelector('#convert-btn');
const convertBtnTwo = document.querySelector('#convert-btn-2');

// Input Add Form variables
const addRemoveBtns = document.querySelectorAll('.add-remove-btns');
const inputAdd = document.querySelectorAll('.input-add');

// Input Convert variable
const inputConvert = document.querySelector('.input-convert');


// Currency not added hide the convert button
let ulList = document.querySelectorAll('.list-group-item');
if (ulList.length < 2) {
    convertBtn.style.display = 'none';
}

// Convert button
convertBtn.addEventListener('click', function(){

    hideButtons();
    inputConvert.style.display = 'block';
});

// First add button
addBtnOne.addEventListener('click', function(){

    // Hide buttons
    hideButtons();

    for (let i = 0; i < addRemoveBtns.length; i++) {
        // Show input form
        inputAdd[i].style.display = 'block';
    }

});

// First delete button - checkbox creation
deleteBtnOne.addEventListener('click', function(){

    // Show second delete button 
    deleteBtnTwo.style.display = 'block';

    // Hide buttons
    hideButtons();
    
    let ulList = document.querySelectorAll('.list-group-item');

    for (let i = 0; i < ulList.length; i++) {
        // li element
        let liItem = ulList[i];
        // change the color of li elements
        liItem.style.backgroundColor = '#ff3d50';
        liItem.style.color = 'white';

        // Get label element from li element
        let labelItem = liItem.childNodes[1];
        
        // Get for attribute from label element
        let forAttribute = labelItem.getAttribute('for');
        
        // Create new input tag and append it to li
        let checkbox = document.createElement('input');

        // Match label attributes with new checkbox element
        checkbox.type = 'checkbox';
        checkbox.class = 'form-check-input';
        checkbox.value = forAttribute;
        checkbox.id = forAttribute;
        checkbox.name = forAttribute;

        // Make checkboxes bigger
        checkbox.style.width = '20px';
        checkbox.style.height = '20px';

        // Append new check box to existing label
        liItem.appendChild(checkbox);

        
    }
});

// Hide all buttons
function hideButtons() {
    for (let i = 0; i < addRemoveBtns.length; i++) {
        addRemoveBtns[i].style.display = 'none';
    }
}
