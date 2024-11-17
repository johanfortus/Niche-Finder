// api.js handles API form inputs

let form = document.querySelector('form');

let searchType = '';
let startDateInput = document.querySelector('.start-date');
let endDateInput = document.querySelector('.end-date');
let countryInput = document.querySelector('.country');
let engagementInput = document.querySelector('.engagement-range');
let tags = [];

form.addEventListener('submit', async (e) => {
    e.preventDefault();

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

        console.log(res.data);
    }
    
    catch(error) {
        console.log(error);
    }

    

})