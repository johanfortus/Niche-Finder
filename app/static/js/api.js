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

    if(tabOne.classList[1] === 'active') {
        searchType = 'k-means';
    }
    
    if(tabTwo.classList[1] === 'active') {
        searchType = 'apriori';
    }
    
    let dateRange = {'start': startDateInput.value, 'end': endDateInput.value};
    let country = countryInput.value;
    let engagement = engagementInput.value;

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
        resultPage(scatterData);
    }
    catch(error) {
        console.log(error);
    }
})