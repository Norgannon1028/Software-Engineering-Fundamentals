<template>
  <div class="write">
    <Navigator return="write" />
    <div style="margin-top: 15px;">
      标题:<el-input
        placeholder="title"
        v-model="title"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      关键词:
      <el-input
        type="keyword"
        placeholder="keyword"
        v-model="keyword"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      内容:
      <el-input
        type="text"
        placeholder="text"
        v-model="text"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      <el-button type="primary" @click="test_ajax">
        发表
      </el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
export default {
  name: "Write",
  components: {
    Navigator
  },
  data() {
    return {
      username: global.username,
      userid: global.userid,
      text: "",
      title: "",
      keyword: ""
    };
  },
  methods: {
    test_ajax() {
      var that = this;
      axios
        .post("http://localhost:5000/write", {
          username: that.username,
          userid: that.userid,
          text: that.text,
          title: that.title,
          keyword: that.keyword
        })
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "发布成功!") {
            //alert(Navigator.username );
            //alert(Navigator.username );
            //this.forceUpdate();
            //this.$root.username = that.uname;
            //this.$root.loginflag = true;
            that.$router.push({
              path: "/home"
            });
          }
        })
        .catch(function(error) {
          alert(error);
        });
    }
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
