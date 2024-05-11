<template>
    <div>
        <T_NavBar/>
    <div class="container"><br>
        <h3>Shows in {{ theater.theater_name }}, {{ theater.t_place }}</h3> <br><br>
        <div v-if="show_details.length === 0">
            <p class="text-center" style="font-size: 25px;">
                <i>There are no Shows
                <hr>
                Add new show <br> 
                <button class="btn btn-success rounded-circle" style="font-size: 25px;" @click="addshow"> + </button> </i>
            </p>
        </div>
        <table class="table table-secondary" v-else>
            <thead>
                <tr>
                    <th>Show ID</th>
                    <th>Name</th>
                    <th>Time Slot</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="s in show_details" :key="s.id">
                    <td>{{ s.id }}</td>
                    <td>
                        <router-link :to="{ name: 'S_Details', params:{ id : s.id }}"> {{ s.show_name }} </router-link>
                    </td>
                    <td>{{ s.show_time }}</td>
                </tr>
            </tbody>
        <button class="btn btn-success rounded-circle"  @click="addshow"> + </button><br>
        </table>
        <router-link :to="{name : 'GetTheater'}" class="btn btn-primary">Back</router-link>

    </div>
    </div>
</template>
<script>
import T_NavBar from '@/components/T_NavBar.vue'
export default {
    name : 'ViewShow',
    components:{
        T_NavBar
    },
    data() {
        return{
            theater : [],
            show_details : [],
        }
        
    },

    mounted(){
        this.fetchshows()
    },
    methods: {
        fetchshows(){
            const t_id = this.$route.params.id;
            fetch(`http://127.0.0.1:5000/admin/theater/${t_id}`,{
                headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type':'application/json'
                }
            })
            .then(resp => {
                if(resp.status===200){
                    return resp.json()
                }else if(resp.status === 401){
                    this.$router.push('/not-authorized')
                }else if(resp.status === 404){
                    this.$router.push('/not-found')
                }
            })
            .then( data => {
                this.theater = data;
                this.show_details = data.shows;
            }).catch(error =>{
                console.log(error)
                alert('Something went wrong, try again later :(')
            })
        },
        addshow(){
            const theater_id = this.theater.id
            this.$router.push({name:'AddShow', params:{ id : theater_id}})
        }
    },
}
</script>
