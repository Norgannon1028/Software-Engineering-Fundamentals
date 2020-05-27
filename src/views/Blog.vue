<template>
  <div class="blog">
    <Navigator return="blog" />
    
    <div class="item">
      <p>文章标题：{{blog_title}} 关键词：{{ blog_keyword }}</p>
      <p>作者：{{ blog_author }} 被赞数：{{ blog_like }}</p>

      <el-button type="primary" @click="likethisbolg" v-if="likeflag==false && loginflag==true">点赞</el-button>
      <el-button @click="dislikethisbolg" v-if="likeflag==true && loginflag==true">已点赞</el-button>

      <p>发表时间：{{ blog_time }}</p>
      <p>内容：{{blog_link}}</p>
    </div>
    
  </div>
</template>

<script>
// @ is an alias to /src
import Navigator from "@/components/Navigator.vue";
import axios from "axios";
import global from "@/components/global.vue";

export default {
  name: "Blog",
  components: {
    Navigator
  },
  data() {
    return {
      username:global.username,
      loginflag:global.loginflag,
      blog_id:-1,
      blog_title:'',
      blog_author:'',
      blog_time:'',
      blog_like:0,
      blog_link:'',
      blog_keyword:'',
      likeflag:false
    };
  },
  created() {
    this.blog_id = this.$route.query.id;
    var that=this;
    axios
        .post("http://localhost:5000/getblog", {
          blogid: that.blog_id,
          thisuser: global.userid
        })
        .then(function(response) {
          that.blog_title=response.data.blog.title;
          that.blog_author=response.data.writer;
          that.blog_time=response.data.blog.time;
          that.blog_like=response.data.blog.like;
          that.blog_link=response.data.blog.link;
          that.blog_keyword=response.data.blog.keyword;
          that.likeflag=response.data.likeflag;
        })
        .catch(function(error) {
          alert(error);
        });
  },
  methods: {
    likethisbolg() {
      var that=this;
      axios
        .post("http://localhost:5000/addlike", {
          blogid: that.blog_id,
          thisuser: global.userid
        })
        .then(function(response) {
          // alert(response.data.msg)
          if(response.data.msg=="点赞成功！")
          {
            that.blog_like+=1;
            that.likeflag=true;
          }
          else
          {
            alert("点赞失败，请稍后重试")
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    dislikethisbolg() {
      var that=this;
      axios
        .post("http://localhost:5000/dislike", {
          blogid: that.blog_id,
          thisuser: global.userid
        })
        .then(function(response) {
          // alert(response.data.msg)
          if(response.data.msg=="已取消点赞！")
          {
            that.blog_like-=1;
            that.likeflag=false;
          }
          else
          {
            alert("取消点赞失败，请稍后重试")
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    lookingnow() {
      global.lookingblog=true
    },
    searchblog() {
      var that = this;
      axios
        .post("http://localhost:5000/blog", {
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
      this.$router.push({ path: "/blog/" + blogid });
    }
  },
  mounted(){
    //alert("hi!");
    this.lookingnow()
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