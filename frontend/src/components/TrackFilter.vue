<template>
    <b-container class="text-left mb-5">
        <b-row>
            <b-col cols=4>
                <b-form-select v-model="selected" :options="options"></b-form-select>
            </b-col>
        </b-row>
    </b-container>
</template>


<script>
export default {
    name: 'TrackFilter',
    data: () => ({
      selected: 'days',
      options: [
          { value: 'days', text: 'Tracks played in the last x days'},
          { value: 'date', text: 'Tracks played between two dates'}
      ]
    })
}
</script>
