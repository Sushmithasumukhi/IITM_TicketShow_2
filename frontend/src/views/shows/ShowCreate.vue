<template>
    <div>
     <T_NavBar/>
     <br>
       <h1 class="container text-center">ADD NEW SHOW</h1>
       <div class="container" v-if="theaters.length !== 0">
           <form @submit.prevent="createShow">
            <div>
          <p style="font-size: 15px;color: red;"><i>{{ error_msg }}</i></p>

            </div>
             <div>
               <input id="title" class="form-control" v-model="show_name" placeholder="Enter the Show name" required/>
             </div>
             <br>
             
             <div>
               <textarea id="description" class="form-control" v-model="description" placeholder="Summary of the show" required></textarea>
             </div>
             <br>
   
               <input type="text" class="form-control" id="tags" v-model="tags" placeholder="Genre" required/>
               <small class="form-text text-muted">eg. Action, Mystery, Comedy</small>
               <br>
   
               <div class="input-group mb-2">
                 <div class="input-group-prepend">
                   <div class="input-group-text"><b>₹</b></div>
                 </div>
                   <input type="text" class="form-control" id="inlineFormInputGroup" v-model="price" placeholder="₹ Amount per ticket in Rs">
               </div><br>
               <input type="text" class="form-control" id="show_time" v-model="show_time" placeholder="Starting Time of Show" required/><br>
               <div>
                 <label for="theater" style="font-size: 20px;">Theater :</label>
               <select id="theater" class="form-control" v-model="theaterselect" required>
                 <option v-for="t in theaters" :value="t.id" :key="t.id">{{ t.theater_name }} -- {{ t.t_place }} , {{ t.location }}</option>
               </select><br>
                 <input type="checkbox" value="Show Image" @click="ImageFile"><label style="font-size: 20px;">  Show Image Upload</label><br>
                 <input type="file" id="photo1" v-if="isImagefile" @change="UploadImage" accept="image\*">
               </div>
             <br><br>
             <button type="submit" class="btn btn-secondary">Upload</button>
             <router-link to="/admin/show/all"><button class="btn btn-primary ml-2">Go Back</button></router-link>
           </form>
         </div>
         <div v-else>
            <p class="text-center" style="font-size: 25px; font-style: oblique; color: brown; ">Please add Theaters to add Shows.</p>   
         </div>
   </div>
         
   </template>
   <script>
   import axios from 'axios';
   import T_NavBar from '@/components/T_NavBar.vue';
   
   
   export default{
     name: 'ShowCreate',
     components:{
           T_NavBar
       },
         data() {
           return {
             show_name: '',
             description: '',
             price:'',
             tags:'',
             show_time:'',
             photo1: null,
             isImagefile : false,
             theater_id:'', //selected theater id is stored
             theaters:[] ,//theater data stored here
             theaterselect:'',
            
             error_msg:''
       }
         },

         mounted(){
           this.TheaterDetails();
         },
         methods:{
            TheaterDetails(){
              const t_URL = 'http://127.0.0.1:5000/admin/get/theater';
              const t_id = this.theaterselect;
    
              const url_fetch = t_id ? `${t_URL}/${t_id}` : t_URL;
    
              fetch(url_fetch,{
                  headers:{
                  'Authentication-Token': sessionStorage.auth_token,
                  'Content-Type':'application/json'
                }
             })
             .then(resp=>{
                //  this.isAuth=true;
                 return resp.json()
               }
             ).then(data =>{
               this.theaters = data;
             }).catch(error=>{
               console.log(error);
               alert('Something went wrong, try again later')
             })
             },
           ImageFile(){
               this.isImagefile = !this.isImagefile
           },
   
           UploadImage(event) {
             this.photo1 = event.target.files[0];
            //  console.log(this.photo1)
           },
            async createShow() {
                let  formData = new FormData();
                formData.append('show_name', this.show_name);
                formData.append('description', this.description);
                formData.append('price', this.price);
                formData.append('show_time', this.show_time);
                formData.append('tags', this.tags);
                formData.append('theater_id', this.theaterselect);
              if (this.photo1){
              formData.append('m_image', this.photo1);
              }
              const t_id = this.theaterselect;
              try{
                let auth_token = sessionStorage.getItem('auth_token')

                await axios.post(`http://127.0.0.1:5000/admin/show/upload/${t_id}`,formData,{
                  headers:{
                    'Authentication-Token': auth_token
                  }
                })
                this.$router.push('/admin/show/all')
              }
              catch(error){
                if(error.response.status === 406)
                    this.error_msg = error.response.data.errors
                if(error.response.status === 422)
                    this.error_msg = error.response.data.errors
                if(error.response.status === 404)
                    this.$router.push('/not-found')
                else if(error.response.status === 405){
                    this.error_msg = error.response.data.message
                    console.log(error)
                }
              }
        }
      },     
    }
</script>