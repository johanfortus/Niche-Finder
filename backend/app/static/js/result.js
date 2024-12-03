
let loadingSection = document.querySelector('#loading');
let loadingContainer = document.querySelector('.loadingContainer');
let resultSection = document.querySelector('.result-section');
let resultHeader = document.querySelector('.result-header');
let scatterPlot = document.querySelector('#scatter-plot')

function resultPage(scatterData) {

    loadingContainer.removeAttribute('class', 'tag-section-invisible');
    loadingSection.classList.toggle('loading');
    loadingSection.scrollIntoView();

    let timer = setTimeout(() => {
        loadingContainer.classList.add('tag-section-invisible');
        loadingSection.classList.toggle('loading');

        resultSection.classList.remove('tag-section-invisible');
        resultHeader.innerHTML = 'Result';

        createScatterPlot(scatterData);
    }, 2000);

}

function createScatterPlot(scatterData){
    console.log("CREATING SCATTER PLOT");
    console.log(scatterData);
}