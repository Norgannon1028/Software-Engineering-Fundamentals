<template>
  <div class="blog">
    <Navigator return="blog" />
    
    <div class="item">
      <p>文章标题：{{blog_title}} 关键词：{{ blog_keyword }}</p>
      <p>作者：{{ blog_author }} 被赞数：{{ blog_like }}</p>

      <el-button type="primary" @click="likethisbolg" v-if="likeflag==false && loginflag==true">点赞</el-button>
      <el-button @click="dislikethisbolg" v-if="likeflag==true && loginflag==true">已点赞</el-button>

      <p>发表时间：{{ blog_time }}</p>
      <mavon-editor
      class="md"
      :value="blog_md"
      :subfield = "false"
      :defaultOpen = "'preview'"
      :toolbarsFlag = "false"
      :editable="false"
      :scrollStyle="true"
      :ishljs = "true"
      ></mavon-editor>

      <el-button type="primary" @click="showallcomment">查看评论</el-button>
      <el-button type="primary" @click="writecomment">发表评论</el-button>
      <br />
      <br />
      <el-input
        type="comment"
        placeholder="在此输入评论内容"
        v-model="comment"
        style="width:60%"
        class="input-with-select"
        v-if="writingcomment==true"
      ></el-input>
      <br />
      <br />
      <el-button type="primary" v-if="writingcomment==true" @click="finishcomment">确认</el-button>
      <el-button v-if="writingcomment==true" @click="stopwriting">取消</el-button>
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
      blog_id:1,
      blog_title:'',
      blog_author:'',
      blog_time:'',
      blog_like:0,
      blog_md:'',
      blog_keyword:'',
      likeflag:false,
      writingcomment:false,
      comment:""
    };
  },
  created() {
    this.blog_id = parseInt(this.$route.params.id);
    var that=this;
    axios
        .post("http://localhost:5000/getblog", {
          blogid: that.blog_id,
          thisuser: global.userid
        })
        .then(function(response) {
          that.blog_id=response.data.blog.id
          that.blog_title=response.data.blog.title;
          that.blog_author=response.data.writer;
          that.blog_time=response.data.blog.time;
          that.blog_like=response.data.blog.like;
          that.blog_md=response.data.blog.link;
          that.blog_keyword=response.data.blog.keyword;
          that.likeflag=response.data.likeflag;
        })
        .catch(function(error) {
          alert(error);
        });
  },
  methods: {
    stopwriting() {
      this.writingcomment=false;
    },
    writecomment() {
      this.writingcomment=true;
    },
    finishcomment() {
      var that=this;
      axios
        .post("http://localhost:5000/addcomment", {
          blogid: that.blog_id,
          thisuser: global.userid,
          commenttext: that.comment
        })
        .then(function(response) {
          // alert(response.data.msg)
          if(response.data.msg=="评论成功！")
          {
            alert(response.data.msg)
          }
          else
          {
            alert("点赞失败，请稍后重试")
          }
        })
        .catch(function(error) {
          alert(error);
        });
      this.writingcomment=true;
    },
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
     this.$router.push({
        name: "Blog",
        params: {
          id: blogid
        }
      });
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