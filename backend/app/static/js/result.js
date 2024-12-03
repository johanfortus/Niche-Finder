
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

// Used Scatter Plot Template - https://d3-graph-gallery.com/graph/custom_theme.html
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
        .style("fill", "#FFFFFF")

    var x = d3.scaleLinear()
        .domain(d3.extent(scatterData, d => d.view_count_T))
        .range([0, width]);
        
    var y = d3.scaleLinear()
        .domain(d3.extent(scatterData, d => d.like_count_T))
        .range([height, 0]);

    // X axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(-height*1.3).ticks(10))
        .call(g => g.select(".domain").remove())
        .selectAll("text")
        .style("fill", "white")
    
    // Y axis
    svg.append("g")
        .call(d3.axisLeft(y).tickSize(-width*1.3).ticks(7))
        .call(g => g.select(".domain").remove())
        .selectAll("text")
        .style("fill", "white");
    
    // Customization
    svg.selectAll(".tick line")
        .attr("stroke", "lightgray");

    // X axis label
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width/2 + margin.left)
        .attr("y", height + margin.top + 20)
        .style("fill", "white")
        .text("View Count");
    
    // Y axis label
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 20)
        .attr("x", -margin.top - height/2 + 20)
        .style("fill", "white")
        .text("Like Count");

}