const Axios = require('axios');
const _acct = Axios.create({baseURL:'http://172.16.4.5:9090'});
async function user_logout(acctuniqueid){

   try{ await _acct.get('logout/'+acctuniqueid).then(res=>console.log(res);return true);
}catch(e){console.error('[logout]');return false}

}

user_logout('8cdb0c35a519ebea17b6a115df046b24').then(s=>console.log(s))
