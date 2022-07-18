var SequelizeAuto = require("sequelize-auto-v2");
const Config = require("config");
//const sequelize_config = Config.get('sequelize')

const sequelize_config = {
  db_host: "172.16.4.5",
  db_port: "3306",
  db_name: "radius",
  db_username: "edith",
  db_password: "@utFRID2023",
};
const auto = new SequelizeAuto(
  sequelize_config.db_name,
  sequelize_config.db_username,
  sequelize_config.db_password,
  {
    host: sequelize_config.db_host,
    dialect: "mysql",
    directory: "../rad_models",
    port: sequelize_config.db_port,
    tables: ["raddaily", "radacct", "radusergroup", "radpackages"],
    dialectOptions: {
      insecureAuth: true,
    },
  }
);

auto.run((err) => {
  if (err) {
    console.log(err);
  } else {
    console.log(auto.tables); // table list
  }
});
