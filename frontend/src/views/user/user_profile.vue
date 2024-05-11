<template>
    <div>
    <user_NavBar/>
    <div class="container" style="margin-top: 30px;">
        <div class="user">
        <h2>{{ u_details.username }}</h2>
        <p>{{ u_details.email }}</p>
    </div><br>
        
            <h3 style="background-color: rgb(66, 72, 72); padding: 10px; font-family: cursive; color: beige;">REVIEWS</h3><hr>  
        <!-- <div class="card border-dark shadow p-3 mb-5 bg-body rounded"> -->
            <div style="color: rgb(174, 212, 245);">{{ error_msg }}</div>
            <!-- <div v-if="usr_details.length > 0"> -->
                <div class="card shadow mb-3 bg-body rounded" v-for="r in u_details.reviews" :key="r.id">
                    <div class="box">
                    <button style="margin-left: 950px;" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#exampleModal" @click="deleteReview(r.rate_id, r.id)"><b>Delete Review</b></button>
                    <div class="img rgt">
                        <img :src="r.m_image" alt={{r.show_name}}>
                    </div>
                    <router-link :to="{name: 'user_show_detail', params:{id:r.id}}"> 
                    <h2>{{ r.show_name }}</h2></router-link>
                    <h6 style="color: aliceblue; font-size: 15px;">Ratings given</h6>
                    <p>{{ r.rating }}/10</p>                  
                    <h6 style="color: aliceblue; font-size: 15px;">Review</h6>
                    <p>{{ r.review }}</p> 
                    <h6 style="color: rgb(164, 196, 223);">Show Added on</h6>
                    <p class="text-muted">{{ dateformat(r.date) }}</p>
                    </div><br>
            </div>
        </div>
                            <!-- --------------- DELETE REVIEW MODEL --------------------- -->
        <div>
            <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ratings/Review Delete</h5>
                    <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to delete your rating/review ??</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="cancelbutton" @click="cancel">Back</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" id="cb" @click="deletefetch(rate_id,show_id)">Delete</button>
                </div>
                </div>
                </div>
                </div>                     
            
        </div>
    </div>
<!-- </div> -->
    <!-- </div> -->
</template>
<script>
import user_NavBar from '@/components/user_NavBar.vue'

export default {
    name: 'user_profile',
    components:{
        user_NavBar
    },
    data(){
        return{
            u_details:[],
            error_msg:'',
            show_id:null,
            rate_id:null
        }
    },
    mounted(){
        this.fetch_user()
    },
    methods:{
        async fetch_user(){
            const id = this.$route.params.id
            const response = await fetch(`http://127.0.0.1:5000/user/${id}`,{
                headers:{
                    'Authentication-Token':sessionStorage.auth_token,
                    'Content-Type':'application/json'
                }
            })
            if(response.status === 200){
                const data = await response.json();
                this.u_details = data;
            }else if(response.status === 404){
                this.$router.push('/not-found')
            }else if(response.status === 401 || response.status === 403){
                this.$router.push('/not-authorized')
            }else if(response.status === 408){
                this.error_msg = 'No Reviews provided by you...'
            }else{
                const error = response.text();
                console.log(error)
            }
        },
        dateformat(date_in){
            const d = new Date(date_in).toLocaleDateString();
            return d
        },
        deleteReview(rate_id, show_id){
            this.show_id = show_id;
            this.rate_id = rate_id;
        },
        cancel(){
            this.show_id = null;
            this.rate_id = null;
        },
        async deletefetch(rate_id,show_id){
            const user_id = this.u_details.id;
            const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/show/${show_id}/review/${rate_id}`,{
                method:'DELETE',
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
            })
            
            if(response.status === 200){
                document.getElementById('cancelbutton').click()
                await this.fetch_user()
                this.$router.push({name:'User_show'})
            }else if(response.status === 404){
                this.$router.push('/not-found')
                document.getElementById('cb').click()
            }else if(response.status === 403){
                document.getElementById('cb').click()
                this.$router.push('/not-authorized')
            }else{
                const error = await response.text()
                console.error(error)
                alert('Something went wrong, Try again later')
            }
        }
    }
}
</script>


<style>
    
.box{
    background-color: #1a1919;
    justify-content: space-between;
    border: 1px solid blanchedalmond;
    padding: 20px;
}
.box img{
    height: 150px;
    object-fit: cover;
    flex-shrink: 0;
}
.box .img.rgt{
    float: right;
    margin: 10px;
}
.box h2{
    color: greenyellow;
    font-size: 50;

}

.box p{
    color: blanchedalmond;
    margin-bottom: 15px;
    
}
.user{
    background: rgb(56, 54, 54);
    border-radius: 8px 8px 8px 8px;
    padding-left: 20px;
    padding: 20px;
    font-family:cursive;
    color:cornsilk;
}


</style>