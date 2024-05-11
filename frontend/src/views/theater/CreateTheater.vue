<template>
    <div v-if="isAuth">
        <T_NavBar/>
    <div class="container">
        <br>
        <div class="container text-center">
            <h3>Add New Theater</h3>
            <br>
        </div>
      <form @submit.prevent="AddTheater">
          <input type="text" class="form-control" v-model="theater_name" placeholder=" Enter Theater Name : eg. IONIX, PVR" required>
          <p style="font-size: 15px;color: red;"><i>{{ error_msg }}</i></p>
          <input type="text" class="form-control" v-model="t_place" placeholder="Enter Theater Place : eg. Orion Mall" required>
          <br>
          <input type="text" class="form-control" v-model="location" placeholder="Enter Location : eg. Bengaluru" required>
          <br>
          <input type="number" class="form-control" v-model="seat_capacity" placeholder="Enter Seating Capacity : eg. 100" required>
        <br>
          <button type="submit" class="btn btn-primary">Add Theater</button>
        <router-link :to="{name:'GetTheater'}" class="btn btn-dark ml-3">Back</router-link>

      </form>
        </div>
  </div>
</template>

<script>
import T_NavBar from '@/components/T_NavBar.vue';

export default{
    name: 'CreateTheater',
    components:{
        T_NavBar
    },
  data() {
      return {
          theater_name: '',
          t_place:'',
          location:'',
          seat_capacity:null,
          error_msg:'',
          isAuth: false
      }
  },
  beforeMount(){
        const auth_token = sessionStorage.getItem('auth_token');
        if(auth_token){
            this.isAuth = true;
        }else{
            this.$router.push('/not-authorized')
        }
  },
  methods: {
      async AddTheater(){
        const resp = await fetch("http://127.0.0.1:5000/admin/theater/create",{
            method : 'POST',
            headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type':'application/json'
            },
            body: JSON.stringify({
                theater_name:this.theater_name,
                t_place:this.t_place,
                location:this.location,
                seat_capacity:this.seat_capacity
            })
        })
            if (resp.status === 200){
                this.$router.push('/admin/theater')
            }else if(resp.status===405){
                const error = await resp.json()
                this.error_msg = error.message
            }else{
                const error = await resp.text()
                console.error(error)
                alert('Something went wrong, Try again later')
                }
        }
      },
}
</script>
