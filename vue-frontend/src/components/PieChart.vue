<template>
    <canvas ref="pieChart"></canvas>
</template>
  
<script>
import { Pie } from 'chart.js/auto'

export default {
    props: ['chartData'],
    mounted() {
        new Pie(this.$refs.pieChart, {
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
  