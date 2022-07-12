export default {
  mongo: {
    connections: {
      default: { uri: "mongodb://localhost/internet" },
    },
  },

  radius: {
    username: "opnsense",
    password: "opnsense@123",
  },

  log: {
    sentry: {
      dsn: null,
    },
  },

  /**
   * Configure auth
   */
  auth: {
    secret: "SMOIJc92jcO",
    oauth: {
      aut: {
        url: "https://account.aut.ac.ir/api/oauth",
        url_internal: "https://account.aut.ac.ir/api/oauth",
        client_id: "5894a9bfa1a08704482fc97e",
        redirect_uri: "http://localhost:3000/authorize",
        client_secret: "Ajjc82j8cz",
      },
    },
  },
};
