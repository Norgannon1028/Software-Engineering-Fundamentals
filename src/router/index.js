import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import Zone from "../views/Zone.vue";
import Write from "../views/Write.vue";
import Blog from "../views/Blog.vue";
import Forget from "../views/Forget.vue";
import ChangePassword from "../views/ChangePassword.vue";
import Comment from "../views/Comment.vue";
import Follow from "../views/Follow.vue";
import Follower from "../views/Follower.vue";
import Info from "../views/Info.vue";
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
    path: "/comment",
    name: "Comment",
    component: Comment
  },
  {
    path: "/follow",
    name: "Follow",
    component: Follow
  },
  {
    path: "/follower",
    name: "Follower",
    component: Follower
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/forget",
    name: "Forget",
    component: Forget
  },
  {
    path: "/changepassword",
    name: "ChangePassword",
    component: ChangePassword
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup
  },
  {
    path: "/zone",
    name: "Zone",
    component: Zone
  },
  {
    path: "/write/:id",
    name: "Write",
    component: Write
  },
  {
    path: "/blog/:id",
    name: "Blog",
    component: Blog
  },
  {
    path: "/info",
    name: "Info",
    component: Info
  }
];

const router = new VueRouter({
  routes
});

export default router;
