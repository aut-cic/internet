/* jshint indent: 1 */

export default function (sequelize, _DataTypes) {
  return sequelize.define(
    "radpackages",
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
      groupname: {
        type: "VARCHAR(64)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
        foreignKey: [Object],
      },
      daily_volume: {
        type: "INT(12)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      weekly_volume: {
        type: "INT(12)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      monthly_volume: {
        type: "INT(12)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      priority: {
        type: "INT(12)",
        allowNull: false,
        defaultValue: null,
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
      session: {
        type: "INT(11)",
        allowNull: false,
        defaultValue: "3",
        primaryKey: false,
        autoIncrement: false,
        comment: null,
      },
    },
    {
      tableName: "radpackages",
    }
  );
}
