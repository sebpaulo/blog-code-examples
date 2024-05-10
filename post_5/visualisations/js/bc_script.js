// this visualisation is adapted and inspired by https://observablehq.com/@d3/connected-scatterplot/2?intent=fork

const dataURL = "data/de_data.json";

fetch(dataURL)
      .then((response) => response.json())
      .then((data) => {
          prepareChart("#chart", data);
      })
      .catch((error) => console.log(error));


function prepareChart(container, data) {
  const buttonDiv = d3.create("div")
    const button = d3.create("button")
    button.node().classList.add("replay-button");
    button.node().textContent = "Replay";
    const chartContainer = d3.select(container);
    chartContainer.node().append(buttonDiv.node());
    buttonDiv.node().append(button.node());

    drawChart(chartContainer, button, data);
}

async function drawChart(chartContainer, button, data) {

  button.on("click", () => {
    chartContainer.selectAll("svg").remove();
    drawChart(chartContainer, button, data);
  });

  const width = 800;
  const height = 720;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 30;
  const marginLeft = 40;

  const x = d3.scaleLinear()
      .domain(d3.extent([d3.min(data, d => d.unemployment_rate) - 0.2, d3.max(data, d => d.unemployment_rate) + 0.2])).nice()
      .range([marginLeft, width - marginRight]);

  const y = d3.scaleLinear()
      .domain(d3.extent([d3.min(data, d => d.vacancy_rate) - 0.2, d3.max(data, d => d.vacancy_rate) + 0.2])).nice()
      .range([height - marginBottom, marginTop]);

  const line = d3.line()
      .curve(d3.curveCatmullRom)
      .x(d => x(d.unemployment_rate))
      .y(d => y(d.vacancy_rate));

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

  const l = length(line(data));

  svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .call(d3.axisBottom(x).ticks(width / 80))
      .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
          .attr("y2", -height)
          .attr("stroke-opacity", 0.1))
      .call(g => g.append("text")
          .attr("x", width - 4)
          .attr("y", -4)
          .attr("font-weight", "bold")
          .attr("text-anchor", "end")
          .attr("fill", "currentColor")
          .text("Unemployment rate"));
  
  svg.append("g")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line").clone()
        .attr("x2", width)
        .attr("stroke-opacity", 0.1))
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 4)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text("Job vacancy rate"));

  svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", 2.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-dasharray", `0,${l}`)
      .attr("d", line)
      .transition()
        .duration(5000)
        .ease(d3.easeLinear)
        .attr("stroke-dasharray", `${l},${l}`);

  const circles = svg.append("g")
      .attr("fill", "white")
      .attr("stroke", "black")
      .attr("stroke-width", 2)
      .selectAll("circle")
      .data(data)
      .join("circle")
        .attr("cx", d => x(d.unemployment_rate))
        .attr("cy", d => y(d.vacancy_rate))
        .attr("r", 1);
  
  const labelBox = svg.append("g")
          .selectAll("rect")
          .data(data)
          .join("rect")
            .attr("transform", d => {
              if (d.date.endsWith("Q4") & (Number(d.date.slice(0,4) % 2 != 0) | Number(d.date.slice(0,4) == 2010))) {
                return `translate(${x(d.unemployment_rate) - 2},${y(d.vacancy_rate) - 14})`
              }
            })
            .attr("width", (d) => {
              if (d.date.endsWith("Q4") & (Number(d.date.slice(0,4) % 2 != 0) | Number(d.date.slice(0,4) == 2010))) {
                    return 50;
                  } else {
                    return 0;
                  }
            })
            .attr("height", d => 25)
            .attr("fill-opacity", 0);

  const label = svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 11)
      .attr("font-weight", "bold")
      .selectAll()
      .data(data)
      .join("text")
        .attr("transform", d => {
          if (d.date.endsWith("Q4") & (Number(d.date.slice(0,4) % 2 != 0) | Number(d.date.slice(0,4) == 2010))) {
            return `translate(${x(d.unemployment_rate)},${y(d.vacancy_rate)})`
          }
        })
        .attr("fill-opacity", 0)
        .text(d => d.date)
          .attr("stroke", "transparent")
          .attr("paint-order", "stroke")
          .attr("fill", "currentColor")
          .each(function(d) {
            const t = d3.select(this);
            t.attr("text-anchor", "start").attr("dx", "0.3em");
          });

  label.transition()
      .delay((d, i) => length(line(data.slice(0, i + 1))) / l * (5000 - 125))
      .attr("fill-opacity", 1);

  labelBox.transition()
     .delay((d, i) => length(line(data.slice(0, i + 1))) / l * (5000 - 125))
     .attr("fill", "white")
     .attr("stroke", "black")
     .attr("fill-opacity", 0.9);
  
  circles.transition()
     .delay((d, i) => length(line(data.slice(0, i + 1))) / l * (5000 - 125))
     .attr("r", (d) => {
          if (d.date.endsWith("Q4") & (Number(d.date.slice(0,4) % 2 != 0) | Number(d.date.slice(0,4) == 2010))) {
            return 5;
          } else {
            return 3;
          }
        })
     .attr("fill", (d) => {
            if (d.date.endsWith("Q4") & (Number(d.date.slice(0,4) % 2 != 0) | Number(d.date.slice(0,4) == 2010))) {
              return "black";
            } else {
              return "white";
            }
        });
  
  chartContainer.node().append(svg.node());

}

function length(path) {
  return d3.create("svg:path").attr("d", path).node().getTotalLength()
}
