<template>
  <div id="app">
    <!-- <ChartComponent/> -->
    <ScatterChartContainer></ScatterChartContainer>
  </div>
</template>

<script>
// import ChartComponent from './components/Chart.vue'
import ScatterChartContainer from './components/GraphContainer.vue'

export default {
  name: 'app',
  components: {
    // ChartComponent,
    ScatterChartContainer
  }
}
</script>

<style>
@import url("assets/bootstrap.min.css");

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 120px;
}
</style>
