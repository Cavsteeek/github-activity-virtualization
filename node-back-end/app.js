const express = require('express');
const axios = require('axios');
require('dotenv').config();

// GitHub API URL
const GITHUB_API_URL = 'https://api.github.com'

const app = express();

async function fetchGitHubData(url) {
    try {
      const response = await axios.get(url, {
        headers: { Authorization: `token ${process.env.GITHUB_TOKEN}` }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching data from GitHub: ${error.message}`);
      throw error;
    }
  }


// Route to get commit frequency
app.get('/api/commits', async (req, res) => {
    const { owner, repo } = req.query;
  
    try {
      const commits = await fetchGitHubData(`${GITHUB_API_URL}/repos/${owner}/${repo}/commits`);
      const commitFrequency = {};
  
      commits.forEach(commit => {
        const date = commit.commit.author.date.split('T')[0];
        commitFrequency[date] = (commitFrequency[date] || 0) + 1;
      });
  
      res.json(commitFrequency);
    } catch (error) {
      res.status(500).json({ message: 'Error fetching commit data' });
    }
  });
  
  // Route to get contributor statistics
  app.get('/api/contributors', async (req, res) => {
    const { owner, repo } = req.query;
  
    try {
      const contributors = await fetchGitHubData(`${GITHUB_API_URL}/repos/${owner}/${repo}/contributors`);
      const contributorStats = contributors.map(contributor => ({
        login: contributor.login,
        contributions: contributor.contributions
      }));
  
      res.json(contributorStats);
    } catch (error) {
      res.status(500).json({ message: 'Error fetching contributor data' });
    }
  });
  
  // Route to get issue and pull request trends
  app.get('/api/issues', async (req, res) => {
    const { owner, repo } = req.query;
  
    try {
      const issues = await fetchGitHubData(`${GITHUB_API_URL}/repos/${owner}/${repo}/issues`);
      const openIssues = issues.filter(issue => issue.state === 'open').length;
      const closedIssues = issues.filter(issue => issue.state === 'closed').length;
  
      res.json({ openIssues, closedIssues });
    } catch (error) {
      res.status(500).json({ message: 'Error fetching issue data' });
    }
  });
  

  module.exports = app;