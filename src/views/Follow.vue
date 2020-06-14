<template>
  <div class="follow">
    <Navigator return="zone" />
    <el-button style="float:left" @click="backtohisinfo(username)">返回信息界面</el-button>
    <br/>
    <br/>
    <div
        class="follow"
        v-for="item in allfollows.data"
        :key="item.id"
      >
      <div @click="tohisinfo(item.username)" class="box">
        <p class="touch">用户名：{{ item.username }}</p>
        <p>邮箱：{{ item.email }}</p>
        <p v-if="item.sex==1">性别：男</p>
        <p v-if="item.sex==0">性别：女</p>
        <p>年龄：{{ item.old }}</p>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import jwt_decode from 'jwt-decode';
export default {
  name: "Follow",
  components: {
    Navigator
  },
  data() {
    return {
      username:"",
      allfollows:{}
    };
  },
  created() {
    this.username = this.$route.params.username;
    //alert(this.username)
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
    this.showallfollows();
   // this.loadcomments();  

  },
  methods: {
    tohisinfo(hisname) {
      this.$router.push({
        name: "Zone",
        params: {
          username: hisname
        }
      });
    },
    backtohisinfo(hisname) {
        this.$router.push({
        name: "Zone",
        params: {
          username: hisname
        }
      });
    },
    showallfollows() {
       var that = this;
        axios
        .post("http://175.24.53.216:5000/allfollows", {
           username: this.username
        })
        .then(function(response) {
          that.allfollows=response
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
.box { 
    border: 1px solid #DCDFE6;
    padding: 10px 35px 15px 35px;
    float:left;
    margin-left: 5px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 5px #909399;
    opacity: 1;
    width:20%
  }
  .touch{
    cursor: pointer;
  }
  .touch:hover{
    padding-left: 10px;
		color: #409EFF;
  }
</style>