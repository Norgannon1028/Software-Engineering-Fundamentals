<template>
  <div class="draft">
    <Navigator return="draft" />

    <div style="padding: 10px 0px 0px 15px;">
        <div
        class="draft"
        v-for="item in alldraft.data"
        :key="item.id"
        >
            <div class="box">
                    <div class="list_con">
                        <h5 @click="writethisdraft(item.id)" tag="span" class="art-title">{{ item.title}} </h5>
                        <div class="art-abstract">关键词：{{ item.keyword }}

                        </div>
                    
                        <div class="art-more">
                            <div class="art-time"><i class="el-icon-time"></i>发表时间：{{ item.time }}
                            </div>
                        
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
  name: "Draft",
  components: {
    Navigator
  },
  data() {
    return {
      userid:global.userid,
      username:global.username,
      loginflag:global.loginflag,
      alldraft: {}
    };
  },
  created()
  {
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
    this.findalldraft();
  },
  methods: {
    writethisdraft(draftid) {
      this.$router.push({
        name: "Write",
        params: {
          id: draftid
        }
      });
    },
    findalldraft() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/getalldraft", {
          userid: that.userid
        })
        .then(function(response) {
          that.alldraft=response
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