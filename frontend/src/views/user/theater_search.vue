<template>
    <div>
    <user_NavBar/>
        <div class="container d-flex justify-content-center mt-5">
        <div class="col-lg-6 col-md-8 col-sm-10" style="margin-top: 50px;">
        <h3 class="text-center">Search Theater</h3> <br>
        <p class="text-center">Use the search box to search for theaters based on Name, Location, Place.</p>
            <hr>
            <br>

        <form @submit.prevent="fetchTheaterSearch">
            <div class="form-group d-flex justify-content-centre">
                <input class="form-control" v-model="query" placeholder="Search Theaters.." style="width: 70%;">
                <button type="submit" class="btn btn-warning">Search</button>
            </div>
        </form>
        <button @click="goBack()" class="btn btn-primary">Back</button>
        </div>
        </div>
            <div v-if="theater_details.length>0" class="container justify-content-center mt-5">
            <table class="table table-dark">
            <thead>
                <tr>
                    <th>Theater ID</th>
                    <th>Theater name</th>
                    <th>Place</th>
                    <th>Location</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="t in theater_details" :key="t.id">
                    <td>{{ t.id }}</td>
                    <td>
                        <router-link :to="{name:'theater_details', params:{id:t.id}}">
                        {{ t.theater_name }}
                        </router-link>
                    </td>
                    <td>{{ t.t_place }}</td>
                    <td>{{ t.location }}</td>
                </tr>
            </tbody>
            </table>
        </div>
        <div class="container text-center" v-else-if="query !== ''">
            <p class="td-flex justify-content-center" style="font-size: 15px; color: brown;">
                <i>No Theater found for search entry "{{ query }}"
                <hr>
                Search another theater and book shows!!
            </i>
            </p>
        </div>
    </div>
</template>

<script>
import user_NavBar from '@/components/user_NavBar.vue';

export default {
    components: { user_NavBar },
    name:'theater_search',
    data(){
        return{
            query:'',
            theater_details:[]
        }
    },
    methods:{
        async fetchTheaterSearch(){

            this.theater_details = [];
            if(!this.query){
                alert('Enter search item!!')
                return;
            }

            const resp = await fetch(`http://127.0.0.1:5000/user/theaters/search?query=${this.query}`,{
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
                method:'GET'
            })
            if (resp.status===200){
                const data = await resp.json()
                this.theater_details = data;
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
    }
}
</script>