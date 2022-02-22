$(document).ready(function () {


    <!--Basic Pie echarts init-->

    var dom = document.getElementById("basic-Pie");
    var bpChart = echarts.init(dom);

    var app = {};
    option = null;
    option = {
        textStyle: {
            fontSize: 20

        },
        color: ['#26DAD2', '#FC6180', '#FAD9AA'],
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            textStyle: {
                fontSize: 15
            },
            data: ['Revisados', 'No revisados', 'Externos']
        },
        calculable: true,
        series: [
            {
                name: 'Revisiones',
                type: 'pie',
                radius: '60%',
                center: ['50%', '60%'],

                data: [
                    {value: 352, name: 'Revisados'},
                    {value: 310, name: 'No revisados'},
                    {value: 234, name: 'Externos'}
                ]
            }
        ]
    };

    if (option && typeof option === "object") {
        bpChart.setOption(option, false);
    }


    /**
     * Resize chart on window resize
     * @return {void}
     */
    window.onresize = function () {
        // chartOne.resize();
        // myChart.resize();
        // rainChart.resize();
        // nbChart.resize();
        bpChart.resize();
        // npChart.resize();
        // dnutChart.resize();
        // bsChart.resize();
        // rdChart.resize();
        // gaugeChart.resize();
    };


});