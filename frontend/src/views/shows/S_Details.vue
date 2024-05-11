<template>
    <div>
        <T_NavBar/>
    <div class="container">
    <div class="d-flex flex-row-reverse" style="margin-top: 10px;">
        <router-link :to="{name: 'ShowUpdate', params:{id : show.id}}" class="btn btn-warning ml-2">Update Show</router-link>
        <button class="btn btn-danger btn-sm ml-2" data-bs-toggle="modal" data-bs-target="#exampleModal">Delete Show</button>
        <router-link :to="{name: 'ShowGet'}" class="btn btn-primary ml-2">Back</router-link>
    </div>
    <br>
    <div class="card border-dark shadow p-3 mb-5 bg-body rounded show-display">
    <div class="show-display">
                    <div class="content">
                    <div class="img rgt">
                        <img :src="show.m_image" alt={{show.show_name}} style="height: 250px; width: auto; object-fit: cover; flex-shrink: 0;">
                    </div>
                    <h2>{{ show.show_name }}</h2>
                    <h6 style="color: aliceblue; font-size: 20px;">About Show</h6>                    
                    <div class="description">
                        <p>{{ show.description }}</p>
                    </div>
                    <div class="genre-con">
                        <h6 style="color: aliceblue; font-size: 20px;">Genre </h6>
                        <p>{{ show.tags }}</p>
                    </div>
                    <h6 style="color: aliceblue; font-size: 20px;">Show Time</h6>
                    <p>{{ show.show_time }}</p> 
                    <h6 style="color: aliceblue; font-size: 20px;">Show price ₹</h6>
                    <p>₹ {{ show.price }}</p> 
                    <h6 style="color: aliceblue; font-size: 20px;">Show Rating</h6>                    
                    <p>{{ show.avg_rating }}/10.00</p>
                    <h6 style="color: rgb(164, 196, 223);">Show Added on</h6>
                    <p class="text-muted">{{ dateformat(show.show_added_on) }}</p>
                </div>


                <!-- DELETE SHOW MODEL -->

        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Delete Show - {{ show.show_name }}</h5>
                <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <i>Are you sure you want to delete this show?? </i>
            </div>
            <div class="modal-footer">
                <router-link :to="{name: 'S_Details', params:{ id : show.id}}" type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="cancelbutton">cancel</router-link>
                <button type="button" class="btn btn-danger" @click="deleteshow(show.id)">Delete</button>
            </div>
            </div>
        </div>
        </div>
    </div>
    </div>
    </div>
    </div>
</template>
<script>

import T_NavBar from '@/components/T_NavBar.vue';
 

export default {
    name: "S_Details",
    components:{
        T_NavBar
    },
    data() {
        return {
           show:[],
           admin_id:null
        };
    },
    async mounted(){
            await this.fetchshow()
        },
    methods: {
        
        async fetchshow(){
            const s_id = this.$route.params.id;
            const resp = await fetch(`http://127.0.0.1:5000/admin/show/${s_id}`,{
                headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type':'application/json'
                }
            })
            
            if(resp.status === 200){
                    const data =  await resp.json()
                    this.show = data;
                    this.admin_id = data.admin_id;
                }
                else if(resp.status === 401){
                    this.$router.push('/not-authorized')
                }else if(resp.status === 404){
                    this.$router.push('/not-found')
                }else{
                    const error = await resp.text()
                    console.log(error)
                    alert('Something went wrong, try again')
                }
            
        },
        dateformat(date_in){
            const d = new Date(date_in).toLocaleDateString();
            return d
        },
        

        async deleteshow(show_id){

            const resp = await fetch(`http://127.0.0.1:5000/admin/show/delete/${show_id}`,{
                    method: 'DELETE',
                    headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type':'application/json'
            },
                })
                if (resp.status===200){
                    console.log('Show Deleted')
                    this.$router.push('/admin/show/all')
                    document.getElementById('cancelbutton').click()

                } else {
                    if(resp.status === 401){
                        this.$router.push('/not-authorized')
                    }
                     if (resp.status === 404){
                        this.$router.push('/not-found')
                    } 
                    else{
                    const error = await resp.text()
                    console.log(error)
                    alert('Something went wrong, please try agin later')
                    }
                }
            }
        }
    }
</script>

<style>
.content{
    margin-left: 20px;
    
}
.show-display{
    background-color: #1a1919;
    justify-content: space-between;
}
/* .show-display img{
    height: 250px;
    object-fit: cover;
    flex-shrink: 0;
} */
.show-display .img.rgt{
    float: right;
    margin-left: 30px;
    margin-bottom: 10px;
}
.show-display h2{
    color: greenyellow;
    font-size: 50;

}

.show-display p{
    color: blanchedalmond;
    /* text-align: justify; */
    margin-bottom: 15px;
    
}
.description p{
    font-size: 15px;
    text-align: justify;  

}
</style>