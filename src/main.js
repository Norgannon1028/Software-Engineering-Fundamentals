import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";

Vue.config.productionTip = false;

// 将axios全局注册为名为http的变量
Vue.prototype.$http = axios;
// axios发送请求的网址
axios.defaults.baseURL = "http://.";

Vue.use(ElementUI);

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
