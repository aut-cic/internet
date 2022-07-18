export default {
  // Routes
  routes: ["./controllers/site"],

  // Plugins
  registrations: ["@bakjs/nunjucks"],

  nunjucks: {
    staticCache: 300 * 60 * 1000,
  },
};
