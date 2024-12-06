// api.js handles API form inputs

let form = document.querySelector('form');

let searchType = '';
let startDateInput = document.querySelector('.start-date');
let endDateInput = document.querySelector('.end-date');
let countryInput = document.querySelector('.country');
let engagementInput = document.querySelector('.engagement-range');
let tags = [];

let globalScatterData = null;

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if(!invalidInputHandling()) {
        toggleInvalidButton();
        console.log('Invalid Input');
        return;
    }

    // If it's the user's second time submitting form, add invisible class to previous results
    if(resultSection[1] === undefined) {
        clearResults();
    }

    displayLoadingScreen();

    // Hide error screen if it is visible
    if(!errorContainer.classList.contains('tag-section-invisible')) {
        errorContainer.classList.add('tag-section-invisible');
        errorSection.classList.toggle('error-screen');
    }

    // TEMPORARY - Hide fp-growth screen if it is visible
    if(!fpgrowthContainer.classList.contains('tag-section-invisible')) {
        fpgrowthContainer.classList.add('tag-section-invisible');
        fpgrowthSection.classList.toggle('error-screen');
    }

    if(tabOne.classList[1] === 'active') {
        searchType = 'k-means';
    }
    
    if(tabTwo.classList[1] === 'active') {
        searchType = 'apriori';
    }
    
    let dateRange = {'start': startDateInput.value, 'end': endDateInput.value};
    let country = countryInput.value;
    let engagement = engagementInput.value;

    
    // TEMPORARY fpgrowth screen as the algorithm has not yet been implemented
    if(searchType === 'apriori') {
        let timer = setTimeout(() => {
            loadingContainer.classList.add('tag-section-invisible');
            loadingSection.classList.toggle('loading');

            fpgrowthContainer.classList.remove('tag-section-invisible');
            fpgrowthSection.classList.toggle('error-screen');
        }, 2000);

        return;
    }

    try {
        // Send request to Flask
        console.log('Sending Request');
        let res = await axios.post('/result', 
            {
                searchType,
                dateRange,
                country,
                engagement,
                tags
            }, 
            
            {
                'headers': {
                    'Content-Type' : 'application/json'
                }
            }
        );
        console.log("tags:")
        console.log(res.data['best_tags']);
        console.log("-------------------")

        const scatterData = res.data;
        globalScatterData = scatterData;
        let timer = setTimeout(() => {
            resultPage(scatterData);    
        }, 2000);
    }
    catch(error) {
        console.log(error);
        
        let timer = setTimeout(() => {

            loadingContainer.classList.add('tag-section-invisible');
            loadingSection.classList.toggle('loading');

            errorContainer.classList.remove('tag-section-invisible');
            errorSection.classList.toggle('error-screen');

        }, 1000)

    }
})