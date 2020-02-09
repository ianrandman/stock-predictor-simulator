import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import React from 'react';

am4core.useTheme(am4themes_animated);

class CandleStick extends React.Component{
  componentDidMount() {
    let chart = am4core.create("chartdiv", am4charts.XYChart);

    chart.paddingRight = 20;

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

    let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;

    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;

    let series = chart.series.push(new am4charts.CandlestickSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "close";
    series.dataFields.openValueY = "open";
    series.dataFields.lowValueY = "low";
    series.dataFields.highValueY = "high";
    series.simplifiedProcessing = true;
    series.tooltipText = "Open:${openValueY.value}\nLow:${lowValueY.value}\nHigh:${highValueY.value}\nClose:${valueY.value}";

    chart.cursor = new am4charts.XYCursor();

// a separate series for scrollbar
    let lineSeries = chart.series.push(new am4charts.LineSeries());
    lineSeries.dataFields.dateX = "date";
    lineSeries.dataFields.valueY = "close";
// need to set on default state, as initially series is "show"
    lineSeries.defaultState.properties.visible = false;

// hide from legend too (in case there is one)
    lineSeries.hiddenInLegend = true;
    lineSeries.fillOpacity = 0.5;
    lineSeries.strokeOpacity = 0.5;

    let scrollbarX = new am4charts.XYChartScrollbar();
    scrollbarX.series.push(lineSeries);
    chart.scrollbarX = scrollbarX;

    chart.data = this.props.data;
    this.chart = chart;
  }

  componentWillUnmount() {
    if(this.chart){
      this.chart.dispose();
    }
  }

  render() {
    return (
      <div id="chartdiv" style={{width: "100%", height: "500px"}}/>
    );
  }
}

export default CandleStick;