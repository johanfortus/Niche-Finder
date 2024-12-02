let loadingSection = document.querySelector('#loading');
let loadingContainer = document.querySelector('.loadingContainer');

let resultSection = document.querySelector('.result-section');
let resultHeader = document.querySelector('.result-header');

let clusterTabOne = document.querySelector('.cluster-tab-one');
let clusterTabTwo = document.querySelector('.cluster-tab-two');
let clusterTabThree = document.querySelector('.cluster-tab-three');
let clusterTabSlider = document.querySelector('.cluster-tab-slider');

let scatterPlot = document.querySelector('#scatter-plot');

function resultPage(scatterData) {

    // If it's the user's second time submitting form, add invisible class to previous results
    if(resultSection[1] === undefined) {
        resultSection.classList.add('tag-section-invisible');
        resultHeader.innerHTML = '';
        clusterTabOne.innerHTML = '';
        clusterTabTwo.innerHTML = '';
        clusterTabThree.innerHTML = '';
        scatterPlot.innerHTML = '';
    }

    // Display loading screen
    loadingContainer.removeAttribute('class', 'tag-section-invisible');
    loadingSection.classList.toggle('loading');
    loadingSection.scrollIntoView();

    // Display results after two seconds
    let timer = setTimeout(() => {
        loadingContainer.classList.add('tag-section-invisible');
        loadingSection.classList.toggle('loading');

        resultSection.classList.remove('tag-section-invisible');
        resultHeader.innerHTML = 'Result';

        clusterTabOne.innerHTML = 'Views vs Comments'
        clusterTabTwo.innerHTML = 'Likes vs Views'
        clusterTabThree.innerHTML = 'Views vs Engagement'

        createScatterPlot(scatterData);
    }, 2000);

}

// Used Scatter Plot Template - https://d3-graph-gallery.com/graph/custom_theme.html
function createScatterPlot(scatterData){
    console.log("CREATING SCATTER PLOT");
    console.log(scatterData);

    var margin = {top: 10, right: 30, bottom: 40, left: 50},
    width = 700 - margin.left - margin.right,
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
        .attr("width", width)
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
        .call(d3.axisBottom(x).tickSize(-height*1).ticks(10))
        .call(g => g.select(".domain").remove())
        .selectAll("text")
        .style("fill", "white")
    
    // Y axis
    svg.append("g")
        .call(d3.axisLeft(y).tickSize(-width*1).ticks(7))
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
        .text("View Count (Scaled)");
    
    // Y axis label
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 20)
        .attr("x", -margin.top - height/2 + 20)
        .style("fill", "white")
        .text("Like Count (Scaled)");
    
    // Color scale - 3 clusters
    var color = d3.scaleOrdinal()
        .domain([0, 1, 2])
        .range(["#F8766D", "#00BA38", "#619CFF"]);
    
    var activeDot = null;
    
    // Add dots
    svg.append('g')
        .selectAll("circle")
        .data(scatterData)
        .enter()
        .append("circle")
        .attr("cx", () => Math.random() * width)
        .attr("cy", () => Math.random() * height)
        .attr("r", 0)
        .style("fill", d => color(d.kmeans_3))
        .style('opacity', 0)
        .style('cursor', 'pointer')

        // Hover events
        .on('mouseover', function(e,d) {

            // Reset the previous activeDot
            if(activeDot && activeDot !== this) {
                d3.select(activeDot)
                    .transition()
                    .duration(200)
                    .attr('r', 5)
                    .style('fill', color(d3.select(activeDot).data()[0].kmeans_3));
                
                activeDot = null;
            }

            // Enlarge Dot
            d3.select(this)
                .transition()
                .duration(200)
                .attr('r', 8)

            // Video information
            d3.select('.tooltip')
                .classed('visible', true)
                .html(`
                        <img src="${d.thumbnail_url}" class="tooltip-thumbnail" onClick="window.open(href='https://www.youtube.com/watch?v=${d.video_id}', '_blank')"> <br>
                        <b class="tooltip-video-title" onClick="window.open(href='https://www.youtube.com/watch?v=${d.video_id}', '_blank')">${d.title}</b> <br>
                        Channel: ${d.channel_name} <br>
                        Views: ${d.view_count} <br>
                        Likes: ${d.like_count} <br>
                        Comments: ${d.comment_count}
                    `)
                .style('top', (e.pageY - 10) + 'px')
                .style('left', (e.pageX + 10) + 'px');
        })

        // Mouse move events
        .on('mousemove', function() {
            if(activeDot !== this) {
                d3.select('.tooltip')
                    .style('top', (e.pageY - 10) + 'px')
                    .style('left', (e.pageX + 10) + 'px');
            }
        })

        // Mouse out events
        .on('mouseout', function(){
            if(activeDot !== this) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('r', 5)
                    .style('fill', color(d3.select(this).data()[0].kmeans_3));

                d3.select('.tooltip')
                    .classed('visible', false);
            }
        })

        // Click events
        .on('click', function(e, d) {
            if(activeDot === this) {
                activeDot = null;
                d3.select('.tooltip').classed('visible', false);
                d3.select(this)
                    .transition()
                    .attr('r', 5)
                    .style('fill', color(d.kmeans_3));
            }
            else {
                if(activeDot) {
                    d3.select(activeDot)
                        .transition()
                        .attr('r', 5)
                        .style('fill', color(d3.select(activeDot).data()[0].kmeans_3));
                }
                activeDot = this;

                // On dot click, stop moving, stay enlarged, and darken
                d3.select(this)
                    .interrupt()
                    .transition()
                    .attr('r', 8)
                    .style('fill', d3.color(color(d.kmeans_3)).darker(1))

                d3.select('.tooltip')
                    .classed('visible', true)
                    .html(`
                            <img src="${d.thumbnail_url}" class="tooltip-thumbnail" onClick="window.open(href='https://www.youtube.com/watch?v=${d.video_id}', '_blank')"> <br>
                            <b class="tooltip-video-title" onClick="window.open(href='https://www.youtube.com/watch?v=${d.video_id}', '_blank')">${d.title}</b> <br>
                            Channel: ${d.channel_name} <br>
                            Views: ${d.view_count} <br>
                            Likes: ${d.like_count} <br>
                            Comments: ${d.comment_count}
                        `)
                        .style('top', (e.pageY - 10) + 'px')
                        .style('left', (e.pageX + 10) + 'px');
            }
        })

        // Animation
        .transition()
        .duration(1000)
        .delay((d, i) => i * 50)
        .attr('cx', d => x(d.view_count_T))
        .attr('cy', d => y(d.like_count_T))
        .attr('r', 5)
        .style('fill', d => color(d.kmeans_3))
        .style('opacity', 1)
        .on('end', function() {
            floatingAnimation(d3.select(this));
        });
    
    function floatingAnimation(selection) {
        selection
            .transition()
            .duration(2000)
            .ease(d3.easeSinInOut)
            .attr('cx', d => x(d.view_count_T) + (Math.random() - 0.5) * 10)
            .attr('cy', d => y(d.like_count_T) + (Math.random() - 0.5) * 10)
            .on('end', function() {
                floatingAnimation(d3.select(this));
            });
    }
}