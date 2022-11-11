import axios from 'axios'
import ElementUI from "element-ui";

const request1 = axios.create({
    baseURL: 'http://127.0.0.1:5003/',
    timeout: 5000
})
request1.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';
    config.headers['Access-Control-Allow-Origin'] = '*';
    return config
}, error => {
    return Promise.reject(error)
});

export default request1
