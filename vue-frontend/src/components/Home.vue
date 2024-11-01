<script>
export default {
  name: 'Home',
}

</script>

<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
      <!-- Header Section -->
      <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">
        GitHub Repository Activity Visualizer
      </h1>

      <!-- Input Section -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Enter your GitHub repository URL:
        </label>
        <input type="text" placeholder="https://github.com/owner/repo"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-200" />
        <button class="w-full mt-4 bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition">
          Fetch Data
        </button>
      </div>

      <!-- Visualization Section -->
      <div class="mt-8 space-y-6">
        <!-- Commit Frequency -->
        <div class="bg-indigo-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Commit Frequency</h2>
          <p class="text-gray-500 text-sm mb-2">Visual representation of commits over time.</p>
          <!-- Placeholder for Commit Frequency Chart -->
          <div class="h-40 bg-indigo-200 rounded-lg"></div>
        </div>

        <!-- Contributor Statistics -->
        <div class="bg-green-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Contributor Statistics</h2>
          <p class="text-gray-500 text-sm mb-2">Number of contributions by each contributor.</p>
          <!-- Placeholder for Contributor Statistics Chart -->
          <div class="h-40 bg-green-200 rounded-lg"></div>
        </div>

        <!-- Issue/PR Trends -->
        <div class="bg-yellow-100 p-4 rounded-lg shadow-sm">
          <h2 class="text-lg font-semibold text-gray-700">Issue & Pull Request Trends</h2>
          <p class="text-gray-500 text-sm mb-2">Trends of issues and pull requests over time.</p>
          <!-- Placeholder for Issue/PR Trends Chart -->
          <div class="h-40 bg-yellow-200 rounded-lg"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
