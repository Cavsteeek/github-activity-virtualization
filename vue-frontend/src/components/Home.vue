<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'Home',
  data() {
    return {
      githubUrl: '',
      owner: '',
      repo: '',
      charts: {
        commitChart: null,
        contributorChart: null,
        issueChart: null,
        prChart: null
      },
      statsData: {
        commits: [],
        contributors: [],
        issues: [],
        pullRequests: []
      }
    }
  },

  methods: {
    extractRepoDetails() {
      const regex = /^https:\/\/github\.com\/([^/]+)\/([^/]+)$/;
      const match = this.githubUrl.match(regex);
      if (match) {
        this.owner = match[1];
        this.repo = match[2];
      } else {
        alert("Please enter a valid GitHub repository URL");
      }
    },

    async fetchData() {
      this.extractRepoDetails();
      if (!this.owner || !this.repo) return;

      await this.getCommit();
      await this.getContributorStats();
      await this.getIssues();
      await this.getPullRequests();
    },

    async getCommit() {
      const apiUrl = `http://localhost:8000/commits?owner=${this.owner}&repo=${this.repo}`;
      try {
        const response = await axios.get(apiUrl);
        console.log("Commit Data: ", response.data);
        this.statsData.commits = response.data;
        this.updateCommitChart();
        // alert("Commit data fetched successfully");
      } catch (error) {
        console.error("Error fetching commits:", error);
      }
    },

    async getContributorStats() {
      const apiUrl = `http://localhost:8000/contributors?owner=${this.owner}&repo=${this.repo}`;
      try {
        const response = await axios.get(apiUrl);
        console.log("Contributor Data: ", response.data);
        this.statsData.contributors = response.data;
        this.updateContributorChart();
        // alert("Contributor data fetched successfully");
      } catch (error) {
        console.error("Error fetching contributors:", error);
      }
    },

    async getIssues() {
      const apiUrl = `http://localhost:8000/issues?owner=${this.owner}&repo=${this.repo}`;
      try {
        const response = await axios.get(apiUrl);
        console.log("Issues Data: ", response.data);
        this.statsData.issues = response.data;
        this.updateIssueChart();
        // alert("Issues data fetched successfully");
      } catch (error) {
        console.error("Error fetching issues:", error);
      }
    },

    async getPullRequests() {
      const apiUrl = `http://localhost:8000/pull_requests?owner=${this.owner}&repo=${this.repo}`;
      try {
        const response = await axios.get(apiUrl);
        console.log("Pull Requests Data: ", response.data);
        this.statsData.pullRequests = response.data;
        this.updatePRChart();
        // alert("Pull requests data fetched successfully");
      } catch (error) {
        console.error("Error fetching pull requests:", error);
      }
    },

    initializeCharts() {
      // Initialize Commit Frequency Chart
      this.charts.commitChart = new Chart(
        document.getElementById('commitChart'),
        {
          type: 'line',
          data: {
            labels: [],
            datasets: [{
              label: 'Commits',
              data: [],
              borderColor: '#4F46E5',
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        }
      );

      // Initialize Contributor Statistics Chart
      this.charts.contributorChart = new Chart(
        document.getElementById('contributorChart'),
        {
          type: 'bar',
          data: {
            labels: [],
            datasets: [{
              label: 'Contributions',
              data: [],
              backgroundColor: '#10B981'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        }
      );

      // Initialize Issue Trends Chart
      this.charts.issueChart = new Chart(
        document.getElementById('issueChart'),
        {
          type: 'line',
          data: {
            labels: [],
            datasets: [{
              label: 'Open Issues',
              data: [],
              borderColor: '#FBBF24',
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        }
      );

      // Initialize PR Trends Chart
      this.charts.prChart = new Chart(
        document.getElementById('prChart'),
        {
          type: 'line',
          data: {
            labels: [],
            datasets: [{
              label: 'Pull Requests',
              data: [],
              borderColor: '#3B82F6',
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        }
      );
    },

    updateCommitChart() {
      const commits = this.statsData.commits;
      // Process commit data - example assuming commits have date property
      const commitsByDate = commits.reduce((acc, commit) => {
        const date = new Date(commit.created_at).toLocaleDateString();
        acc[date] = (acc[date] || 0) + 1;
        return acc;
      }, {});

      this.charts.commitChart.data.labels = Object.keys(commitsByDate);
      this.charts.commitChart.data.datasets[0].data = Object.values(commitsByDate);
      this.charts.commitChart.update();
    },

    updateContributorChart() {
      const contributors = this.statsData.contributors.slice(0, 10); // Top 10 contributors
      this.charts.contributorChart.data.labels = contributors.map(c => c.login);
      this.charts.contributorChart.data.datasets[0].data = contributors.map(c => c.contributions);
      this.charts.contributorChart.update();
    },

    updateIssueChart() {
      const issues = this.statsData.issues;
      // Group issues by month
      const issuesByMonth = issues.reduce((acc, issue) => {
        const month = new Date(issue.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
        acc[month] = (acc[month] || 0) + 1;
        return acc;
      }, {});

      this.charts.issueChart.data.labels = Object.keys(issuesByMonth);
      this.charts.issueChart.data.datasets[0].data = Object.values(issuesByMonth);
      this.charts.issueChart.update();
    },

    updatePRChart() {
      const prs = this.statsData.pullRequests;
      // Group PRs by month
      const prsByMonth = prs.reduce((acc, pr) => {
        const month = new Date(pr.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
        acc[month] = (acc[month] || 0) + 1;
        return acc;
      }, {});

      this.charts.prChart.data.labels = Object.keys(prsByMonth);
      this.charts.prChart.data.datasets[0].data = Object.values(prsByMonth);
      this.charts.prChart.update();
    }
  },
  mounted() {
    this.initializeCharts();
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
      <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">
        GitHub Repository Activity Visualizer
      </h1>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Enter your GitHub repository URL:
        </label>
        <input type="text" placeholder="https://github.com/owner/repo"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-200"
          v-model="githubUrl" />
        <button class="w-full mt-4 bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition"
          @click="fetchData">
          Fetch Data
        </button>
      </div>

      <!-- Visualization Section -->
      <div class="mt-8 space-y-6">
        <!-- Commit Frequency -->
        <div class="bg-indigo-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Commit Frequency</h2>
          <div class="h-40 bg-indigo-200 rounded-lg"></div>
        </div>

        <!-- Contributor Statistics -->
        <div class="bg-green-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Contributor Statistics</h2>
          <div class="h-40 bg-green-200 rounded-lg"></div>
        </div>

        <!-- Issue Trends -->
        <div class="bg-yellow-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Issue Trends</h2>
          <div class="h-40 bg-yellow-200 rounded-lg"></div>
        </div>

        <!-- Pull Request Trends -->
        <div class="bg-blue-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Pull Request Trends</h2>
          <div class="h-40 bg-blue-200 rounded-lg"></div>
        </div>
      </div>
    </div>
  </div>
</template>
