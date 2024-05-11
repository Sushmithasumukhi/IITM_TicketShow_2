<template>
    <div>
    <T_NavBar/>
    <div class="container">
    <br>
      <h1>Shows</h1>
      <!-- <div v-if="theaters.length===0">
        <p class="text-center" style="font-size: 25px; font-style: oblique; color: brown; ">Please add Theaters to add Shows.</p>
      </div> -->
      <!-- <div v-else> -->
        <div class="d-flex flex-row-reverse">
        <router-link class="btn btn-warning" :to="{name:'ShowCreate'}">+ Add Shows</router-link>
      </div><br>
      <!-- </div> -->
      <div class="row" v-if="shows.length!==0">
        <div v-for="m in shows" :key="m.id" class="col-lg-4 col-md-6 col-sm-12">
          <div class="card-p3 bg body-dark">
            <router-link :to="{name: 'S_Details', params:{id : m.id}}">
        <img :src="m.m_image" class="card-img-top" style="width: 180px; height: 180px ;" :alt="m.show_name" >
          
        <div class="card-body">
            <h4 class="card-title" style="font-size: 20px;">{{ m.show_name }}</h4>
            <div class="badge badge-success" v-for="genre in m.tags" :key="genre">{{ genre }}</div> <br>
          </div>
        </router-link>
        </div>
      </div>
      </div>
      <div v-else>
        <p style="font-size: 20px; color: brown;">No shows, Add shows</p>
        <!-- <p style="font-size: 20px; font-style: italic; color: brown;" class="text-center">No shows added, please add shows</p> -->
      </div>
   </div>
  </div>
  
</template>
  
<script>
  
  import T_NavBar from '@/components/T_NavBar.vue';
  
  
  export default{
    name:'ShowGet',
    components:{
          T_NavBar
      },
    data(){
          return {
                shows:[],
                theaters:[]
        }
      },

    mounted(){
      this.fetchshows();
      this.fetchtheater();
    },
    methods:{
      fetchshows(){
        fetch('http://127.0.0.1:5000/admin/show/all',{
          method: 'GET',
          credentials: 'include',
          headers:{
            'Authentication-Token': sessionStorage.auth_token,
            'Content-Type':'application/json'
          }
        })
        .then(resp => {
          if(resp.status === 200){
              return resp.json()
          }else if(resp.status === 401 ){
              this.$router.push('/not-authorized')
          }else if(resp.status === 404 ){
              this.$router.push('/not-found')}
        })
        .then(data =>{
          this.shows = data;
        }).catch(error =>{
          console.log(error)
        })
      },
      fetchtheater(){
        fetch('http://127.0.0.1:5000/admin/get/theater',{
          headers:{
            'Authentication-Token': sessionStorage.auth_token,
            'Content-Type':'application/json'
          }
        })
        .then(resp => resp.json())
        .then(data =>{
          this.theaters = data;
        }).catch(error=>{
          console.log(error)
        })
      }
    }
  }
  </script>
  
  <style scoped>
  
  .card-img-top{
    width: 170px;
    height: 170px;
  }
  .card-body{
    padding: 10px;
  }
  </style>
  
  
  
  
  
  