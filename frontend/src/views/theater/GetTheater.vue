<template>
    <div>
     <T_NavBar/>
    <div class="container"><br>
        <h3 class="text-center">Theaters</h3> <br>
        <div v-if="theaters.length === 0">
            <p class="text-center" style="font-size: 20px; color: brown;">
                <i>There are no theaters
                <hr>
                create new theater by using navbar.
            </i>
            </p>
        </div>

        <table class="table table-dark" v-else>
            <thead>
                <tr>
                    <th>Theater ID</th>
                    <th>Name</th>
                    <th>place</th>
                    <th>Location</th>
                    <th>Seat Capacity</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="t in theaters" :key="t.id">
                    <td>{{ t.id }}</td>
                    <td>{{ t.theater_name }}</td>
                    <td>{{ t.t_place }}</td>
                    <td>{{ t.location }}</td>
                    <td>{{ t.seat_capacity }}</td>
                    <td>
                        <router-link :to="{ name: 'ViewShow', params: { id : t.id}}" class="btn btn-warning btn-sm">View Shows</router-link>
                        <button @click="deletemodalshow(t.theater_name,t.id)" class="btn btn-danger btn-sm ml-2" data-bs-toggle="modal" data-bs-target="#exampleModal">Delete</button>
                        <router-link :to="{ name: 'UpdateTheater', params: { id : t.id}, query:{theater_name : t.theater_name} }" class="btn btn-success btn-sm ml-2">Update</router-link>
                        <button @click="export_csv(t.id)" class="btn btn-info btn-sm ml-2">export</button>
                    </td>
                </tr>
            </tbody>
        </table>

                                <!-- ----------------- DELETE MODEL-------------------  -->
        <div>
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Delete Theater - {{ Theater_Selected }}</h5>
                <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <i>Are you sure you want to delete this theater?? </i>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="cancel" id="cancelbutton">Cancel</button>
                <button type="button" class="btn btn-danger" @click="deletetheater(del_id)">Delete</button>
            </div>
            </div>
        </div>
        </div>
    </div>
    </div>
    </div>

</template>

<script>
import T_NavBar from '@/components/T_NavBar.vue'


export default {
    name: 'GetTheater',
    components:{
        T_NavBar
    },
    data() {
        return {
            theaters:[],
            Theater_Selected: null,
            del_id:'',
        }
    },
    mounted(){
        this.get_theater()
    },      
    methods:{
        get_theater(){
            fetch('http://127.0.0.1:5000/admin/get/theater',{
                headers:{
                'Authentication-Token': sessionStorage.auth_token,
                'Content-Type':'application/json'
                }
            })
            .then(resp => {
                if(resp.status === 200){
                    return resp.json()
                }else if(resp.status === 401){
                    this.$router.push('/not-authorized')
                }else if(resp.status === 404){
                    this.$router.push('/not-found')
                }
            })
            .then(data => {
                this.theaters = data;
            })
            .catch(error =>{
                console.log(error)
                alert('Something went wrong, Unable to fetch theater....  ')
            })
            },

        deletemodalshow(t,id){
            this.Theater_Selected = t;
            this.del_id = id
        },
        cancel(){
            this.Theater_Selected = null;
        },
        async deletetheater(del_id){

            const resp = await fetch(`http://127.0.0.1:5000/admin/theater/delete/${del_id}`,{
                    method: 'DELETE',
                    headers:{
                        'Authentication-Token': sessionStorage.auth_token,
                        'Content-Type':'application/json'
                    }
                })
                if (resp.status === 200){
                    console.log('Theater Deleted')
                    document.getElementById('cancelbutton').click()
                    this.get_theater()
                    this.$router.push('/admin/theater')
                } else {
                    if(resp.status === 401){
                        this.$router.push('/not-authorized')   
                    }
                     if (resp.status === 404){
                        this.$router.push('/not-found')  
                    } else{
                    const error = await resp.json()
                    console.log(error)
                    alert('Something went wrong, please try agin later')
                    }
                }
            },
            async export_csv(id){
                const response = await fetch(`http://127.0.0.1:5000/admin/theater/export/${id}`,{
                    method: 'GET',
                    headers:{
                        'Authentication-Token': sessionStorage.auth_token,
                        'Content-Type':'application/json'
                    }
                })

                if(response.status === 200){
                    alert('CSV file generated and emailed to you!')
                    return;
                }else if(response.status === 401){
                    this.$router.push('/not-authorized')  
                }else if(response.status === 404){
                    this.$router.push('/not-found')  
                }else{
                    const error = await response.text()
                    console.log(error)
                    alert('Something went weong while exporting, try again later')
                }
            }
        }
    }
</script>
