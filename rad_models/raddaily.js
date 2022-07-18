module.exports = function (sequelize, _DataTypes) {
  return sequelize.define(
    "raddaily",
    {
      id: {
        type: "INT(11)",
        allowNull: false,
        defaultValue: null,
        primaryKey: true,
        autoIncrement: true,
        comment: null,
        foreignKey: [Object],
      },
      username: {
        type: "VARCHAR(64)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
        foreignKey: [Object],
      },
      usageorig: {
        type: "BIGINT(20)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      usagediscount: {
        type: "BIGINT(20)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      createddate: {
        type: "DATE",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
        foreignKey: [Object],
      },
    },
    {
      tableName: "raddaily",
    }
  );
};
