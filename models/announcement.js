const {Model} = require('bak');
const {Schema} = require('mongoose');
const {bcrypt_hash} = require('bak/lib/helpers/security');

class Announcement extends Model {

    static get $schema() {
        return {
            type: {type: String},
            message: {type: String},
            visible: {type: Boolean},
            link: {type: String},
        }
    };

}

module.exports = Announcement.$model;
