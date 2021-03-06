<template>
    <div class="background">
        <section class="content">
            <b-row>
                <b-col>
                    <h1>Trends</h1>
                </b-col>
                <b-col cols="auto">
                    <b-button
                        :disabled="trackUpdateLoading"
                        class="row mb-5 ml-3"
                        v-on:click="triggerTracksUpdate"
                        variant="outline-primary"
                    >
                        Update DB
                        <b-spinner
                            v-if="trackUpdateLoading"
                            small
                            class="ml-2"
                            type="grow"
                            variant="primary"
                            label="Loading..."
                        ></b-spinner>
                    </b-button>
                </b-col>
            </b-row>

            <TrackFilter
                v-on:days-filter="updateChartDays"
                v-on:date-filter="updateChartDate"
                :format="dateFormatter"
            />

            <scatter-chart
                v-if="loaded"
                :height="150"
                :options="options"
                :chart-data="chartdata"
            />

            <div class="sr-only" role="main">
                <li v-for="(track, i) in loadedTracks" :key="i">
                    Played {{track.title}} with valence {{track.valence}} on {{track.date}}   
                </li>
            </div>

        </section>
    </div>
</template>

<style lang="scss">
$primaryFont: Raleway, sans-serif;
$secondaryFont: Montserrat, sans-serif;

.background {
    // background-image: linear-gradient(to right, #56ab2f, #95cc3e),
    //     linear-gradient(to bottom, #8fca2f, #608e15);
    // background-blend-mode: lighten;
    background-image: url("../assets/background.png");
    background-size: cover;
    height: 100%;
}

.content {
    padding: 10vw 5vw 0 5vw;
    text-align: left;

    h1 {
        font-family: $secondaryFont;
    }

    ol {
        padding-left: 1rem;
    }

    a {
        text-decoration: none;
        color: white;
        transition: ease-in-out 0.2s;
    }

    a:hover {
        color: rgb(206, 206, 206);
    }
}
a {
    color: #42b983;
}

#scatter-chart {
    padding-bottom: 2em;
}

#chartjs-tooltip {
    opacity: 1;
    position: absolute;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 10px;
    border-radius: 3px;
    -webkit-transition: all 0.1s ease;
    transition: all 0.1s ease;
    pointer-events: none;
    -webkit-transform: translate(-50%, 0);
    transform: translate(-50%, 0);
}

.track-title {
    font-family: $primaryFont;
    font-size: 22px;
    text-align: left;
}

.artists {
    font-family: $primaryFont;
    text-align: left;
    font-size: 16px;
}
</style>

<script>
import Chart from "chart.js";
import ScatterChart from "@/components/Graph.vue";
import TrackFilter from "@/components/TrackFilter.vue";
import axios from "axios";
import moment from "moment";

const baseURL = process.env.VUE_APP_URL;

const chunk = (arr, size) =>
    Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
        arr.slice(i * size, i * size + size)
    );

var tracksinfo = {};

Chart.Tooltip.positioners.custom = function(elements, position) {
    let yPos = position.y;
    let xPos = position.x;

    if (position.y > elements[0]._chart.height / 3) {
        yPos += elements[0]._chart.height / 3 - position.y;
    }

    if (position.x < 150) {
        xPos = 150;
    } else if (position.x > elements[0]._chart.width - 150) {
        xPos = elements[0]._chart.width - 150;
    }

    return {
        x: xPos,
        y: yPos
    };
};

