<template>
    <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="#">TicketShow</a>
                <button class="navbar-toggler" type="button" @click="$emit('toggleDropdown')" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            <div class="collapse navbar-collapse" id="navbarNav" :class="{'show':'dropdown'}">
            <ul class="navbar-nav">
            <li class="nav-item">
                <router-link :to="{name : 'User_show'}" class="nav-link active">All Shows</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{name : 'show_search'}" class="nav-link active">Show Search</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{name : 'theater_search'}" class="nav-link active">Theater Search</router-link>
            </li>
            <div v-if="user.id">
            <li class="nav-item">
                <router-link :to="{name : 'user_profile', params:{id: user.id}}" class="nav-link active">Profile</router-link>
            </li>
            </div>
            <div v-if="user.id">
            <li class="nav-item">
                <router-link :to="{name : 'booking_details', params:{user_id: user.id}}" class="nav-link active">Bookings</router-link>
            </li>
            </div>
            <li class="nav-item" v-if="user.id">
                <a class="nav-link active btn" @click="logoutuser()">Logout</a>
            </li>
            </ul>
        </div>
        </nav>
    </div>
</template>

<script>
export default{
    name:'T_NabBar',
    data(){
        return{
            user:{
                id:null
            }
        }
    },
    // props:{
    //     dropdown:{
    //         type: Boolean,
    //         required: true
    //     }
    // },
    created(){
        this.user.id = sessionStorage.getItem('current_user')
    },
    methods: {
        async logoutuser(){
			const logoutresp = await fetch('http://127.0.0.1:5000/logout', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				// flask security somehow requires an empty body to be sent to return a json response on a POST request
				body: JSON.stringify({})
			})
            if(logoutresp.ok){
                sessionStorage.removeItem('auth_token')
                sessionStorage.removeItem('current_user')
                this.$router.push({ name : 'u_login'})
            }
		}
        }
    }
</script>
