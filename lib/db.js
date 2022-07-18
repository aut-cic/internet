const Sequelize = require("sequelize");
const Config = require("config");
//const sequelize_config = Config.get('sequelize')

const sequelize_config = {
  db_host: process.env.SQL_HOST,
  db_port: process.env.SQL_PORT,
  db_name: process.env.SQL_NAME,
  db_username: process.env.SQL_USERNAME,
  db_password: process.env.SQL_PASS,
};
const sequelize = new Sequelize(
  sequelize_config.db_name,
  sequelize_config.db_username,
  sequelize_config.db_password,
  {
    host: sequelize_config.db_host,
    por: sequelize_config.db_port,
    dialect: "mysql",
    dialectOptions: {
      insecureAuth: true,
    },
    define: {
      timestamps: false,
    },
  }
);

module.exports = sequelize;
