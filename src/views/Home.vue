<template>
  <div class="home">
    <Navigator return="home" />
    
    <div class="searchBox" style="margin-top: 15px;">
      <el-input
        placeholder="请输入搜索内容"
        v-model="searchkeynotuse"
        class="searchInput"
        style="padding-left: 10px;"
        @keydown.enter.native="searchblog(searchmethods)"
      >
        <el-button
          class="searchButton"
          slot="append"
          icon="el-icon-search"
          @click="searchblog(searchmethods)"
          
        ></el-button>
      </el-input>
    </div>
    <div v-if="searchflag==false" style="padding: 10px 0px 0px 15px;">
      <div style="float:left;font-size:14px">
        排序方式：
      </div>
      <el-dropdown style="float:left" @command="recommendCommand">
        <span class="el-dropdown-link">
          {{ recommendmethods }}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="最热门">最热门</el-dropdown-item>
          <el-dropdown-item command="最新">最新</el-dropdown-item>
            <!-- <el-dropdown-item>螺蛳粉</el-dropdown-item>
            <el-dropdown-item disabled>双皮奶</el-dropdown-item>
            <el-dropdown-item divided>蚵仔煎</el-dropdown-item> -->
        </el-dropdown-menu>
      </el-dropdown>
      
      <br />
      <div
        class="recommend"
        v-for="item in recommendret.data"
        :key="item.id"
      >
      <div class="box">
        <div class="list_con">
          <h5 @click="tothisblog(item.id)" tag="span" class="art-title">{{ item.title}} </h5>
        <div class="art-abstract">关键词：{{ item.keyword }}</div>
        <div style="display:flex"> 
            <el-avatar class="user-img" :src="item.face"></el-avatar>
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
    </div>
    <div v-if="searchflag==true">
      <div style="float:left;font-size:14px">
        排序方式：
      </div>
      <el-dropdown style="float:left" @command="searchCommand">
        <span class="el-dropdown-link">
          {{ searchmethods }}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <br />
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="最热门">最热门</el-dropdown-item>
          <el-dropdown-item command="最新">最新</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <br />
      <div
        class="search"
        v-for="item in searchret.data"
        :key="item.id"
      >
      <br/>
      <div class="box">
        <div class="list_con">
          <h5 @click="tothisblog(item.id)" tag="span" class="art-title">{{ item.title}} </h5>
          <div class="art-abstract">关键词：{{ item.keyword }}</div>
          <div style="display:flex"> 
            <el-avatar class="user-img" :src="item.face"></el-avatar>
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
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Navigator from "@/components/Navigator.vue";
import axios from "axios";
import global from "@/components/global.vue";
import jwt_decode from 'jwt-decode';

export default {
  name: "Home",
  components: {
    Navigator
  },
  data() {
    return {
      username:global.username,
      loginflag:global.loginflag,
      searchkeynotuse: "",
      searchkey: "",
      searchret: {},
      recommendret: {},
      searchflag: false,
      // showList: false,
      recommendmethods: "最热门",
      searchmethods: "最热门"
    };
  },
  created()
  {
    this.searchflag = false;
    this.searchret = {};
    this.recommendblog(this.recommendmethods);
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
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
    recommendCommand(command) {
      this.recommendmethods=command;
      this.recommendblog(this.recommendmethods);
    },
    searchCommand(command) {
      this.searchmethods=command;
      this.sortblog(this.searchmethods);
    },
    recommendblog(recommendway) {
      var that = this;
      axios
        .post("http://localhost:5000/recommend", {
          recommendway: recommendway
        })
        .then(function(response) {
          that.recommendret=response
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
    searchblog(searchway) {
      this.searchkey=this.searchkeynotuse
      this.searchflag=true
      this.recommendret={}
      var that = this;
      axios
        .post("http://localhost:5000/searchblog", {
          searchkey: that.searchkey,
          searchway: searchway
        })
        .then(function(response) {
          that.searchret=response
        })
        .catch(function(error) {
          alert(error);
        });
    },
    sortblog(searchway) {
      this.searchflag=true
      this.recommendret={}
      var that = this;
      axios
        .post("http://localhost:5000/searchblog", {
          searchkey: that.searchkey,
          searchway: searchway
        })
        .then(function(response) {
          that.searchret=response
        })
        .catch(function(error) {
          alert(error);
        });
    },
  }
};
</script>

<style scoped>
.each {
  width: 30%;
  border: 1px solid black;
  margin: 5px;
  cursor: pointer;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
}
.el-icon-arrow-down {
  font-size: 12px;
}
.searchBox{
  
  }
  .searchInput{
    
  }
  .searchButton{
    
  }
  .box { 
    border: 1px solid #DCDFE6;
    margin: 10px auto;
    padding: 10px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 5px #909399;
    opacity: 1
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
  }
  .art-time {
		margin-right: 20px;
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
  .name{
    margin-top:10px ;
    margin-left: 5px;
    cursor: pointer;
  }
  .name:hover{
    padding-left: 10px;
		color: #409EFF;
  }
</style>