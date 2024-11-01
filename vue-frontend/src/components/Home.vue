<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
      <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">
        GitHub Repository Activity Visualizer
      </h1>

      <!-- Input for GitHub URL -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Enter your GitHub repository URL:</label>
        <input type="text" placeholder="https://github.com/owner/repo"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-200"
          v-model="githubUrl" />
        <button class="w-full mt-4 bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
          @click="fetchData">
          Fetch Data
        </button>
      </div>

      <!-- Charts for Visualizing Data -->
      <div v-if="commitChartOptions" class="mb-8">
        <h2 class="text-lg font-semibold mb-2">Commit Frequency</h2>
        <v-chart :option="commitChartOptions" style="height: 400px; width: 100%;"></v-chart>
      </div>

      <div v-if="contributorChartOptions" class="mb-8">
        <h2 class="text-lg font-semibold mb-2">Contributor Stats</h2>
        <v-chart :option="contributorChartOptions" style="height: 400px; width: 100%;"></v-chart>
      </div>

      <div v-if="issuesChartOptions" class="mb-8">
        <h2 class="text-lg font-semibold mb-2">Issues Count</h2>
        <v-chart :option="issuesChartOptions" style="height: 400px; width: 100%;"></v-chart>
      </div>

      <div v-if="pullRequestsChartOptions" class="mb-8">
        <h2 class="text-lg font-semibold mb-2">Pull Requests Count</h2>
        <v-chart :option="pullRequestsChartOptions" style="height: 400px; width: 100%;"></v-chart>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent, LegendComponent } from 'echarts/components'
import ECharts from 'vue-echarts'
import axios from 'axios'

use([CanvasRenderer, BarChart, PieChart, GridComponent, TooltipComponent, TitleComponent, LegendComponent])

export default defineComponent({
  components: { VChart: ECharts },
  data() {
    return {
      githubUrl: '',
      owner: '',
      repo: '',
      commitChartOptions: null,
      contributorChartOptions: null,
      issuesChartOptions: null,
      pullRequestsChartOptions: null,
    }
  },
  methods: {
    extractRepoDetails() {
      const regex = /^https:\/\/github\.com\/([^/]+)\/([^/]+)$/
      const match = this.githubUrl.match(regex)
      if (match) {
        this.owner = match[1]
        this.repo = match[2]
      } else {
        alert("Please enter a valid GitHub repository URL")
      }
    },
    async fetchData() {
      this.extractRepoDetails()
      if (!this.owner || !this.repo) return

      try {
        await Promise.all([this.getCommit(), this.getContributorStats(), this.getIssues(), this.getPullRequests()])
      } catch (error) {
        console.error("Error fetching data:", error)
      }
    },
    async getCommit() {
      const apiUrl = `http://localhost:8000/commits?owner=${this.owner}&repo=${this.repo}`
      try {
        const response = await axios.get(apiUrl)
        const commitData = response.data.map((item, index) => ({ week: `Week ${index + 1}`, count: item.commit_count }))
        this.commitChartOptions = {
          title: { text: 'Commit Frequency' },
          tooltip: {},
          xAxis: { type: 'category', data: commitData.map(item => item.week) },
          yAxis: { type: 'value' },
          series: [{ type: 'bar', data: commitData.map(item => item.count) }]
        }
      } catch (error) {
        console.error("Error fetching commits:", error)
      }
    },
    async getContributorStats() {
      const apiUrl = `http://localhost:8000/contributors?owner=${this.owner}&repo=${this.repo}`
      try {
        const response = await axios.get(apiUrl)
        const contributorData = response.data.map(contrib => ({ name: contrib.login, value: contrib.contributions }))
        this.contributorChartOptions = {
          title: { text: 'Contributor Stats' },
          tooltip: { trigger: 'item' },
          legend: { orient: 'vertical', left: 'left' },
          series: [{ type: 'pie', radius: '50%', data: contributorData }]
        }
      } catch (error) {
        console.error("Error fetching contributors:", error)
      }
    },
    async getIssues() {
      const apiUrl = `http://localhost:8000/issues?owner=${this.owner}&repo=${this.repo}`
      try {
        const response = await axios.get(apiUrl)
        const issuesData = [{ name: 'Open Issues', value: response.data.open }, { name: 'Closed Issues', value: response.data.closed }]
        this.issuesChartOptions = {
          title: { text: 'Issues Count' },
          tooltip: { trigger: 'item' },
          legend: { data: ['Open Issues', 'Closed Issues'] },
          series: [{ type: 'bar', data: issuesData }]
        }
      } catch (error) {
        console.error("Error fetching issues:", error)
      }
    },
    async getPullRequests() {
      const apiUrl = `http://localhost:8000/pull_requests?owner=${this.owner}&repo=${this.repo}`
      try {
        const response = await axios.get(apiUrl)
        const pullRequestData = [{ name: 'Open PRs', value: response.data.open }, { name: 'Merged PRs', value: response.data.merged }]
        this.pullRequestsChartOptions = {
          title: { text: 'Pull Requests Count' },
          tooltip: { trigger: 'item' },
          legend: { data: ['Open PRs', 'Merged PRs'] },
          series: [{ type: 'bar', data: pullRequestData }]
        }
      } catch (error) {
        console.error("Error fetching pull requests:", error)
      }
    }
  }
})
</script>

<style>
.chart-container {
  width: 100%;
  margin-top: 2rem;
}
</style>
