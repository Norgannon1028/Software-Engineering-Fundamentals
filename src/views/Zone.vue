<template>
  <div class="zone">
    <Navigator return="zone" />
    <div v-if="myinfoflag==false && loginflag==true">
      <el-button style="float:left" @click="tomyinfo">
            返回我的空间
      </el-button>
      <br />
      <br />
    </div>
    <el-container>
    <el-aside class="aside">
      <span> 用户名: </span>
      <span> {{uname}} </span>
      <br />
      <br />
      <span>邮箱:</span>
      <span> {{email}} </span>
      <br />
      <br />

      <el-avatar src="this.face"></el-avatar>
      <br />
      <br />
      <span v-if="this.sex==1">性别:男</span>
      <span v-if="this.sex==0">性别:女</span>
      <br />
      <br />
      <span>年龄:{{age}}</span>
      <br />
      <br />
      <span @click="tofans()">粉丝数:{{fansnum}}</span>
      <br />
      <br />
      <span @click="tofollows()">关注数:{{follownum}}</span>
      <br />
      <br />
      <el-button type="primary" @click="changeinfo()" v-if="changeflag == false && myinfoflag==true"
        >修改
      </el-button>
    <div>
      <el-button type="primary" @click="followhim()" v-if="followflag == false && myinfoflag==false && loginflag==true"
          >关注
      </el-button>
      <el-button @click="disfollowhim()" v-if="followflag == true && myinfoflag==false && loginflag==true"
          >取消关注
      </el-button>
    </div>
    </el-aside>
    <el-main class="main">
    <div
        class="allhisblogs"
        v-for="item in hisblogs.data"
        :key="item.id"
      >
      <br/>
      <div class="box" @click="tothisblog(item.id)">
        <div class="list_con">
          <div class="title">
            <h2> 
              <a @click="tothisblog(item.id)">
                文章标题：{{ item.title }}
              </a>
            </h2>
          </div>
        <div class="key-word">关键词：{{ item.keyword }}</div>
        <dl class="userbar"> 
          <dt>
            <el-avatar class="user-img" src="item.face"></el-avatar>
          </dt>
          <dd class="name" @click="tohisinfo(item.userid)">作者：{{ item.userid }} </dd>
        </dl>
        
        
        <p>被赞数：{{ item.like }}</p>
        <p>发表时间：{{ item.time }}</p>
        </div>
      </div>
    </div>
  </el-main>
   </el-container>
  </div>
</template>


<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
import jwt_decode from 'jwt-decode';
export default {
  name: "Zone",
  components: {
    Navigator
  },
  created() {
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
  },
  data() {
    return {
      fansnum:0,
      follownum:0,
      loginflag: global.loginflag,
      changeflag: false,
      uname: "",
      email: "",
      sex: "",
      face:"",
      age: "",
      image_url:'',
      hisblogs:{},
      myinfoflag:true,
      nowusername:global.username,
      followflag: true
    };
  },
  mounted(){
    //alert("hi!");
    this.uname = this.$route.params.username;
    if(this.uname==global.username)
    {
      this.myinfoflag=true
    }
    else
    {
      this.myinfoflag=false
    }
    if(this.myinfoflag==false && this.loginflag==true)
    {
      this.checkfollow();
    }
    this.getinfo();
    this.gethisblogs();
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
    tofollows() {
      this.$router.push({
        name: "Follow",
        params: {
          username: this.uname
        }
      });
    },
    tofans() {
      this.$router.push({
        name: "Follower",
        params: {
          username: this.uname
        }
      });
    },
    followhim() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/followhim", {
          hisname: that.uname,
          myname: global.username
        })
        .then(function(response) {
          if(response.data.msg=='关注成功！')
          {
            that.followflag=true;
            that.fansnum+=1;
            alert(response.data.msg)
          }
          else
          {
            alert(response.data.msg)
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    disfollowhim() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/disfollowhim", {
          hisname: that.uname,
          myname: global.username
        })
        .then(function(response) {
          if(response.data.msg=='取消关注成功！')
          {
            that.followflag=false;
            that.fansnum-=1;
            alert(response.data.msg)
          }
          else
          {
            alert(response.data.msg)
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    checkfollow() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/checkfollow", {
          hisname: that.uname,
          myname: global.username
        })
        .then(function(response) {
          if(response.data.followflag==true)
          {
            that.followflag=true;
          }
          else
          {
            that.followflag=false;
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    tomyinfo() {
      this.uname=global.username
      this.myinfoflag=true
      this.getinfo();
      this.gethisblogs();
    },
    gethisblogs() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/allhisblog", {
          username: that.uname
        })
        .then(function(response) {
          that.hisblogs=response
        })
        .catch(function(error) {
          alert(error);
        });
    },
    tothisblog(blogid)
    {
      this.$router.push({
        name: "Blog",
        params: {
          id: blogid
        }
      });
    },
    getinfo(){
      var that = this;
      axios
        .post("http://127.0.0.1:5000/getinfo", {
          username: that.uname,
        })
        .then(function(response) {
          //that.$set()
          that.email=response.data.email;
          that.age=response.data.old;
          //alert(that.age)
          that.sex=response.data.sex;
          that.fansnum=response.data.fansnum;
          that.follownum=response.data.follownum;
          that.face=response.data.face;
          //alert(response)
          // if (response.data.name == "登录成功!") {
          //   Navigator.data.loginflag = true;
          // }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    changeinfo(){
      this.$router.push({ path: "/info" });
    },
  }
};
</script>

<style scoped>
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  .box { 
    border: 1px solid #DCDFE6;
    margin: 0px auto;
    padding: 10px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 5px #909399;
    opacity: 1
  }
  .aside { 
    border: 1px solid #DCDFE6;
    margin: 10px auto;
    padding: 10px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 5px #909399;
    opacity: 1;
    height: 600px;
  }
  .main{ 
    border: 1px solid #DCDFE6;
    margin: 10px auto;
    margin-left: 30px;
    padding: 0px 35px 15px 15px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 5px #909399;
    opacity: 1
  }
  .title{
    font-size: 18px;
    font-weight: bold;
    line-height: 24px;
    height: 50px;
    margin-bottom: 4px;
    overflow: hidden;
    white-space: nowrap;
    text-decoration: none!important;
  }
</style>
