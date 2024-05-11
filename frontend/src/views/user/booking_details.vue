<template>
    <div>
    <user_NavBar/>
        <div class="container"><br>
        <h3 class="text-center">Show Bookings</h3> <br>
        <div v-if="bookings.length === 0">
            <p class="text-center" style="font-size: 20px; color: brown;">
                <i>You don't have any bookings yet. Exciting shows await. Book your favorite seats now!
                <hr>
                Book Shows
                <router-link :to="{name: 'User_show'}" class="btn btn-success round">+</router-link>
            </i>
            </p>
        </div>

        <table class="table table-dark" v-else>
            <thead>
                <tr>
                    <th>Booking ID</th>
                    <th>Show</th>
                    <th>Theater</th>
                    <th>Place</th>
                    <th>Location</th>
                    <th>Num of Tickets</th>
                    <th>Total Amount </th>
                    <th>Rate the show</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="bk in bookings" :key="bk.id">
                    <td>{{ bk.id }}</td>
                    <td>{{ bk.show_booked }}</td>
                    <td>{{ bk.theater_booked }}</td>
                    <td>{{ bk.theater_place }}</td>
                    <td>{{ bk.theater_location }}</td>
                    <td style="padding-left: 50px;">{{ bk.num_of_tickets }}</td>
                    <td>{{ bk.tot_cost }}</td>
                    <td>
                        <button @click="rateshowmodel(bk.user_id,bk.theater_id,bk.show_id,bk.show_booked,bk.id)" class="btn btn-sm btn-warning" data-bs-toggle="modal" data-bs-target="#exampleModal">Rate</button>
                        <button @click="delbooking(bk.user_id,bk.theater_id,bk.show_id,bk.show_booked,bk.id,bk.num_of_tickets)" class="btn btn-sm btn-danger ml-2" data-bs-toggle="modal" data-bs-target="#exampleModal_1">cancel</button>

                    </td>
                </tr>
            </tbody>
        </table>

                <!-- RATING SHOW MODEL -->

        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel"> {{ show_selected_for_rating }}</h5>
                    <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <i>Rate Show</i><hr>
                    <div v-if="rating<=0 || rating>10">
                        <h6 style="color: rgba(232, 97, 97, 0.901);">Rate the show between 1 to 10</h6>
                    </div>
                    <input id="title" class="form-control" type="number" min="1" max="10" v-model.number="rating" placeholder="Rate the show from 1 to 10" required/><br>
                    <textarea id="review" class="form-control" type="text" v-model="review" placeholder="Review about Show" required></textarea><br> 
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="cancel" id="cancelbutton">Cancel</button>
                    <button type="button" class="btn btn-warning" @click="rating_show(user_id,t_id,show_rating_id,b_id)">Rate Show</button>
                </div>
                </div>
                </div>
                </div>

                <!-- CANCEL BOOKING MODEL -->

            <div class="modal fade" id="exampleModal_1" tabindex="-1" role="dialog" aria-labelledby="exampleModal_1Label" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModal_1Label"> Cancel Booking</h5>
                    <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to cancel booking order??</p>
                    <p> Show: {{ show_selected_for_cancel }}</p>
                    <p> Num of tickets: {{ tickets }}</p>

                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="cancel" id="cb">Back</button>
                    <button type="button" class="btn btn-danger" @click="cancel_booking(user_id,t_id,show_rating_id,b_id)" id="cancelbutton">Cancel</button>
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
  components: { user_NavBar },
    name:'booking_details',
    data(){
        return{
            bookings:[],
            rating:null,
            review:'',
            show_selected_for_rating:'',
            show_selected_for_cancel:'',
            tickets:null,
            show_rating_id:null,
            t_id:null,
            user_id:null,
            b_id:null,
        }
    },
    mounted(){
        const user_id = this.$route.params.user_id;
        const current_user = sessionStorage.current_user;
        if(user_id !== current_user){   
            this.$router.push('/not-authorized')
        }else{
            this.booking_details()
        }
    },
    methods:{
        async booking_details(){
          

            const u_id = this.$route.params.user_id;
            const response = await fetch(`http://127.0.0.1:5000/user/${u_id}/booking/details`,{
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type': 'application/json'
                },
                method:'GET'
            })
            if(response.status === 200){
                const details = await response.json();
                this.bookings = details;
            }
            else if(response.status===401){
                this.$router.push('/not-authorized')
            }else if(response.status===404){
                this.$router.push('/not-found')
            }else if(response.status===403){
                this.$router.push('/not-authorized')
            }else{
                const error = response.text();
                console.log(error);
                alert('Something went wrong, try again later')
            }
        },
        rateshowmodel(u_id,t_id,s_id,s_name,b_id){
            this.show_selected_for_rating = s_name;
            this.show_rating_id  = s_id;
            this.t_id = t_id;
            this.user_id = u_id;
            this.b_id = b_id;


        },
        delbooking(u_id,t_id,s_id,s_name,b_id,tickets){
            this.show_rating_id = s_id;
            this.b_id = b_id;
            this.show_selected_for_cancel = s_name;
            this.t_id = t_id;
            this.tickets = tickets;
            this.user_id=u_id;
        },
        cancel(){
            this.show_selected_for_rating = null;
            this.t_id=null;
            this.user_id=null;
            this.show_selected_for_cancel = null;
            this.b_id = null;
            this.tickets = null;

        },
        async rating_show(u_id,t_id,s_id,b_id){

            if(this.rating<=0 || this.rating>10){
                alert("Rate the show between 1 to 10")
                return;
            }

            const response = await fetch(`http://127.0.0.1:5000/user/${u_id}/${t_id}/${s_id}/${b_id}`,{
                method:'POST', 
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
                body: JSON.stringify({
                        review:this.review,
                        rating:this.rating
            })
        })
            if(response.status === 200){
                document.getElementById('cancelbutton').click()
                await this.booking_details()
                const user_id = this.user_id;
                alert('Review successful !! Thank you for your valuable feedback!')
                this.$router.push({name: 'booking_details', params:{ user_id : user_id}})

            }else if(response.status===400){
                alert('Alredy Show has been reviewd by you...')
                return; 
            }else if(response.status===405){
                alert("Rate the show between 1 to 10")
                return;
            }else if(response.status===404){
                document.getElementById('cancelbutton').click()
                this.$router.push('/not-found')
            }else if(response.status===403){
                document.getElementById('cancelbutton').click()
                this.$router.push('/not-authorized')
            }else{
                const error = await response.text()
                console.error(error)
                alert('Something went wrong, Try again later')
            }

        },


        async cancel_booking(u_id,t_id,s_id,b_id){
            const response = await fetch(`http://127.0.0.1:5000/user/${u_id}/theater/${t_id}/show/${s_id}/booking/${b_id}`,{
                method:'DELETE',
                headers:{
                    'Authentication-Token': sessionStorage.auth_token,
                    'Content-Type':'application/json'
                },
            })
            if(response.status === 200){
                document.getElementById('cb').click()
                await this.booking_details()
                this.$router.push({name:'User_show'})
                
            }else if(response.status===404){
                this.$router.push('/not-found')
                document.getElementById('cb').click()
            }else if(response.status===403){
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