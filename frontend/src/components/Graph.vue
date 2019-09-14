<script>
import { Scatter, mixins } from 'vue-chartjs'
import axios from 'axios'

const { reactiveProp } = mixins

export default {
  extends: Scatter,
  mixins: [reactiveProp],
  props: ['options'],
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}

var accessToken;
getAccessToken();

function getAccessToken() {
    axios.get("http://localhost:5000/api/get_token")
        .then(token => {
            accessToken = token.data
            return token.data
        })
}
//
function getTrackInfo(spotifyid) {
    // interceptor for handling authentication errors

    var refresh_interceptor = axios.interceptors.response.use(null, (error) => {
          if (error.config && error.response && error.response.status === 401) {
            return axios.get("http://localhost:5000/api/get_token").then((token) => {
              error.config.headers.Authorization = "Bearer " + token.data
              // console.log(error.config)
              return axios.request(error.config);
            });
          }

          return Promise.reject(error);
        });

    return axios.get("https://api.spotify.com/v1/tracks/" + spotifyid,
                { headers: {'Authorization':'Bearer ' + accessToken}})

}

var customTooltips = function(tooltip) {
	// Tooltip Element
	var tooltipEl = document.getElementById('chartjs-tooltip');

	if (!tooltipEl) {
		tooltipEl = document.createElement('div');
		tooltipEl.id = 'chartjs-tooltip';
		tooltipEl.innerHTML = '<div></div>';
		this._chart.canvas.parentNode.appendChild(tooltipEl);
	}

	// Hide if no tooltip
	if (tooltip.opacity === 0) {
		tooltipEl.style.opacity = 0;
		return;
	}

	// Set caret Position
	tooltipEl.classList.remove('above', 'below', 'no-transform');
	if (tooltip.yAlign) {
		tooltipEl.classList.add(tooltip.yAlign);
	} else {
		tooltipEl.classList.add('no-transform');
	}

	// Set Text
	if (tooltip.body) {
        var innerHtml;
		var titleLines = tooltip.title || [];
		let spotifyid = tooltip.body[0].lines[0];
        console.log(spotifyid)
        let trackInfo =
            getTrackInfo(spotifyid)
                .then(response => {
                    let artists = []

                    let title = response.data.name;
                    let imgUrl = response.data.album.images[1].url
                    for (let artist of response.data.artists) {
                        artists.push(artist.name)
                    }

                    innerHtml = '<h3 class="track-title mb-0">' + title + '</h2>';
                    innerHtml += '<h5 class="artists mb-3">' + artists.join(', ') + '</h5>'
                    innerHtml += '<img src= ' + imgUrl + '>'

    				var tableRoot = tooltipEl.querySelector('div');
    				tableRoot.innerHTML = innerHtml;

                    return "trackInfo";
                })
	}

	var positionY = this._chart.canvas.offsetTop;
	var positionX = this._chart.canvas.offsetLeft;

	// Display, position, and set styles for font
	tooltipEl.style.opacity = 1;
	tooltipEl.style.left = positionX + tooltip.caretX + 'px';
	tooltipEl.style.top = positionY + tooltip.caretY + 'px';
	tooltipEl.style.fontFamily = tooltip._bodyFontFamily;
	tooltipEl.style.fontSize = tooltip.bodyFontSize + 'px';
	tooltipEl.style.fontStyle = tooltip._bodyFontStyle;
};

</script>
