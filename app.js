
let algoTitle = document.querySelector(".algorithm-title");
let algoDesc = document.querySelector(".algorithm-desc");

let tabOne = document.querySelector(".tab-one");
let tabTwo = document.querySelector(".tab-two");

let tagContainer = document.querySelector(".tag-container");
let tagInputContainer = document.querySelector(".tag-input-container");
let tagInput = document.querySelector(".tag-input");
let tagHead = document.querySelector(".tag-header");
let tagField = document.querySelector(".tag-field");

let tags = [];

tabOne.addEventListener("click", (e) => {
    e.preventDefault();
    if(tabOne.classList[1] !== "active") {
        tabOne.classList.toggle("active");
        tabTwo.classList.toggle("active");

        tagHead.classList.toggle("tag-section-invisible");
        tagField.classList.toggle("tag-section-invisible");

        algoTitle.innerText = "K-3 Means Search Algorithm";
        algoDesc.innerText = "k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters";
    }
})

tabTwo.addEventListener("click", (e) => {
    e.preventDefault();
    if(tabTwo.classList[1] !== "active") {
        tabTwo.classList.toggle("active");
        tabOne.classList.toggle("active");

        tagHead.classList.toggle("tag-section-invisible");
        tagField.classList.toggle("tag-section-invisible");


        algoTitle.innerText = "Apriori Algorithm";
        algoDesc.innerText = "A machine learning algorithm to identify relationships between items by identifying frequent itemsets.";
    }
})

tagInput.addEventListener("keyup", (e) => {
    // if(e.key === "Enter" || e.key === " ") {
    if(e.key === "Enter") {
        tags.push(tagInput.value.trim());        
        
        let newTag = document.createElement("span");
        newTag.setAttribute("class", "added-tag");
        newTag.innerText = tagInput.value;
        
        deleteTagBtn = document.createElement("button");
        deleteTagBtn.innerText = "x";
        deleteTagBtn.setAttribute("class", "delete-tag-btn");
        newTag.append(deleteTagBtn);
        
        // https://stackoverflow.com/questions/46188263/how-to-append-an-element-before-another-using-javascript
        tagContainer.insertBefore(newTag, tagInputContainer);
        
        tagInput.value = "";

        console.log(tags);
    }
    
    if(e.key === "Backspace") {
        if(tagInputContainer.previousElementSibling) {
            tagInputContainer.previousElementSibling.remove();
            tags.pop();
            console.log(tags);
        }
    }
})

tagContainer.addEventListener("click", (e) => {
    if(e.target.tagName === "BUTTON") {
        let removedTag = e.target.parentElement.innerText;
        removedTag = removedTag.slice(0, removedTag.length - 1).trim();
        
        let idx = tags.indexOf(removedTag);
        tags.splice(idx, 1);
        
        e.target.parentElement.remove();
        console.log(tags);
    }
})


