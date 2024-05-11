<template>
    <div>
        <user_NavBar/><br>
        <div class="container show-display">
            <div class="content" v-for="s in t_del" :key="s.theater.id">
                    <h2>{{ s.theater.theater_name }}</h2>
                    <div>
                        <p>{{ s.theater.t_place  }}</p>
                    </div>
                    <div class="t_place">
                        <p>{{ s.theater.loaction  }}</p>
                    </div>
                    <router-link :to="{name: 'user_show_detail', params:{id:s.id}}">
                        <div class="image">
                        <img :src="s.m_image" alt={{s.show_name}}>
                        </div>
                        <div>
                            <p>{{ s.tags }}</p>
                        </div>
                    </router-link>
                </div>
                </div><br>

    </div>
</template>
<script>
import user_NavBar from '@/components/user_NavBar.vue';

export default {
    name:'theater_details',
    components:{
        user_NavBar
    },
    data(){
        return{
            t_del:[]
        }
    },
    mounted(){
        this.fetchTheaterDetails()
    },
    methods:{
        async fetchTheaterDetails(){
            const t_id = this.$route.params.id
            const resp = await fetch(`http://127.0.0.1:5000/user/theater/${t_id}`,{
                headers:{
                    'Authentication-Token':sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
                method:'GET'
            })

            if(resp.status===200){
                const data = await resp.json()
                this.t_del=data;
            }else if(resp.status == 404){
                this.$router.push('/not-found')
            }else if(resp.status==401){
                this.$router.push('/not-authorized')
            }else{
                const error = await resp.text()
                console.log(error)
                alert('something went wrong')
            }
        }
    }
}
</script>

<style>
.content{
    margin-left: 20px;
    padding: 10px;    
}
.show-display{
    background-color: #1a1919;
    justify-content: space-between;
    border-radius: 8px;
}
.show-display image{
    height: 250px;
    object-fit: cover;
    flex-shrink: 0;
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
</style>