	function exist(array, data){
		for( i = 0; i < array.length; i++){
			if(data == array[i]){
				return true;
			}
		}
		return false;
	}

	// Get a subset of the data based on the group
	function getFilteredData_Constructor(data, ConstructorName) {
		return data.filter(function(d) { return d.ConstructorName === ConstructorName; });
	}

	function getFilteredData_Year(data, StartYear, EndYear) {
		return data.filter(function(d) { 
			var status = false;
			_tempYearArray = d.Years.split(",");
			for(i = 1; i < _tempYearArray.length; i++){
				if((parseInt(_tempYearArray[i]) >= parseInt(StartYear)) && (parseInt(_tempYearArray[i]) <= parseInt(EndYear)))
					status = true;
					break; 
				}
			return status;
			});
	}

	const SVG_WIDTH = 500;
	const SVG_HEIGHT = 500;
	const BAR_GAP = SVG_WIDTH/12;
	const INNERBAR_OFFSET = BAR_GAP/3;
	const BAR_WIDTH = BAR_GAP * 0.6;
	var colorMin = 1;

	var colorMax = 8;

	var lengthMin = 0;

	var lengthMax = 1000;

	var margin ={top: 20, right: 20, bottom: 20, left: 20},
		width = SVG_WIDTH - margin.left - margin.right,
		height = SVG_HEIGHT - margin.top - margin.bottom;

	var length = d3.scale.linear()
					.range([0, width]);

	var invertLength = d3.scale.linear()
					.range([lengthMin, lengthMax]).domain([0, width]);

	// console.log(invertLength(4));

	// var color = d3.scale.linear()
	//       			// .interpolate(d3.interpolateHcl)
 //      				.range([d3.rgb("#99000D"), d3.rgb('#fff5f0')]);
	// 				// .range(["red", "green"]);
	// color.domain([colorMin, colorMax]);

	function color(componentType){
		if(componentType.includes("stroke")){
			return "#99000D";
		}
		if(componentType.includes("inner_bar")){
			return "#FC9272";
		}
		if(componentType.includes("outer_bar")){
			return "#000000"
		}
	}
	// function color(value){
	// 	switch(value){
	// 		case 1: return "#99000D"; break;
	// 		case 2: return "#CB181D"; break;
	// 		case 3: return "#EF3B2C"; break;
	// 		case 4: return "#FB6A4A"; break;
	// 		case 5: return "#FC9272"; break;
	// 		case 6: return "#FCBBA1"; break;
	// 		case 7: return "#FEE0D2"; break;
	// 		case 8: return "#fff5f0"; break;
	// 	}
	// }

	// length.domain([lengthMin, lengthMax]);
	d3.select("visualisation_1").append("h2").text("Hello World")
	console.log("visualisation_1")

	var svg = d3.select("#visualisation_1")
				.append("svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom);

	// Define the div for the tooltip
	var div = d3.select("#visualisation_1").append("div")	
	    .attr("class", "tooltip")				
	    .style("opacity", 0)
	    .style("font", "10px times");

	// var $BarcodeContainerSelector = querySelector("barcodeContainer");

	d3.csv("/static/data/PreprocessedDataset2.csv", function(data){
		// console.log(error);
		// console.log(data);
		DriverIDArray = [];
		YearsArray = [];
		// Turn data to usable format
		data.forEach(function(d){
			// console.log(parseInt(d.Pattern_1.split("_")[0]));
			// console.log((d.Pattern_1.split("_"))[1].replace("%",""));
			if(exist(DriverIDArray, d.DriverId)){
				
			}else{
				DriverIDArray.push(d.DriverId);
			}
		});

		function enterBars(data){
			var i1 = -1;
			var i2 = -1;
			for(var i = 0; i < data.length; i++){
				g = svg.append("g").attr("id", String(i));
				var d = data[i];
				// var xMove = 0.0;
				// var d = data[i];
				length.domain([d.FirstLapChangeMin, d.FirstLapChangeMax]);
				g.append("rect")
					.attr("transform",function(){
						return "translate(" + [0, i*BAR_GAP + INNERBAR_OFFSET] + ")";
					})
					.attr("width", width)
					.attr("height", BAR_WIDTH)
					.attr("fill", function(){
						return color("inner_bar");})
					// .on("mouseover", handleMouseOver)
					// .on("mouseout", handleMouseOut)
				// for (var property in data[i]) {
				//     if (data[i].hasOwnProperty(property)) {
				//     	if(String(property).includes("Pattern_")){
				//     		// console.log(String(data[i][property]));

				// 			g.append("rect")
				// 			.attr("transform",function(){
				// 				return "translate(" + [0, i*BAR_GAP + INNERBAR_OFFSET] + ")";
				// 			})
				// 			.attr("width", width)
				// 			.attr("height", BAR_WIDTH)
				// 			.attr("fill", function(){
				// 				return color("inner_bar");})
				// 			.on("mouseover", handleMouseOver)
				// 			.on("mouseout", handleMouseOut)
				//     	}
				//     }
				// }
			}
		}


		  enterBars(data);

	// Create Event Handlers for mouse
	function handleMouseOver(d) {  // Add interactivity
		div.transition()		
            .duration(200)		
            .style("opacity", .9);		
        div	.style("width", 60)
        	.style("height", 70).html("Min: ")
            .style("left", (d3.event.pageX + 10) + "px")		
            .style("top", (d3.event.pageY - 28) + "px");	
        
	      // Use D3 to select element, change color and size
  	      d3.select(this).attr(
	      	{height: BAR_GAP*0.8}
	      	);
  	      console.log(d3.select(this).attr("id"));
	    }

	function handleMouseOut(d){

		div.transition()		
                .duration(500)		
                .style("opacity", 0);	
	      // Use D3 to select element, change color back to normal
	      d3.select(this).attr(
	      	{height: BAR_GAP*0.6}
	      	);
	    }
	});
