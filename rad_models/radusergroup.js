/* jshint indent: 1 */

export default function (sequelize, _DataTypes) {
  return sequelize.define(
    "radusergroup",
    {
      username: {
        type: "VARCHAR(64)",
        allowNull: false,
        defaultValue: "",
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      groupname: {
        type: "VARCHAR(64)",
        allowNull: false,
        defaultValue: "",
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      priority: {
        type: "INT(11)",
        allowNull: false,
        defaultValue: "1",
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      id: {
        type: "INT(11)",
        allowNull: false,
        defaultValue: null,
        primaryKey: true,
        autoIncrement: true,
        comment: null,
        foreignKey: [Object],
      },
      update_time: {
        type: "DATETIME",
        allowNull: true,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
    },
    {
      tableName: "radusergroup",
    }
  );
}
