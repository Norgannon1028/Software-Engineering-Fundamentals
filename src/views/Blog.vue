<template>
  <div class="blog">
    <Navigator return="home" />
    
    <div class="item">
      <p>文章标题：{{blog_title}} 关键词：{{ blog_keyword }}</p>
      <p>作者：{{ blog_author }} 被赞数：{{ blog_like }}</p>
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
  name: "Home",
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
      blog_keyword:''
    };
  },
  created() {
    this.blog_id = this.$route.params.id;
    var that=this;
    axios
        .post("http://localhost:5000/getblog", {
          blogid: this.$route.params.id
        })
        .then(function(response) {
          that.blog_title=response.data.title;
          that.blog_author=response.data.userid;
          that.blog_time=response.data.time;
          that.blog_like=response.data.like;
          that.blog_link=response.data.link;
          that.blog_keyword=response.data.keyword;
        })
        .catch(function(error) {
          alert(error);
        });
  },
  methods: {
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