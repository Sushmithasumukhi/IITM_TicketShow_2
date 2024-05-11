<template>
    <div>
        <T_NavBar/>
    <div class="container">
        <h3 class="text-center">Update Show </h3>
        <form @submit.prevent="UpdateShow">
            <div>
          <p style="font-size: 15px;color: red;"><i>{{ error_msg }}</i></p>
            </div>
        <input type="text" class="form-control" v-model="details.show_name"><br>
        <textarea id="description" class="form-control" for="details.description" v-model="details.description"></textarea><br>

        <label for="show_time">Update Show Time</label>
        <input type="text" class="form-control" id="show_time" v-model="details.show_time"> <br>
        
        <label for="price">Update Price ₹</label>
        <input type="text" class="form-control" id="inlineFormInputGroup" v-model="details.price"> <br> 
        <label>Theater ID</label>
        <div class="form-control" disabled>{{ details.theater_id }}</div>
        
        <label for="image">Update Image/Poster</label>
            <input type="file" class="form-control" id="image" ref="image" @change="UpdateImg" accept="image\*"><br>
        <button type="submit" class="btn btn-warning" @click.prevent="UpdateShow">Update Show</button>
        <router-link :to="{name:'S_Details', params:{id:details.id}}" class="btn btn-primary ml-2">Cancel</router-link>
        </form>
    </div>
</div>
</template>

<script>

import axios from 'axios'
import T_NavBar from '@/components/T_NavBar.vue';

export default {
    name: 'ShowUpdate',
    components:{
        T_NavBar
    },
    data() {
        return {
            details:{
                show_name:'',
                description:'',
                show_time:'',
                price:'',
                theater_id:''
            },
            image: null,
            error_msg:''
            
            
        }
    },
    created(){
        this.fetchshowdetails()
    },

    methods:{
        fetchshowdetails(){
            const s_id = this.$route.params.id;
            fetch(`http://127.0.0.1:5000/admin/show/${s_id}`,{
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type':'application/json'
                }
            })
            .then(response => {
                if(response.status === 200){
                    return response.json()
                }else if(response.status === 401){
                    this.$router.push('/not-authorized')
                }else if(response.status === 404){
                    this.$router.push('/not-authorized')
                }
            }).then(data=>{
                this.details = data;     // fetching the data in 2nd promise "then" only.
            })
            .catch(error =>{
                console.log(error)
                alert('Something went wrong, Try again later :(')
            });
        },

        async UpdateShow(){
            const up_id = this.$route.params.id;
            const theater_id = this.details.theater_id;
            const fd = new FormData();

            fd.append('show_name',this.details.show_name);
            fd.append('description',this.details.description);
            fd.append('show_time',this.details.show_time);
            fd.append('price',this.details.price);
            fd.append('theater_id',theater_id);

            if(this.image){
                fd.append('m_image', this.image)
            }
            try{
                let auth_token = sessionStorage.getItem('auth_token')
                await axios.put(`http://127.0.0.1:5000/admin/show/update/${up_id}/theater/${theater_id}`,fd,{
                headers:{       
                    'Authentication-Token': auth_token,
                    'Content-Type':'multipart/form-data'

                }
            })
            this.$router.push('/admin/show/all')
            }catch(error){
            if(error.response.status=== 404){
                this.$router.push('/not-found')
            }else if(error.response.status=== 405){
                this.error_msg = error.response.data.message
                    // console.log(error)
            }else if(error.response.status=== 422){
                this.error_msg = error.response.data.message
        }   }        
    },
        UpdateImg(event){
            this.image = event.target.files[0]
    }
    }
}

</script>
            