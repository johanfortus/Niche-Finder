// app.js handles frontend interactivity (and adding to tags array)

// Frontend Elements
let algoInfoContainer = document.querySelector('.algorithm-info');
let algoTitle = document.querySelector('.algorithm-title');
let algoDesc = document.querySelector('.algorithm-desc');

let selectSearchSection = document.querySelector('.select-search-section');
let tabOne = document.querySelector('.tab-one');
let tabTwo = document.querySelector('.tab-two');
let tabSlider = document.querySelector('.tab-slider');
let searchAttributeContainer = document.querySelector('.search-attributes-container');
let leftCol = document.querySelectorAll('.left-col');
let rightCol = document.querySelectorAll('.right-col');

let tagContainer = document.querySelector('.tag-container');
let tagInputContainer = document.querySelector('.tag-input-container');
let tagInput = document.querySelector('.tag-input');
let tagHead = document.querySelector('.tag-header');
let tagField = document.querySelector('.tag-field');

let btnContainer = document.querySelector('.btn-container');
let submitBtn = document.querySelector('.submit-btn');

// When tab one (Video Grouping) is active, all exclusve tag-search elements will be be invisible
tabOne.addEventListener('click', (e) => {
    e.preventDefault();
    if(tabOne.classList[1] !== 'active') {
        tabOne.classList.toggle('active');
        tabTwo.classList.toggle('active');
        resetFields();

        // Tab Slide Animation
        if (tabSlider.classList[1] !== 'tab-slider-default') {
            tabSlider.classList.toggle('tab-slider-one');
            tabSlider.classList.toggle('tab-slider-two');
        }

        // Fade transition new content
        btnContainer.classList.toggle('element-fade');
        searchAttributeContainer.classList.toggle('element-fade');
        algoInfoContainer.classList.toggle('element-fade');

        // Delay content change until content has fully faded out
        const timer = setTimeout(() => {
            // Make frequest tag search attributes invisible
            tagHead.classList.toggle('tag-section-invisible');
            tagField.classList.toggle('tag-section-invisible');

            // Change margin bottom of search attributes
            leftCol.forEach((val) => {
                val.classList.toggle('left-col', 'left-col-tag-search');
                val.classList.toggle('left-col-tag-search');
            });
            rightCol.forEach((val) => {
                val.classList.toggle('right-col');
                val.classList.toggle('right-col-tag-search');
            });

            // Change algorithm title and description
            algoTitle.innerText = 'K-Means Search Algorithm';
            algoDesc.innerText = 'A machine learning algorithm that groups data into clusters based on similarities, aiming to organize items into meaningful categories.';
            
            // Remove fade class
            btnContainer.classList.toggle('element-fade');
            searchAttributeContainer.classList.toggle('element-fade');
            algoInfoContainer.classList.toggle('element-fade');
        }, 200);
    }
})

// Tab switching logic
tabTwo.addEventListener('click', (e) => {
    e.preventDefault();
    if (tabTwo.classList[1] !== 'active') {
        tabTwo.classList.toggle('active');
        tabOne.classList.toggle('active');
        resetFields();
        
        if (tabSlider.classList[1] === 'tab-slider-default') {
            tabSlider.classList.remove('tab-slider-default');
            tabSlider.classList.add('tab-slider-two');
        }
        else {
            tabSlider.classList.toggle('tab-slider-one');
            tabSlider.classList.toggle('tab-slider-two');
        }

        btnContainer.classList.toggle('element-fade');
        searchAttributeContainer.classList.toggle('element-fade');
        algoInfoContainer.classList.toggle('element-fade');
        
        const timer = setTimeout(() => {

            leftCol.forEach((val) => {
                val.classList.toggle('left-col');
                val.classList.toggle('left-col-tag-search');
            });
            rightCol.forEach((val) => {
                val.classList.toggle('right-col');
                val.classList.toggle('right-col-tag-search');
            });

            tagHead.classList.toggle('tag-section-invisible');
            tagField.classList.toggle('tag-section-invisible');

            algoTitle.innerText = 'FP-Growth Algorithm';
            algoDesc.innerText = 'A machine learning algorithm to identify relationships between items by identifying frequent itemsets.';

            btnContainer.classList.toggle('element-fade');
            searchAttributeContainer.classList.toggle('element-fade');
            algoInfoContainer.classList.toggle('element-fade');
        }, 200);
    }
})

tagInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        tags.push(tagInput.value.trim());        
        
        let newTag = document.createElement('span');
        newTag.setAttribute('class', 'added-tag');
        newTag.innerText = tagInput.value;
        
        deleteTagBtn = document.createElement('button');
        deleteTagBtn.innerText = 'x';
        deleteTagBtn.setAttribute('class', 'delete-tag-btn');
        newTag.append(deleteTagBtn);
        
        // https://stackoverflow.com/questions/46188263/how-to-append-an-element-before-another-using-javascript
        tagContainer.insertBefore(newTag, tagInputContainer);
        
        tagInput.value = '';
        console.log(tags);
    }
})

// Remove tag on backspace
tagInput.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace' && tagInput.value === '') {
        if (tagInputContainer.previousElementSibling) {
            console.log(tagInput.value)
            tagInputContainer.previousElementSibling.remove();
            tags.pop();
            console.log(tags);
        }
    }
})

// Remove tag on x button clicked
tagContainer.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
        let removedTag = e.target.parentElement.innerText;
        removedTag = removedTag.slice(0, removedTag.length - 1).trim();
        
        let idx = tags.indexOf(removedTag);
        tags.splice(idx, 1);
        
        e.target.parentElement.remove();
        console.log(tags);
    }
})


// Handling Invalid User Inputs
startDateInput.addEventListener('click', (e) => {
    if(startDateInput.classList.contains('invalid-input')) {
        startDateInput.classList.remove('invalid-input');
        endDateInput.classList.remove('invalid-input');
    }
    if(submitBtn.classList.contains('invalid-btn')) {
        submitBtn.classList.toggle('submit-btn');
        submitBtn.classList.toggle('invalid-btn');
        submitBtn.innerHTML = 'Submit';
    }
})
endDateInput.addEventListener('click', (e) => {
    if(endDateInput.classList.contains('invalid-input')) {
        startDateInput.classList.remove('invalid-input');
        endDateInput.classList.remove('invalid-input');
    }
    if(submitBtn.classList.contains('invalid-btn')) {
        submitBtn.classList.toggle('submit-btn');
        submitBtn.classList.toggle('invalid-btn');
        submitBtn.innerHTML = 'Submit';
    }
})
countryInput.addEventListener('click', (e) => {
    if(countryInput.classList.contains('invalid-input')) {
        countryInput.classList.remove('invalid-input');
    }
    if(submitBtn.classList.contains('invalid-btn')) {
        submitBtn.classList.toggle('submit-btn');
        submitBtn.classList.toggle('invalid-btn');
        submitBtn.innerHTML = 'Submit';
    }
})
function invalidInputHandling() {
    let isInputValid = true;
    if(startDateInput.value === '') {
        invalidInputStyle(startDateInput);
        isInputValid = false;
    }
    if(endDateInput.value === '') {
        invalidInputStyle(endDateInput);
        isInputValid = false;
    }
    if(startDateInput.value > endDateInput.value) {
        invalidInputStyle(startDateInput);
        invalidInputStyle(endDateInput);
        isInputValid = false;
    }
    
    if(countryInput.value === '') {
        invalidInputStyle(countryInput);
        isInputValid = false;
    }
    return isInputValid;
}

function invalidInputStyle(input) {
    input.classList.add('invalid-input');
}

function toggleInvalidButton() {
    if(submitBtn.classList.contains('submit-btn')) {
        submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle" style="color: #B91C1C;"></i> Invalid Input';
    }
    else {
        submitBtn.innerHTML = 'Submit';
    }
    submitBtn.classList.toggle('submit-btn');
    submitBtn.classList.toggle('invalid-btn');
}

// Function to reset fields
function resetFields() {
    startDateInput.value = '';
    startDateInput.classList.remove('invalid-input');
    endDateInput.value = '';
    endDateInput.classList.remove('invalid-input');
    countryInput.value = '';
    countryInput.classList.remove('invalid-input');
    engagementInput.value = '';
    if(submitBtn.classList.contains('invalid-btn')) {
        submitBtn.innerHTML = 'Submit';
        submitBtn.classList.toggle('submit-btn');
        submitBtn.classList.toggle('invalid-btn');
    }
}