// Algorithm Information
let algoTitle = document.querySelector('.algorithm-title');
let algoDesc = document.querySelector('.algorithm-desc');


// Menu Tabs
let tabOne = document.querySelector('.tab-one');
let tabTwo = document.querySelector('.tab-two');
let tabSlider = document.querySelector('.tab-slider');

// Menu Columns
let leftCol = document.querySelectorAll('#left-col');
let rightCol = document.querySelectorAll('#right-col');


// Tag Search Elements
let tagContainer = document.querySelector('.tag-container');
let tagInputContainer = document.querySelector('.tag-input-container');
let tagInput = document.querySelector('.tag-input');
let tagHead = document.querySelector('.tag-header');
let tagField = document.querySelector('.tag-field');
let tagSubmitBtn = document.querySelector('.tag-submit-btn');


// Array to store tags
let tags = [];


// When tab one (Video Grouping) is active, all exclusve tag-search elements will be be invisible
tabOne.addEventListener('click', (e) => {
    e.preventDefault();
    if(tabOne.classList[1] !== 'active') {
        tabOne.classList.toggle('active');
        tabTwo.classList.toggle('active');

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

        if (tabSlider.classList[1] !== 'tab-slider-default') {
            tabSlider.classList.toggle('tab-slider-one');
            tabSlider.classList.toggle('tab-slider-two');
        }

        algoTitle.innerText = 'K-3 Means Search Algorithm';
        algoDesc.innerText = 'k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters.';
    }
})


// When tab two (Frequent Tag Search) is active, all exclusve tag-search elements will be visible
tabTwo.addEventListener('click', (e) => {
    e.preventDefault();
    if (tabTwo.classList[1] !== 'active') {
        tabTwo.classList.toggle('active');
        tabOne.classList.toggle('active');

        // Make frequest tag search attributes invisible
        tagHead.classList.toggle('tag-section-invisible');
        tagField.classList.toggle('tag-section-invisible');

        // Change margin bottom of search attributes
        leftCol.forEach((val) => {
            val.classList.toggle('left-col');
            val.classList.toggle('left-col-tag-search');
        });
        rightCol.forEach((val) => {
            val.classList.toggle('right-col');
            val.classList.toggle('right-col-tag-search');
        });

        if (tabSlider.classList[1] === 'tab-slider-default') {
            tabSlider.classList.remove('tab-slider-default');
            tabSlider.classList.add('tab-slider-two');
        }
        else {
            tabSlider.classList.toggle('tab-slider-one');
            tabSlider.classList.toggle('tab-slider-two');
        }

        algoTitle.innerText = 'Apriori Algorithm';
        algoDesc.innerText = 'A machine learning algorithm to identify relationships between items by identifying frequent itemsets.';
    }
})


// When user presses enter, add tag to array and frontend (added-tag class style) alongside 'x' button to remove tag
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


// Remove tags from frontend and tags array
// Backspace a tag to remove it
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


// Click x next to a tag to remove it
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