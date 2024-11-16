// api.js handles API form inputs

let form = document.querySelector('form');

let startDateInput = document.querySelector('.start-date');
let endDateInput = document.querySelector('.end-date');
let countryInput = document.querySelector('.country');
let engagementInput = document.querySelector('.engagement-range');
let tags = [];

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    let dateRange = {'start': startDateInput.value, 'end': endDateInput.value};
    let country = countryInput.value;
    let engagement = engagementInput.value;

    try {
        let res = await axios.post('/result', 
            {
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

