<template>
<div>
    <user_NavBar/>
    <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 50px;">
        <h3 class="text-center">Search Shows</h3> <br>
        <p class="text-center">Use the search box to search for shows based on Show title or Genre.</p>
            <hr>
            <br>

        <form @submit.prevent="searchShows">
            <div class="form-group d-flex justify-content-centre">
                <input class="form-control" v-model="query" placeholder="Search for exciting shows and your fav genres" style="width: 70%;">
            <button type="submit" class="btn btn-warning">Search</button>
            </div>
        </form>
        <button @click="goBack()" class="btn btn-primary ml-3">Back</button>
    </div>
    </div><br>

        <div v-if="shows.length>0" class="container">
            <table class="table table-dark">
            <thead>
                <tr>
                    <th>Show ID</th>
                    <th>Show poster</th>
                    <th>Show_name</th>
                    <th>Theater name</th>
                    <th>Place</th>
                    <th>Location</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="s in shows" :key="s.id">
                    <td>{{ s.id }}</td>
                    <td>
                    <router-link :to="{name:'user_show_detail', params:{id:s.id}}">
                    <div class="image">
                        <img :src="s.m_image" alt={{s.show_name}} style="height: 170px; width: auto;">
                    </div>
                    </router-link>
                    <div v-for="g in s.tags" :key="g" style="color: whitesmoke ;">
                        {{ g }}
                        </div>
                </td>
                    <td>
                        <router-link :to="{name:'user_show_detail', params:{id:s.id}}" style="color:whitesmoke ;">
                        {{ s.show_name }}       
                    </router-link>
                </td>
                    <td>{{ s.theater.theater_name }}</td>
                    <td>{{ s.theater.t_place }}</td>
                    <td>{{ s.theater.location }}</td>
                </tr>
            </tbody>
            </table>
        </div>
        <div class="container text-center" v-else-if="query!==''">
            <p class="td-flex justify-content-center" style="font-size: 15px; color: brown;">
                <i>No Shows found for search entry "{{ query }}"
                <hr>
                Search another show and enjoy!!
            </i>
            </p>
        </div>
    </div>
</template>

<script>
import user_NavBar from '@/components/user_NavBar.vue';

export default{
    components: { user_NavBar },
    name:'show_search',
    data(){
        return {
            query:'',
            shows:[],
        }
    },

    methods:{
        async searchShows(){
            this.shows = [];

            if(!this.query){
                alert('Enter search item!!')
                return;
            }

            const resp =await fetch(`http://127.0.0.1:5000/user/shows/search?query=${this.query}`,{
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
                method:'GET'
            })
            if (resp.status===200){
                const data = await resp.json()
                this.shows = data;
            }else if(resp.status===401){
                this.$router.push('/not-authorized')
            }
            else{
                const error = await resp.text();
                console.log(error)
            }
        },
        goBack(){
            this.$router.push({name:'User_show'})
        }
        },

    // watch:{
    //     query: function(){
    //         this.searchShows();
    //     }
    // }
}
</script>

