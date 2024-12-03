
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

    var margin = {top: 10, right: 30, bottom: 40, left: 50},
    width = 520 - margin.left - margin.right,
    height = 520 - margin.top - margin.bottom;

    var svg = d3.select("#scatter-plot")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

    svg
        .append("rect")
        .attr("x",0)
        .attr("y",0)
        .attr("height", height)
        .attr("width", height)
        .style("fill", "EBEBEB")

}