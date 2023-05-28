// {{ values|json_script:"djangoData" }}
$( document ).ready(function() {


    var chart_info = document.getElementById("chart-info");
    var type = chart_info.dataset.type;
    if (chart_info.dataset.type == "pie" || chart_info.dataset.type == "bar"){

        if (type == "pie"){
            google.charts.load('current', {'packages':['controls','corechart']});
        }
        else if (type == "bar"){
            google.charts.load('current', {'packages':['bar']});
        }
            google.charts.setOnLoadCallback(drawChart);

            function drawChart(discerner) {
                // var djangoData = JSON.parse('{{values|safe}}')
            var chartDataElement = document.getElementById("chart-data");
            var djangoData = JSON.parse(chartDataElement.dataset.values);
            var data = google.visualization.arrayToDataTable(djangoData);

            // console.log(djangoRes, "DO WE HAVE DATA?")
            var options = {
                title: '',
                is3D: true,
            };

            let darkMode = localStorage.getItem('darkMode');
            let gDarkMode = localStorage.getItem('gDarkMode')


            const enableGDarkMode = () => {
                localStorage.setItem('gDarkMode', "enabled")
                options.backgroundColor = {fill: 'black'}
                options.legend = {textStyle: {color: 'white', fontSize: 16}}

                options.titleTextStyle	= {color: "white"}

                if (type == "pie"){
                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }

                else if (type == "bar"){
                    var chart = new google.charts.Bar(document.getElementById('bar-chart'));
                    //chart.draw(data, google.charts.Bar.convertOptions(options));
                    chart.draw(data, google.charts.Bar.convertOptions(options));
                }
            }

            const disableGDarkMode = () => {
                options.backgroundColor = {fill: "white"}
                options.legend = {textStyle: {color: 'black', fontSize: 16}}
                options.titleTextStyle	= {color: "black"}
                // options.colors = ['grey', 'black', 'orange', 'red', 'pink']
                // document.getElementById("piechart").classList.add("darkmode")
                localStorage.setItem('gDarkMode', null)

                if (type == "pie"){
                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }

                else if (type == "bar"){
                    var chart = new google.charts.Bar(document.getElementById('bar-chart'));
                    //chart.draw(data, google.charts.Bar.convertOptions(options));
                    chart.draw(data, google.charts.Bar.convertOptions(options));
                }

            }

            if (darkMode == "enabled"){
                enableGDarkMode();
            }else{
                disableGDarkMode();
            }

            



            }

            $("#dark-mode-toggle").on("click", function(){
                let gDarkMode = localStorage.getItem('gDarkMode')
                    if (gDarkMode == "enabled"){
                        drawChart("disable")
                        localStorage.setItem('darkMode', null)

                    }else{
                        drawChart("enable")
                        localStorage.setItem('darkMode', "enabled")
                    }
            });
        }else{
            google.charts.load('current', {packages: ['corechart', 'line']});
            google.charts.setOnLoadCallback(drawLineStyles);
            
            function drawLineStyles() {
                var chartDataElement = document.getElementById("chart-data");
                var djangoData = JSON.parse(chartDataElement.dataset.values);

                    var data = new google.visualization.DataTable();
                    data.addColumn('number', 'Day');
                    data.addColumn('number', 'Resolved');
                    data.addColumn('number', 'Unesolved');
                    var rows = djangoData.map(function(row) {
                        return [new Date(row[0]).getTime(), row[1], row[2]];
                      });
                    data.addRows(rows);
                    console.log(djangoData.length, "lengthy")
                    var options = {
                        hAxis: {
                        title: 'Days',
                        //curveType: 'function',

                        textStyle: {
                            color: '#01579b',
                            fontSize: 16,
                            fontName: 'Arial',
                            bold: true,
                            italic: true
                        },
                        titleTextStyle: {
                            color: '#01579b',
                            fontSize: 16,
                            fontName: 'Arial',
                            bold: false,
                            italic: true
                        }
                        },
                        vAxis: {
                        title: 'Tickets',
                        // curveType: 'function',
                        viewWindow : {
                            // min : 0,
                            // max : 1000
                        },
                        textStyle: {
                            color: '#1a237e',
                            fontSize: 16,
                            bold: true
                        },
                        titleTextStyle: {
                            color: '#1a237e',
                            fontSize: 24,
                            bold: true
                        }
                        },
                        colors: ['#a52714', '#097138']
                    };
                    var chart = new google.visualization.LineChart(document.getElementById('line-chart'));
                    chart.draw(data, options);
                    //chart.draw(data, google.charts.LineChart.convertOptions(options));

                    }
        }
        });
