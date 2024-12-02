
let loadingSection = document.querySelector('#loading');
let loadingContainer = document.querySelector('.loadingContainer');
function loadingScreen() {
    loadingContainer.removeAttribute('class', 'tag-section-invisible');
    loadingSection.classList.toggle('loading');
    loadingSection.scrollIntoView();
}

function createScatterPlot(scatterData){
    console.log("CREATING SCATTER PLOT");
    console.log(scatterData);
}