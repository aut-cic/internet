const {Schema, Model} = require('@bakjs/mongo')

class Subnet extends Model {

    static get $schema() {
        return {
            subnet: {type: "String"},
            description: {type: "String"},
        }
    };

}

module.exports = Subnet.$model;
