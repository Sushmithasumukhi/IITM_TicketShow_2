<template>
    <div>
        <T_NavBar/>
        <br>
        <div class="container">
        <div class="text-center">
            <h3>Update Theater - {{ theater_name }}</h3>
            <br>
        </div>
      <form @submit.prevent="updateTheater">
            <div>
            <p style="font-size: 15px;color: red;"><i>{{ error_msg }}</i></p>
            </div>
          <input type="text" class="form-control" v-model="theater.theater_name" placeholder=" Enter Theater Name : eg. IONIX, PVR" required>
          <br>
          <input type="text" class="form-control" v-model="theater.t_place" placeholder="Enter Theater Place : eg. Orion Mall" required>
          <br>
          <input type="text" class="form-control" v-model="theater.location" placeholder="Enter Location : eg. Bengaluru" required>
          <br>
          <input type="number" class="form-control" v-model="theater.seat_capacity" placeholder="Enter Seating Capacity : eg. 100" required>
        <br>
          <button type="submit" class="btn btn-primary">Update</button>
          <button class="btn btn-dark ml-3" @click="GoBack">Cancel</button>
      </form>
        </div>
  </div>
</template>
<script>
import T_NavBar from '@/components/T_NavBar.vue';

export default {
    name: 'UpdateTheater',
    components:{
        T_NavBar
    },
    data() {
        return {
            id:'',
            theater:{
                theater_name : '',
                t_place:'',
                location:'',
                seat_capacity:'',
            },
            error_msg:''
        }
        
    },

    mounted() {
        this.fetchTheater()
    },
    created(){
        this.theater_name = this.$route.query.theater_name || '';
    },

    methods: {
        fetchTheater(){
            const t_id = this.$route.params.id;
            fetch(`http://127.0.0.1:5000/admin/theater/${t_id}`,{
                headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type': 'application/json'
            }})
            .then(resp => {
                if(resp.status === 200){
                    return resp.json()
                }else if(resp.status === 404){
                    this.$router.push('/not-found')
                }else if(resp.status === 401 || resp.status === 403){
                    this.$router.push('/not-authorized')
                }
            })
            .then(data => {
                this.theater = data;
            })
            .catch(error => {
                console.log(error)
                alert('Something went wrong')
            })
        },

        updateTheater(){
            const t_id = this.$route.params.id;
            const t_data = {
                theater_name : this.theater.theater_name,
                t_place : this.theater.t_place,
                location : this.theater.location,
                seat_capacity : this.theater.seat_capacity
            }
            fetch(`http://127.0.0.1:5000/admin/theater/update/${t_id}`,{
                method:'PUT',
                headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type': 'application/json'
            },
                body: JSON.stringify(t_data)
            })
            .then(resp => {
                if(resp.status === 200){
                    console.log('Theater Updated')
                    this.$router.go(-1)
                    return resp.json()
                }else if(resp.status === 404){
                    this.$router.push('/not-found')
                }else if(resp.status === 401 || resp.status === 403){
                    this.$router.push('/not-authorized')
                }
            })
            .catch(error =>{
                console.log(error)
                alert('Something went wrong')
                }
            )
        },
        GoBack(){
            this.$router.push('/admin/theater')
        }
    },
}
</script>