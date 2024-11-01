<template>
    <canvas ref="lineChart"></canvas>
</template>
  
<script>
import { Line } from 'chart.js/auto'

export default {
    props: ['chartData'],
    mounted() {
        new Line(this.$refs.lineChart, {
            data: this.chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
            },
        })
    }
}
</script>
  
<style scoped>
canvas {
    width: 100% !important;
    height: 100% !important;
}
</style>
  