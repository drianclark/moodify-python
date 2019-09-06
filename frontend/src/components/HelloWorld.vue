<template>
  <div class="hello">
      <b-container>
          <canvas id="myChart" width="200px" height="150px"></canvas>
      </b-container>

  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js';
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }

}

Chart.defaults.global.legend.display = false;

function get_tracks() {
    axios.get("http://localhost:5000/api/get_tracks")
        .then(function (response) {
            let data = []
            let index = 0
            for (let track of response.data) {
                data.push({x:index, y:track.valence})
                index +=1;
            }

            console.log(data)

            var ctx = document.getElementById('myChart').getContext('2d');
            var myLineChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        data: data,
                        fill: false,
                        showLine: true,
                        borderColor: 'rgba(0, 128, 255, 1)',
                        options: {
                            responsive: true,
                            tooltips: {
                                callbacks: {
                                    value: function(tooltipItem, data) {
                                        console.log("callback")
                                        var title = response.data[tooltipItem.datasetIndex].title;
                                        console.log(title);

                                        return title;
                                    }
                                }
                            }
                        }
                    }]
                }
            });

            return data;
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        });
}

window.onload = function() {
    // var ctx = document.getElementById('myChart').getContext('2d');
    console.log("onload")
    get_tracks()
    // var myLineChart = new Chart(ctx, {
    //     type: 'line',
    //     data: {
    //         datasets: [{
    //             data:  get_tracks(),
    //             borderColor: "#3e95cd"
    //         }]
    //     }
    // });

}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
