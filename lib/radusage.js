const Sequelize = require("sequelize");
const Op = Sequelize.Op;
const sequelize = require("./db");
const radacct = require("../rad_models/radacct")(
  sequelize,
  Sequelize.DataTypes
);
const raddaily = require("../rad_models/raddaily")(
  sequelize,
  Sequelize.DataTypes
);
const radusergroup = require("../rad_models/radusergroup")(
  sequelize,
  Sequelize.DataTypes
);
const radpackages = require("../rad_models/radpackages")(
  sequelize,
  Sequelize.DataTypes
);

async function radusage(username, ip) {
  var user_usage = {};
  db_daily_list = await raddaily.findAll({
    where: {
      username: username,
      createddate: {
        [Op.gt]: new Date(new Date(Date.now()) - 30 * 24 * 60 * 60 * 1000),
      },
    },
  });
  usagehistory = db_daily_list.map((d) => {
    return {
      discount: d.usageorig - d.usagediscount,
      usage: d.usagediscount,
      created_date: d.createddate,
    };
  });
  usage = {
    daily: db_daily_list
      .map((d) => {
        if (
          new Date(d.createddate) >
          new Date(new Date("2019-10-06") - 24 * 60 * 60 * 1000)
        ) {
          return d.usagediscount;
        } else {
          return 0;
        }
      })
      .reduce((w1, w2) => {
        return w1 + w2;
      }, 0),
    weekly: db_daily_list
      .map((d) => {
        if (
          new Date(d.createddate) >
          new Date(new Date("2019-10-06") - 7 * 24 * 60 * 60 * 1000)
        ) {
          return d.usagediscount;
        } else {
          return 0;
        }
      })
      .reduce((w1, w2) => {
        return w1 + w2;
      }, 0),
    monthly: db_daily_list.reduce((m1, m2) => {
      return m1 + m2.usagediscount;
    }, 0),
  };
  db_session_list = await radacct.findAll({
    where: {
      username: username,
      acctstoptime: {
        [Op.is]: null,
      },
    },
  });
  sessions = db_session_list.map((s) => {
    return {
      framedipaddress: s.framedipaddress,
      acctuniqueid: s.acctuniqueid,
      acctstarttime: s.acctstarttime,
      usage: s.acctinputoctets + s.acctoutputoctets,
    };
  });
  db_group = await radusergroup.findOne({ where: { username: username } });
  groupname = db_group.groupname;
  db_packages = await radpackages.findOne({ where: { groupname: groupname } });

  user_usage["username"] = username;
  user_usage["usagehistory"] = usagehistory;
  user_usage["usage"] = usage;
  user_usage["sessions"] = sessions;
  user_usage["groupname"] = groupname;
  user_usage["package"] = {
    daily: db_packages.daily_volume,
    monthly: db_packages.monthly_volume,
    weekly: db_packages.weekly_volume,
  };
  return user_usage;
}

module.exports = radusage;
