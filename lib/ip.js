// these subnets shows the location of the user, for example they say
// user is from computer department.
const _subnets = [];

function lookupIP(ip) {
  try {
    for (let i = 0; i < _subnets.length; i++) {
      if (_subnets[i].cidr.contains(ip)) {
        return _subnets[i];
      }
    }
  } catch (e) {
    return null;
  }
  return null;
}

module.exports = {
  lookupIP,
};
