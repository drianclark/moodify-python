<template>
  <div id="app">
    <ChartComponent/>
  </div>
</template>

<script>
import ChartComponent from './components/Chart.vue'

export default {
  name: 'app',
  components: {
    ChartComponent
  }
}
</script>

<style>
@import url("assets/bootstrap.min.css");

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 120px;
}
</style>
