<template>
    <div>
    <T_NavBar/>
      <div class="container"><br>
         <h1 class="text-center">ADD NEW SHOW</h1>
         <div class="container">
             <form @submit.prevent="Addshow">
            <div>
                <p style="font-size: 15px;color: red;"><i>{{ error_msg }}</i></p>
            </div>

               <div>
                 <input type="text" class="form-control" id="title" v-model="show_name" placeholder="Enter Show name" required>
               </div>
               <br>
               
               <div>
                 <textarea id="description" class="form-control" v-model="description" placeholder="Summary of the show" required></textarea>
               </div>
               <br>
     
                 <input type="text" class="form-control" id="tags" v-model="tags" placeholder="Genre" required>
                 <small class="form-text text-muted">eg. Action, Mystery, Comedy</small>
                 <br>
     
                 <div class="input-group mb-2">
                   <div class="input-group-prepend">
                     <div class="input-group-text"><b>₹</b></div>
                   </div>
                     <input type="text" class="form-control" id="inlineFormInputGroup" v-model="price" placeholder="₹ Amount per ticket in Rs">
                 </div><br>
                 <input type="text" class="form-control" id="show_time" v-model="show_time" placeholder="Starting Time of Show" required><br>
                 <div>
                   <input type="file" id="photo1"  @change="UploadImage" accept="image\*">
                 </div>
               <br><br>
               <button type="submit" class="btn btn-secondary">Upload</button>
               <button class="btn btn-primary ml-2" @click="goback">Go Back</button>
             </form>
           </div>
     </div>
  </div>
           
     </template>
     <script>
     import axios from 'axios';
     import T_NavBar from '@/components/T_NavBar.vue';
     
     export default{
       name: 'AddShow',
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
               theater_id:'', //query theater id is stored
               error_msg:''
         }
           },
           created() {
            this.theater_id = this.$route.params.id
           },
           mounted(){
             this.theater_id = this.$route.params.id
            //  console.log(this.theater_id)
           },
           methods:{   
             UploadImage(event) {
               this.photo1 = event.target.files[0];
              //  console.log(this.photo1)
             },
             goback(){
                this.$router.push({ name : 'ViewShow', params:{id : this.theater_id}})
             },
            async Addshow() {
               const formData = new FormData();
               formData.append('show_name', this.show_name);
               formData.append('description', this.description);
               formData.append('price', this.price);
               formData.append('show_time', this.show_time);
               formData.append('tags', this.tags);
               formData.append('theater_id', this.theater_id);
               if (this.photo1){
               formData.append('m_image', this.photo1);
               }
               const t_id = this.theater_id
               try {
               await axios.post(`http://127.0.0.1:5000/admin/show/upload/${t_id}`,formData,{
                headers:{
                  'Authentication-Token': sessionStorage.auth_token
                  }
               })
               this.$router.push('/admin/show/all')
            }
            catch(error){
                if(error.response.status === 404)
                    this.$router.push('/not-found')
                else if(error.response.status === 405){
                    this.error_msg = error.response.data.message
                }
            }
            }
           }
         }
     
     </script>