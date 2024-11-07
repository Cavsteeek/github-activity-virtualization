<template>
  <div class="min-h-screen relative bg-gray-100">
    <div class="container mx-auto px-4 py-8">
      <div class="bg-white shadow-lg rounded-lg p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">
          GitHub Repository Activity Visualizer
        </h1>

        <!-- Input Section -->
        <div class="mb-8">
          <label class="block text-sm font-medium text-gray-700 mb-2">Enter your GitHub repository URL:</label>
          <div class="flex gap-4">
            <input type="text" placeholder="https://github.com/owner/repo"
              class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-200"
              v-model="githubUrl" v-on:keyup.enter="fetchData" />
            <button class="px-6 bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
              @click="fetchData">
              Fetch Data
            </button>
          </div>
        </div>

        <!-- Extend the commit frequency part and also add notifs, find another name for it -->
        <!-- Charts Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Commit Frequency Chart - spans across two columns on medium screens and above -->
          <div v-if="commitChartOptions" class="col-span-1 md:col-span-2 bg-white rounded-lg p-4 shadow">
            <h2 class="text-xl font-semibold mb-4">Commit Frequency</h2>
            <v-chart :option="commitChartOptions" :autoresize="true" class="w-full h-[500px]" />
          </div>

          <!-- Contributor Stats Chart - placed on a new row after Commit Frequency -->
          <div v-if="contributorChartOptions" class="col-span-1 md:col-span-2 bg-white rounded-lg p-4 shadow">
            <h2 class="text-xl font-semibold mb-4">Contributor Stats</h2>
            <v-chart :option="contributorChartOptions" :autoresize="true" class="w-full h-[650px]" />
          </div>

          <!-- Issues Chart -->
          <div v-if="issuesChartOptions" class="bg-white rounded-lg p-4 shadow">
            <h2 class="text-xl font-semibold mb-4">Issues Count</h2>
            <v-chart :option="issuesChartOptions" :autoresize="true" class="w-full h-[400px]" />
          </div>

          <!-- Pull Requests Chart -->
          <div v-if="pullRequestsChartOptions" class="bg-white rounded-lg p-4 shadow">
            <h2 class="text-xl font-semibold mb-4">Pull Requests Count</h2>
            <v-chart :option="pullRequestsChartOptions" :autoresize="true" class="w-full h-[400px]" />
          </div>
        </div>
      </div>
    </div>
    <!-- Footer -->
    <!-- <footer class="mt-8 absolute bottom-5 flex justify-center w-screen items-center text-center text-gray-500 text-sm">
      <p>Cavsteek 2024</p>
    </footer> -->

    <!-- Footer -->
    <footer class="text-center text-gray-500 text-md font-bold py-4">
      &copy; Cavsteek 2024
    </footer>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
  ToolboxComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import axios from 'axios'

use([
  CanvasRenderer,
  BarChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
  ToolboxComponent
])

export default defineComponent({
  name: 'GithubVisualizer',
  components: {
    VChart
  },
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
      const regex = /^https:\/\/github\.com\/([^/]+)\/([^/]+)\/?$/;
      const match = this.githubUrl.match(regex);
      if (match) {
        this.owner = match[1];
        this.repo = match[2];
        return true;
      }
      alert("Please enter a valid GitHub repository URL");
      return false;
    },
    async fetchData() {
      if (!this.extractRepoDetails()) return;

      try {
        await axios.get(`http://localhost:8000/check_repo?owner=${this.owner}&repo=${this.repo}`);

        // If the response was successful, fetch other data
        await Promise.all([
          this.getCommitFrequency(),
          this.getContributorStats(),
          this.getIssues(),
          this.getPullRequests()
        ]);
      } catch (error) {

        console.error("Error fetching data:", error);

        if (error.response) {
          alert(`Error fetching repository data: ${error.response.data.detail || error.message}`);
        } else {
          alert("Error fetching repository data. Please try again.");
        }
      }
    },

    async getCommitFrequency() {  // method for commit frequency
      try {
        const response = await axios.get(`http://localhost:8000/commit_frequency?owner=${this.owner}&repo=${this.repo}`);
        const commitData = response.data.map(item => ({ week: item.week, count: item.count }));

        this.commitChartOptions = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow',
            },
          },
          xAxis: {
            type: 'category',
            data: commitData.map(item => item.week),
            axisLabel: {
              rotate: 45,
              overflow: 'truncate',
              ellipsis: '...',
            },
          },
          yAxis: {
            type: 'value',
            name: 'Commits',
          },
          series: [{
            name: 'Commits',
            type: 'bar',
            data: commitData.map(item => item.count),
            itemStyle: {
              color: '#6366f1',
            },
          }],
        };
      } catch (error) {
        console.error("Error fetching commits:", error);
      }
    },
    async getContributorStats() {
      try {
        const response = await axios.get(`http://localhost:8000/contributors?owner=${this.owner}&repo=${this.repo}`)
        const contributorData = response.data.map(contrib => ({
          name: contrib.login,
          value: contrib.contributions
        }))

        this.contributorChartOptions = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'right',
            top: 'middle',
            type: 'scroll'
          },
          series: [{
            name: 'Contributions',
            type: 'pie',
            radius: '70%',
            center: ['40%', '50%'],
            data: contributorData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        }
      } catch (error) {
        console.error("Error fetching contributors:", error)
      }
    },
    async getIssues() {
      try {
        const response = await axios.get(`http://localhost:8000/issue_counts?owner=${this.owner}&repo=${this.repo}`)
        const issuesData = [
          { name: 'Open Issues', value: response.data.open },
          { name: 'Closed Issues', value: response.data.closed }
        ]

        this.issuesChartOptions = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['Issues']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: issuesData.map(item => item.name)
          },
          yAxis: {
            type: 'value',
            name: 'Count'
          },
          series: [{
            name: 'Issues',
            type: 'bar',
            data: issuesData.map(item => item.value),
            itemStyle: {
              color: function (params) {
                return params.dataIndex === 0 ? '#ef4444' : '#22c55e'
              }
            }
          }]
        }
      } catch (error) {
        console.error("Error fetching issues:", error)
      }
    },
    async getPullRequests() {
      try {
        const response = await axios.get(`http://localhost:8000/pull_request_counts?owner=${this.owner}&repo=${this.repo}`)
        const prData = [
          { name: 'Open PRs', value: response.data.open },
          { name: 'Merged PRs', value: response.data.merged }
        ]

        this.pullRequestsChartOptions = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['Pull Requests']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: prData.map(item => item.name)
          },
          yAxis: {
            type: 'value',
            name: 'Count'
          },
          series: [{
            name: 'Pull Requests',
            type: 'bar',
            data: prData.map(item => item.value),
            itemStyle: {
              color: function (params) {
                return params.dataIndex === 0 ? '#6366f1' : '#8b5cf6'
              }
            }
          }]
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
