<template>
  
  <div class="main">
    <Navigator return="blog" />
    <div class="item">
      <div id="artcle-info">
        <h2 class="text-center"><strong>{{blog_title}}</strong></h2>
        <div class="text-center timeAndView">
            <div>
						<span class="article-time">
							<i class="el-icon-time"></i>
							{{ blog_time }}
						</span>
						&nbsp;|&nbsp;
						<span class="article-views">
							<i class="el-icon-star-off"></i>
							被赞数：{{ blog_like }}
						</span>
            </div>
            <div style="float:right;display:flex">
              <el-avatar class="user-img" :src="this.blog_authorface"></el-avatar>
              <br>
              <div class="name" @click="tohisinfo(blog_author)">{{ blog_author }}</div>
            </div>
            <br>
          </div>
          <p class="abstract">
						关键词：{{ blog_keyword }}
					</p>
      </div>
      
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
      <br />
      <br />
      <div class="comment" v-for="item in showcomment.data" :key="item.id">
        <div style="display:flex" class="user">
          <el-avatar :src="item.face"></el-avatar>
          <div class="name" @click="tohisinfo(item.userid)">{{ item.userid }}</div>
        </div>
        <p>{{ item.content }}</p>
        <p class="time">{{ item.time }}</p>
        <br />
      </div>
      <br />
      <br />
      <div style="text-align:center">
      <el-button type="primary" @click="likefunc">{{liketext}}</el-button>
      <el-button type="primary" @click="showallcomment(blog_id)">查看评论</el-button>
      <el-button type="primary" @click="writecomment">发表评论</el-button>
      </div>
      <br />
      <br />
      <div style="text-align:center">
      <el-input
        type="comment"
        placeholder="在此输入评论内容"
        v-model="comment"
        style="width:60%;"
        class="input-with-select"
        v-if="writingcomment==true"
      ></el-input>
      </div>
      <br />
      <br />
      <div style="text-align:center">
      <el-button type="primary" v-if="writingcomment==true" @click="finishcomment">确认</el-button>
      <el-button v-if="writingcomment==true" @click="stopwriting">取消</el-button>
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
      blog_authorface:'',
      likeflag:false,
      liketext:"点赞",
      writingcomment:false,
      comment:"",
      showcomment:{}
    };
  },
  created() {
    this.blog_id = parseInt(this.$route.params.id);
    //alert(this.blog_id)
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
    var that=this;
    axios
        .post("http://175.24.53.216:5000/getblog", {
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
          that.blog_authorface=response.data.face;
          that.likeflag=response.data.likeflag;
          console.log(response.data);
          console.log(that.likeflag);
          if(that.likeflag==true){
            that.liketext="撤销点赞";
          }
        })
        .catch(function(error) {
          alert(error);
        });
      axios
        .post("http://175.24.53.216:5000/loadcomments", {
          blogid: that.blog_id
        })
        .then(function(response) {
          that.showcomment=response
        })
        .catch(function(error) {
          alert(error);
        });
        
        
    
   // this.loadcomments();     
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
    showallcomment(blogid) {
      document.body.scrollTop = document.documentElement.scrollTop = 0;
      this.$router.push({
        name: "Comment",
        params: {
          id: blogid
        }
      });
    },
    // loadcomments() {
    //   var that = this;
    //   axios
    //     .post("http://localhost:5000/loadcomments", {
    //       blogid: that.blog_id
    //     })
    //     .then(function(response) {
    //       that.showcomment=response
    //     })
    //     .catch(function(error) {
    //       alert(error);
    //     });
    // },
    stopwriting() {
      this.writingcomment=false;
    },
    writecomment() {
      if(global.loginflag==true)
      {
        this.writingcomment=true;
      }
      else
      {
        this.$message('请先登录');
      }
    },
    finishcomment() {
      if(this.comment=="")
      {
        this.$message("评论不能为空");
      }
      else
      {
        var that=this;
        axios
          .post("http://175.24.53.216:5000/addcomment", {
            blogid: that.blog_id,
            thisuser: global.userid,
            commenttext: that.comment
          })
          .then(function(response) {
            // alert(response.data.msg)
            if(response.data.msg=="评论成功！"){
              that.$message(response.data.msg);
            }
            else{
              that.$message("评论失败，请稍后重试");
            }
          })
          .catch(function(error) {
            alert(error);
          });
        this.comment="";
        this.writingcomment=false;
      }
      axios
        .post("http://175.24.53.216:5000/loadcomments", {
          blogid: that.blog_id
        })
        .then(function(response) {
          that.showcomment=response
        })
        .catch(function(error) {
          alert(error);
        });
    },
    likefunc(){
      if(global.loginflag!=true){
        this.$message("请先登录");
        return;
      }
      if(!this.likeflag){
        this.likethisbolg();
      }
      else{
        this.dislikethisbolg();
      }
    },
    likethisbolg() {
      var that=this;
      axios
        .post("http://175.24.53.216:5000/addlike", {
          blogid: that.blog_id,
          thisuser: global.userid
        })
        .then(function(response) {
          // alert(response.data.msg)
          if(response.data.msg=="点赞成功！")
          {
            that.blog_like+=1;
            that.likeflag=true;
            that.liketext="撤销点赞";
            that.$message("点赞成功");
          }
          else
          {
            that.$message("点赞失败，请稍后重试");
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    dislikethisbolg() {
      var that=this;
      axios
        .post("http://175.24.53.216:5000/dislike", {
          blogid: that.blog_id,
          thisuser: global.userid
        })
        .then(function(response) {
          // alert(response.data.msg)
          if(response.data.msg=="已取消点赞！")
          {
            that.blog_like-=1;
            that.likeflag=false;
            that.liketext="点赞";
            that.$message("已取消点赞");
          }
          else
          {
            that.$message("取消点赞失败，请稍后重试");
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
        .post("http://175.24.53.216:5000/blog", {
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
#artcle-info {
    margin: 3px;
		padding: 20px;
    margin-bottom: 40px;
    border: 1px solid #DCDFE6;
	}
	
	#artcle-info .abstract {
		color: #ffffff;
		border-left: 3px solid #409EFF;
		padding: 10px;
		background-color: rgba(126, 129, 135, 0.3);
	}
	
	#artcle-info .timeAndView {
		padding: 20px;
		line-height: 30px;
		font-size: 16px;
	}
	
	pre.has {
		color: #ffffff;
		background-color: rgba(0, 0, 0, 0.8);
	}
	
	img.has {
		width: 100%;
	}
	
	#statement {
		border-left: 3px solid #409EFF;
		padding: 20px;
		background-color: #EBEEF5;
  }
  .comment{
    border: 1px solid #DCDFE6;
    padding: 10px 40px 0px 40px;
  }
  .user{
    display:flex;
  }
  .time{
    display:flex;
    flex-direction: row-reverse;
  }
  .touch{
    cursor: pointer;
  }
  .touch:hover{
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