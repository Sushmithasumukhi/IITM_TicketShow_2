<template>
    <div>
        <user_NavBar/><br>
        <div class="container">
            <div class="m_t">
                <div v-for="t in t_det" :key="t.theater_id">
                <div class="card shadow p-3 mb-5 bg-body rounded theater-card">
                    <h2 style="color: aquamarine;">{{ t.theater_name }}</h2>
                    <p style="color: cadetblue; font-size: 18px;">{{ t.t_place }}, {{ t.location }}</p>
                        <div class="show-list">
                            <div v-for="s in t.shows_present"  :key="s.id" class='show-card'>
                                <router-link :to="{name: 'user_show_detail', params:{id : s.id}}">
                                <h5 style="color: yellowgreen;">{{ s.show_name }}</h5>
                                <img :src="s.m_image" alt={{s.show_name}} class="s-img" style="width: 170px; height: 170px;">
                                <div class="badge badge-success genre" v-for="genre in s.tags" :key="genre">{{ genre }}</div> <br>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

import user_NavBar from '@/components/user_NavBar.vue';

export default {
    name:'User_show',
    components:{
        user_NavBar
    },
    data(){
        return{
            t_det : []
        };
    },
    async mounted(){
        await this.details()
    },
    methods:{
        async details(){
        const response = await fetch('http://127.0.0.1:5000/user/theaters/shows',{
            headers:{
                    'Authentication-Token':sessionStorage.auth_token,
                    'Content-Type':'application/json'
            },
            method:'GET'
        })
        if (response.status===200){
            const details = await response.json()
            this.t_det = details;
        }else{
            const error = await response.text()
            console.log(error)
        }
    }
}
}
</script>
<style>

.show-card {
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-right: 10px;
    margin-left:10px;
    padding: 10px;
    /* display: grid; */
    width: 200px;
    
 }

.theater-card{
    overflow-x: auto;
    background-color: #1a1919;
}   

.show-list{
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: auto;
}
.s-img{
    flex-shrink: 0;
    border-radius: 8px 8px 0 0;
    /* object-fit: cover; */
}
.genre{
    width: fit-content;
    justify-content: center;
}
</style>


