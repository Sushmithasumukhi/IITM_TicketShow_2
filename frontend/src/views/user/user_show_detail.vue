<template>
    <div>
    <user_NavBar/>
    <div class="container" style="margin-top: 30px;">
        <div class="card border-dark shadow p-3 mb-5 bg-body rounded show-display md-8 mx-auto">
            <div v-if="show_display.length===0" style="color: aliceblue;">No Shows found..</div>
            <div v-else>
                
                <div class="show-display">
                    <div class="content">
                    <div class="img rgt">
                        <img :src="show_display.m_image" alt={{show_display.show_name}} style="width: auto; height: 250px;">
                    </div>
                    <h2>{{ show_display.show_name }}</h2>
                    <h6 style="color: aliceblue; font-size: 20px;">About Show</h6>                    
                    <div class="description">
                        <p>{{ show_display.description }}</p>
                    </div>
                    <div class="genre-con">
                        <h6 style="color: aliceblue; font-size: 20px;">Genre </h6>
                        <p>{{ show_display.tags }}</p>
                    </div>
                    <h6 style="color: aliceblue; font-size: 20px;">Show Time</h6>
                    <p>{{ show_display.show_time }}</p> 
                    <h6 style="color: aliceblue; font-size: 20px;">Show price ₹</h6>
                    <p>₹ {{ show_display.price }}</p>
                    <h6 style="color: aliceblue; font-size: 20px;">Show Rating</h6>                    
                    <p style="font-size: larger;">{{ show_display.show_ratings }}/10.00</p>
                    <h6 style="color: rgb(164, 196, 223);">Show Added on</h6>
                    <p class="text-muted">{{ dateformat(show_display.show_added_on) }}</p>                    
                </div>
                </div>
                <div class="container" v-if="show_display.seats_available > 0">
                    <h4 style="color: aliceblue;">Tickets Available : {{ show_display.seats_available  }}</h4>
                </div>
                <div v-else class="container">
                    <h5 style="color: #ad3838">HOUSEFULL, please book another show and enjoy!!</h5>
                </div>
                <br>
                <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#exampleModal">Book Show</button>
                <button type="button" class="btn btn-primary ml-4" @click="goBack()">Back</button>



            <!-- BOOKING MODEL -->

                <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel"> {{ show_display.show_name }}</h5>
                    <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <i>Booking Show</i><hr>
                    <input id="title" class="form-control" type="number" min="1" v-model="no_of_tickets" placeholder="Enter number of tickets" required/><br>
                    <small style="font-size: 20px;"><b>Total cost: ₹{{ no_of_tickets*show_display.price }}</b></small>
                </div>
                <div class="modal-footer">
                    <router-link :to="{name: 'user_show_detail', params:{ id : show_display.id}}" type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="cancelbutton">cancel</router-link>
                    <div v-if="show_display.seats_available > 0">
                        <button type="button" class="btn btn-warning" @click="bookticket(show_display.user_id,show_display.theater_id,show_display.id)" id="cancelbutton">Book show</button>
                    </div>
                    <div v-else>
                        <button type="button" class="btn btn-danger">HOUSEFULL</button>
                    </div>
                </div>
                </div>
                </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="row mb-5">
            <div class="col-md-8 col-xl-6 mx-auto" v-for="r in show_display.reviews" :key="r.id">
                <div class="card border-dark shadow p-3 mb-5 bg-body rounded show-display">
                    <h3 style="color: azure;">{{ r.username }}</h3>
                    <p>{{ r.rating }}/10</p>
                    <p>{{ r.review }}</p>
                    <p class="text-muted">{{ dateformat(r.date) }}</p>                    
                </div>
            </div>
            
        </div>
    </div>
    </div>
</template>
<script>
    
import user_NavBar from '@/components/user_NavBar.vue'

export default {
    name : 'user_show_detail',
    components:{
        user_NavBar
    },
    data() {
        return{
            show_display:[],
            no_of_tickets:null,
            tot_cost:null,
        }
        
    },
    mounted(){
        this.fetchshowdetailsfordisplay()
    },
    methods:{
        dateformat(date_in){
            const d = new Date(date_in).toLocaleDateString();
            return d
        },
        async fetchshowdetailsfordisplay(){
            const s_id = this.$route.params.id;
            const auth_token = sessionStorage.getItem('auth_token')
            const response = await fetch(`http://127.0.0.1:5000/user/shows/${s_id}`,{
                headers:{
                    'Authentication-Token':auth_token,
                    'Content-Type':'application/json'
                },
                method:'GET'
            })
            if(response.status==200){
                const data = await response.json()
                this.show_display = data
            }else if(response.status == 404){
                this.$router.push('/not-found')
            }else if(response.status==401){
                this.$router.push('/not-authorized')
            }
        },

        async bookticket(u_id,t_id,s_id){
            const response = await fetch(`http://127.0.0.1:5000/user/booking/${u_id}/theater/${t_id}/show/${s_id}`,{
                headers:{
                    'Authentication-Token':sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
                method:'POST',
                body: JSON.stringify({
                    no_of_tickets:this.no_of_tickets
                })
            })
            const user_id = this.show_display.user_id;
            if (response.status === 200){
                document.getElementById('cancelbutton').click()
                this.$router.push({name:'booking_details', params:{user_id}})
            }else if(response.status===401 || response.status === 403){
                document.getElementById('cancelbutton').click()
                this.$router.push('/not-authorized')
            }else if(response.status===404){
                document.getElementById('cancelbutton').click()
                this.$router.push('not-found')
            }else if(response.status===405){
                alert('Housefull, please book different show and enjoy!!')
                return; 
            }else{
                const error = await response.text()
                console.log(error)
                alert('Something went wrong, try again later')
            }
        },
        goBack(){
            this.$router.push({name:'User_show'})
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
.show-display img{
    height: 250px;
    object-fit: cover;
    flex-shrink: 0;
}
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
    margin-bottom: 15px;
    
}
.description p{
    font-size: 15px;
    text-align: justify;  

}


</style>