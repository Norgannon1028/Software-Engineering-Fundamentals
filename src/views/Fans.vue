<template>
  <div class="fans">
    <Navigator return="info" />
    <el-button style="float:left" @click="backtohisinfo(username)">返回信息界面</el-button>
    <br/>
    <br/>
    <div
        class="fans"
        v-for="item in allfans.data"
        :key="item.id"
      >
      <br />
      <div @click="tohisinfo(item.username)">
        <p>用户名：{{ item.username }}</p>
        <p>邮箱：{{ item.email }}</p>
        <p v-if="item.sex==1">性别：男</p>
        <p v-if="item.sex==0">性别：女</p>
        <p>年龄：{{ item.old }}</p>
        <br />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";

export default {
  name: "Fans",
  components: {
    Navigator
  },
  data() {
    return {
      username:"",
      allfans:{}
    };
  },
  created() {
    this.username = this.$route.params.username;
    //alert(this.username)
    this.showallfans();
   // this.loadcomments();  

  },
  methods: {
    tohisinfo(hisname) {
      this.$router.push({
        name: "Info",
        params: {
          username: hisname
        }
      });
    },
    backtohisinfo(hisname) {
        this.$router.push({
        name: "Info",
        params: {
          username: hisname
        }
      });
    },
    showallfans() {
       var that = this;
        axios
        .post("http://localhost:5000/allfans", {
           username: this.username
        })
        .then(function(response) {
          that.allfans=response
        })
        .catch(function(error) {
          alert(error);
        });
    }
  },
  mounted(){

  },
};
</script>

<style scoped>
.each {
  width: 30%;
  border: 1px solid black;
  margin: 5px;
  cursor: pointer;
}
</style>