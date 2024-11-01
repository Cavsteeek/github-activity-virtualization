<template>
    <canvas ref="barChart"></canvas>
</template>
  
<script>
import { Bar } from 'chart.js/auto'

export default {
    props: ['chartData'],
    mounted() {
        new Bar(this.$refs.barChart, {
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
  