export default {
    name: "Tracker",
    components: {
        ScatterChart,
        TrackFilter
    },
    methods: {
        updateChartDays: async function(numberOfDays) {
            this.loaded = false;
            this.loadedTracks = [];

            let res = await axios.get(baseURL + "/api/get_tracks_by_days", {
                            params: {
                                days: numberOfDays
                            }
            });

            let tracks = await res.data;
            await this.updateChartInfo(tracks, res);
            this.loaded = true;

            
        },

        updateChartDate: async function(startDate, endDate) {
            this.loaded = false;
            this.loadedTracks = [];

            let res = await axios.get(baseURL + "/api/get_tracks_by_date", {
                            params: {
                                startDate: moment(startDate).format("YYYY-MM-DD"),
                                endDate: moment(endDate).format("YYYY-MM-DD")
                            }
            });

            let tracks = await res.data;
            await this.updateChartInfo(tracks, res);
            this.loaded = true;
        },

        updateTracksInfo: async function(spotifyIDs) {
            for (let idArray of chunk(spotifyIDs, 50)) {
                let info = await getTracksInfo(idArray.join(","));

                for (let trackInfo of info) {
                    let spotifyID = trackInfo.id;
                    let currentInfo = {
                        artists: [],
                        title: trackInfo.name,
                        imgUrl: trackInfo.album.images[1].url
                    };

                    for (let artist of trackInfo.artists) {
                        currentInfo.artists.push(artist.name);
                    }

                    tracksinfo[spotifyID] = currentInfo;
                }
            }

        },

        updateChartInfo: async function(tracks, response) {
            let data = [];
            let index = 0;
            let spotifyIDs = [];

            for (let track of tracks) {
                data.push({
                    x: moment(track.playDate).toDate(),
                    y: track.valence
                });
                spotifyIDs.push(track.spotifyID);

                track.playDate = moment(track.playDate).format("MMMM Do");
                this.loadedTracks.push(track);
                index += 1;

            }

            await this.updateTracksInfo(spotifyIDs);

            let data_object = {
                datasets: [
                    {
                        data: data,
                        fill: false,
                        showLine: true,
                        lineTension: 0,
                        borderColor: "white"
                    }
                ]
            };

            this.chartdata = data_object;
            this.updateTooltips(response);
            this.configureAxes();
        },

        dateFormatter: function(date) {
            return moment(date).format("DD-MM-YYYY");
        },

        triggerTracksUpdate: function() {
            this.trackUpdateLoading = true;
            axios.get(baseURL + "/api/update_tracks").then(response => {
                this.trackUpdateLoading = false;
            });
        },

        updateTooltips: function(response) {
            this.options.tooltips = {
                enabled: false,
                mode: "index",
                position: "custom",
                custom: customTooltips,
                callbacks: {
                    label: function(tooltipItem, data) {
                        let spotifyid =
                            response.data[tooltipItem.index].spotifyID;
                        return spotifyid;
                    }
                }
            };
        },

        configureAxes: function() {
            this.options.legend = {
                display: false
            }

            this.options.scales = {
                gridLines: {
                    color: "white"
                },
                xAxes: [
                    {
                        type: "time",
                        distribution: "series",
                        time: {
                            minUnit: "day"
                        },
                        bounds: "ticks",
                        ticks: {
                            minRotation: 90,
                            fontColor: "rgba(255, 255, 255, 0.8)",
                            fontFamily: "'Raleway', sans-serif",
                            source: "label"
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.2)",
                            zeroLineColor: "rgba(255, 255, 255, 0.2)"
                        }
                    }
                ],
                yAxes: [
                    {
                        ticks: {
                            stepSize: 0.5,
                            maxTicksLimit: 3,
                            fontColor: "rgba(255, 255, 255, 0.8)"
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.2)",
                            zeroLineColor: "rgba(255, 255, 255, 0.2)"
                        }
                    }
                ]
            };
        }
    },
    data: () => ({
        loaded: false,
        chartdata: null,
        options: {},
        trackUpdateLoading: false,
        loadedTracks: []
    }),

    async mounted() {
        this.loaded = false;

        let res = await axios.get(baseURL + "/api/get_tracks_by_days", {
                        params: {
                            days: 1
                        }
        });

        let tracks = await res.data;
        await this.updateChartInfo(tracks, res);
        this.loaded = true;
    }
};

var accessToken;
getAccessToken();

function getAccessToken() {
    axios.get(baseURL + "/api/get_token").then(token => {
        accessToken = token.data;
        return token.data;
    });
}

async function getTracksInfo(spotifyids) {
    let res = await axios.get(baseURL + '/api/get_token');
    let accessToken = await res.data;

    let res1 = await axios.get("https://api.spotify.com/v1/tracks", {
        headers: { Authorization: "Bearer " + accessToken },
        params: { ids: spotifyids }
    });

    return res1.data.tracks;
}

var customTooltips = function(tooltip) {
    // Tooltip Element
    var tooltipEl = document.getElementById("chartjs-tooltip");

    if (!tooltipEl) {
        tooltipEl = document.createElement("div");
        tooltipEl.id = "chartjs-tooltip";
        tooltipEl.innerHTML = "<div></div>";
        this._chart.canvas.parentNode.appendChild(tooltipEl);
    }

    // Hide if no tooltip
    if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
    }

    // Set caret Position
    tooltipEl.classList.remove("above", "below", "no-transform");
    if (tooltip.yAlign) {
        tooltipEl.classList.add(tooltip.yAlign);
    } else {
        tooltipEl.classList.add("no-transform");
    }

    // Set Text
    if (tooltip.body) {
        var innerHtml;
        var titleLines = tooltip.title || [];
        let spotifyid = tooltip.body[0].lines[0];

        let artists = [];

        let title = tracksinfo[spotifyid].title;
        let imgUrl = tracksinfo[spotifyid].imgUrl;
        for (let artist of tracksinfo[spotifyid].artists) {
            artists.push(artist);
        }

        innerHtml = '<h3 class="track-title mb-0">' + title + "</h2>";
        innerHtml += '<h5 class="artists mb-3">' + artists.join(", ") + "</h5>";
        innerHtml += "<img src= " + imgUrl + ">";

        var tableRoot = tooltipEl.querySelector("div");
        tableRoot.innerHTML = innerHtml;
    }

    var positionY = this._chart.canvas.offsetTop;
    var positionX = this._chart.canvas.offsetLeft;

    // Display, position, and set styles for font
    tooltipEl.style.opacity = 1;
    tooltipEl.style.left = positionX + tooltip.caretX + "px";
    tooltipEl.style.top = positionY + tooltip.caretY + "px";
    tooltipEl.style.fontFamily = tooltip._bodyFontFamily;
    tooltipEl.style.fontSize = tooltip.bodyFontSize + "px";
    tooltipEl.style.fontStyle = tooltip._bodyFontStyle;
};
</script>
