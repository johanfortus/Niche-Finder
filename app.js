
let algoTitle = document.querySelector(".algorithm-title");
let algoDesc = document.querySelector(".algorithm-desc");

let tabOne = document.querySelector(".tab-one");
let tabTwo = document.querySelector(".tab-two");

let tagInput = document.querySelector(".tag-input");
let tagHead = document.querySelector(".tag-header");
let tagField = document.querySelector(".tag-field");

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

