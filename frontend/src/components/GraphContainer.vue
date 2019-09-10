<template>
  <div class="container">
    <scatter-chart
      v-if="loaded"
      :chartdata="chartdata"
      :options="options"/>
  </div>
</template>

<script>
import ScatterChart from './Graph.vue'
import axios from 'axios';

export default {
  name: 'ScatterChartContainer',
  components: { ScatterChart },
  data: () => ({
    loaded: false,
    chartdata: null,
    options: null
  }),
  async mounted () {
    this.loaded = false
    try {
      const response = await axios.get("http://localhost:5000/api/get_tracks");

      let data = []
      let index = 0

      for (let track of response.data) {
          data.push({x:index, y:track.valence})
          index +=1;
      }

      let data_object = {
          datasets: [{
              data: data,
              fill: false,
              showLine: true,
              lineTension: 0,
              borderColor: 'rgba(0, 128, 255, 1)'
          }]
      }

      this.chartdata = data_object
      this.options = {
          responsive: true,
          legend: {
              display: false
          },
          tooltips: {
              enabled: true,
              mode: 'index',
              position: 'nearest',
              // custom: customTooltips,
              callbacks: {
                  label: function(tooltipItem, data) {
                      var spotifyid = response.data[tooltipItem.index].spotifyid;
                      console.log(tooltipItem.index);

                      return spotifyid;
                  }
              }
          }
      }

      this.loaded = true

    } catch (e) {
      console.error(e)
    }
  }
}
</script>
