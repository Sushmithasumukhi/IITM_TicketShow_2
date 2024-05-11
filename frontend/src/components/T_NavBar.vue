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
                <router-link :to="{name : 'GetTheater'}" class="nav-link active">Theaters</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{name : 'CreateTheater'}" class="nav-link active">Add Theater</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{name : 'ShowCreate'}" class="nav-link active">Create Show</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{name : 'ShowGet'}" class="nav-link active">All Shows</router-link>
            </li>
            <li class="nav-item">
                <a class="nav-link active btn" @click="logoutadmin()">Logout</a>
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
        }
    },
    // props:{
    //     dropdown:{
    //         type: Boolean,
    //         required: true
    //     }
    // },
    methods: {
        async logoutadmin(){
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
    },
}
</script>
