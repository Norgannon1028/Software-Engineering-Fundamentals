<template>
  <div class="home">
    <Navigator return="home" />
    <div style="margin-top: 15px;">
      <el-input
        placeholder="请输入搜索内容"
        v-model="searchkey"
        class="input-with-select"
      >
        <el-button
          slot="append"
          icon="el-icon-search"
          @click="searchblog"
        ></el-button>
      </el-input>
    </div>
    <div class="recommend" v-if=" searchret.data== null">

      
    </div>
    <div class="item" v-for="item in searchret.data" :key="item.id" @click="tothisblog(item.id)">
      <p>文章标题：{{ item.title }} 关键词：{{ item.keyword }}</p>
      <p>作者：{{ item.username }} 被赞数：{{ item.like }}</p>
      <p>发表时间：{{ item.time }}</p>
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
      searchkey: "",
      searchret: {},
      showList: false,
      items: [
        { con: "18373657", id: "11111" },
        { con: "11111111", id: "22222" },
        { con: "22222222", id: "33333" }
      ]
    };
  },
  methods: {
    searchblog() {
      var that = this;
      axios
        .post("http://localhost:5000/searchblog", {
          searchkey: that.searchkey
        })
        .then(function(response) {
          that.searchret=response
        })
        .catch(function(error) {
          alert(error);
        });
    },
    tothisblog(blogid)
    {
      this.$router.push({
        path: "/blog",
        query: {
          id: blogid
        }
      });
    }
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
</style>