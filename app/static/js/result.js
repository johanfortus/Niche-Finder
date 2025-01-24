let loadingSection = document.querySelector('#loading');
let loadingContainer = document.querySelector('.loadingContainer');

let errorSection = document.querySelector('#error-screen');
let errorContainer = document.querySelector('.error-container');
let tryAgainBtn = document.querySelector('.try-again-btn');

let resultSection = document.querySelector('.result-section');
let resultHeader = document.querySelector('.result-header');

// Display loading screen
function displayLoadingScreen(){
    loadingContainer.removeAttribute('class', 'tag-section-invisible');
    loadingSection.classList.toggle('loading');
    loadingSection.scrollIntoView();
}

// Clear results if submitting form again
function clearResults() {
    resultSection.classList.add('tag-section-invisible');
    resultHeader.innerHTML = '';
    clusterTabOne.innerHTML = '';
    clusterTabTwo.innerHTML = '';
    clusterTabThree.innerHTML = '';
    clusterTabSlider.classList = '';
    scatterPlot.innerHTML = '';
    networkGraph.innerHTML = '';

    if(!clusterTabTwo.classList.contains('active')) {
        clusterTabOne.classList.remove('active');
        clusterTabThree.classList.remove('active');
        clusterTabTwo.classList.add('active');
        clusterTabSlider.classList.add('cluster-tab-slider-default');
    }
}

// Display result page
function resultPage(scatterData) {

    loadingContainer.classList.add('tag-section-invisible');
    loadingSection.classList.toggle('loading');

    resultSection.classList.remove('tag-section-invisible');
    resultHeader.innerHTML = 'Result';
    console.log("SCATTER DATA: ", scatterData);
    if (scatterData['best_tags']) {
        createNetworkGraph(scatterData['best_tags']);
    }
    else {
        clusterTabOne.innerHTML = 'Views vs Comments';
        clusterTabTwo.innerHTML = 'Likes vs Views';
        clusterTabThree.innerHTML = 'Views vs Engagement';
        createScatterPlot(scatterData);
    }
}

// Error Screen
tryAgainBtn.addEventListener('click', () => {
    selectSearchSection.scrollIntoView();
})

document.querySelector('.fpgrowth-try-again-btn').addEventListener('click', () => {
    selectSearchSection.scrollIntoView();
})