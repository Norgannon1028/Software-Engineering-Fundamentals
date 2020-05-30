<template>
  <div class="comment">
    <Navigator return="comment" />
    <el-button style="float:left" @click="backtothisblog(blog_id)">返回</el-button>
    <br/>
    <br/>
    <div
        class="comments"
        v-for="item in allcomments.data"
        :key="item.id"
      >
      <br />
        <p>评论内容：{{ item.content }}</p>
        <p @click="tohisinfo(item.userid)">作者：{{ item.userid }}</p>
        <p>发表时间：{{ item.time }}</p>
        <br />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";

export default {
  name: "Blog",
  components: {
    Navigator
  },
  data() {
    return {
      blog_id:1,
      allcomments:{}
    };
  },
  created() {
    this.blog_id = parseInt(this.$route.params.id);
    //alert(this.blog_id)
    this.showallcomments();
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
    backtothisblog(blogid) {
        this.$router.push({
        name: "Blog",
        params: {
          id: blogid
        }
      });
    },
    showallcomments() {
       var that = this;
        axios
        .post("http://localhost:5000/allcomments", {
          blogid: this.blog_id
        })
        .then(function(response) {
          that.allcomments=response
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