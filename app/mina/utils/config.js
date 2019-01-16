export default class Config {
    constructor() {
        this.restUrl = "http://localhost:5000/api/v1";
    }
    static getInstance() {
        if (!Config.instance) {
            Config.instance = new Config();
        }
        return Config.instance
    }
}