<template>
  <div class="home">
    <Navigator return="home" />
    <div style="margin-top: 15px;">
      <el-input
        placeholder="请输入搜索内容"
        v-model="searchkeynotuse"
        class="input-with-select"
      >
        <el-button
          slot="append"
          icon="el-icon-search"
          @click="searchblog(searchmethods)"
        ></el-button>
      </el-input>
    </div>
    <br />
    <div v-if="searchflag==false">
      <div style="float:left;font-size:14px">
        排序方式：
      </div>
      <el-dropdown style="float:left" @command="recommendCommand">
        <span class="el-dropdown-link">
          {{ recommendmethods }}<i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <br />
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
      <br/>
        <p @click="tothisblog(item.id)">文章标题：{{ item.title }}</p>
        <p>关键词：{{ item.keyword }}</p>
        <p @click="tohisinfo(item.userid)">作者：{{ item.userid }} </p>
        <p>被赞数：{{ item.like }}</p>
        <p>发表时间：{{ item.time }}</p>
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
            <!-- <el-dropdown-item>螺蛳粉</el-dropdown-item>
            <el-dropdown-item disabled>双皮奶</el-dropdown-item>
            <el-dropdown-item divided>蚵仔煎</el-dropdown-item> -->
        </el-dropdown-menu>
      </el-dropdown>
      <br />
      <div class="item" v-for="item in searchret.data" :key="item.id" @click="tothisblog(item.id)">
        <p>文章标题：{{ item.title }} 关键词：{{ item.keyword }}</p>
        <p>作者：{{ item.userid }} 被赞数：{{ item.like }}</p>
        <p>发表时间：{{ item.time }}</p>
      </div>
    </div>
    <!-- <div id="list">
      <div
        class="each"
        v-show="showList"
        v-for="(item, index) in items"
        :key="index"
        @click="toResult(item.id)"
      >
        
      </div>
    </div> -->
    <!-- <div style="margin-top: 15px;">
      <el-tag v-show="showList" @click="addItem">添加元素</el-tag>
      <br />
      <br />
      <el-tag v-show="showList" @click="deleteItem">删除元素</el-tag>
    </div> -->
    <!-- <div style="margin-top: 15px;">
      <el-tag @click="toTest">跳转测试</el-tag>
      <br />
      <br />
      <el-tag @click="toTest2">地址栏传值测试</el-tag>
      <br />
      <br />
      <el-tag @click="toTest3">隐式传值测试</el-tag>
      <br />
      <br />
      <el-tag @click="addItem">增加测试</el-tag>
    </div> -->
  </div>
</template>

<script>
// @ is an alias to /src
import Navigator from "@/components/Navigator.vue";
import axios from "axios";
import global from "@/components/global.vue";

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
    // toResult(itemId) {
    //   this.$router.push({ path: "/result/" + itemId });
    // },
    // toTest() {
    //   this.$router.push("test");
    // },
    // toTest2() {
    //   this.$router.push({
    //     path: "/test",
    //     query: {
    //       id: 222
    //     }
    //   });
    // },
    // // ?id=21312312
    // toTest3() {
    //   this.$router.push({
    //     name: "Test",
    //     params: {
    //       id: 222
    //     }
    //   });
    // },
    // addItem() {
    //   this.items.push({ con: "new", id: "1231223" });
    // },
    // deleteItem() {
    //   if (this.items.length != 1) {
    //     this.items.pop();
    //   } else {
    //     alert("无法删除");
    //   }
    // }
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
</style>