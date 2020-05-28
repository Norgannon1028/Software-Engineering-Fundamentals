import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import Info from "../views/Info.vue";
import Write from "../views/Write.vue";
import Blog from "../views/Blog.vue";
import Repassword from "../views/Repassword.vue";
import Changepassword from "../views/Changepassword.vue";
Vue.use(VueRouter);
const routes = [
  // 单纯的切换，redirect对应的是name
  {
    path: "/",
    redirect: "Home"
  },
  // 先在上方引入Home的vue对象，然后作为组件使用
  {
    path: "/home",
    name: "Home",
    component: Home
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/repassword",
    name: "Repassword",
    component: Repassword
  },
  {
    path: "/changepassword",
    name: "Changepassword",
    component: Changepassword
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup
  },
  {
    path: "/info",
    name: "Info",
    component: Info
  },
  {
    path: "/write/:id",
    name: "Write",
    component: Write
  },
  {
    path: "/blog:id",
    name: "Blog",
    component: Blog
  },
  // 在添加组件时再引用vue文件使用
  // {
  //   path: "/test",
  //   name: "Test",
  //   component: () => import("../views/Test.vue")
  // },
  // 同上，不过此时需要有一个id的参数才能显示，参数可获取
  {
    path: "/result/:id",
    name: "Result",
    component: () => import("../views/Result.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
