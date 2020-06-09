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
      <br/>
      <el-avatar src="this.face"></el-avatar>
      <br/>
      <span>邮箱:</span>
      <span> {{email}} </span>
      
      <br/>
      <br/>
      <span v-if="this.sex==1">性别:男</span>
      <span v-if="this.sex==0">性别:女</span>
      <br/>
      <br/>
      <span>年龄:{{age}}</span>
      <br/>
      <br/>
      <span class="touch" @click="tofans()">粉丝数:{{fansnum}}</span>
      <br/>
      <br/>
      <span class="touch" @click="tofollows()">关注数:{{follownum}}</span>
      <br/>
      <br/>
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
      <div class="box">
        <div class="list_con">
          <h5 @click="tothisblog(item.id)" tag="span" class="art-title">{{ item.title}} </h5>
        <div class="art-abstract">关键词：{{ item.keyword }}</div>
        <div style="display:flex"> 
            <el-avatar class="user-img" src="item.face"></el-avatar>
            <br>
            <div class="name" @click="tohisinfo(item.userid)">作者：{{ item.userid }} </div>
        </div>
        <div class="art-more">
          <div class="art-time"><i class="el-icon-time"></i>发表时间：{{ item.time }}</div>
          <div class="view"><i class="el-icon-star-on"></i>被赞数：{{ item.like }}</div>
        </div>
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
    margin: 5px ;
    margin-left: 10px;
    margin-bottom: 10px;
    width: 800px;
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
    margin: 5px auto;
    margin-left: 30px;
    padding: 0px 0px 0px 0px;
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
  #side .item {
		margin-bottom: 30px;
	}
	
	.art-item {
		margin-bottom: 30px;
		position: relative;
	}
	
	.art-item .star {
		width: 60px;
		height: 60px;
		position: absolute;
		top: 0;
		right: 0;
	}
	
	img.tag {
		width: 16px;
		height: 16px;
	}
	
	.art-title {
		border-left: 3px solid #409EFF;
		padding-left: 5px;
		cursor: pointer;
	}
	
	.art-title:hover {
		padding-left: 10px;
		color: #409EFF;
	}
	
	.art-time {
		margin-right: 20px;
	}
	
	.art-body {
		display: flex;
		padding: 10px 0;
	}
	
	.side-img {
		height: 150px;
		width: 270px;
		overflow: hidden;
		margin-right: 10px;
	}
	
	img.art-banner {
		width: 100%;
		height: 100%;
		transition: all 0.6s;
	}
	
	img.art-banner:hover {
		transform: scale(1.4);
	}
	
	.side-abstract {
		flex: 1;
		display: flex;
		flex-direction: column;
	}
	
	.art-abstract {
		flex: 1;
    color: #aaa;
    margin-bottom: 20px;
	}
	
	.art-more {
		height: 40px;
		display: flex;
		justify-content: flex-end;
		align-items: flex-end;
	}
	
	.art-more .view {
		color: #aaa;
	}
	h5{
		font-size: 18px;
	}
	.pagination {
		background-color: #F9F9F9;
  }
  .name{
    margin-top:10px ;
    margin-left: 5px;
    cursor: pointer;
  }
  .name:hover{
    padding-left: 10px;
		color: #409EFF;
  }
  .touch{
    cursor: pointer;
  }
  .touch:hover{
    padding-left: 10px;
		color: #409EFF;
  }
</style>
