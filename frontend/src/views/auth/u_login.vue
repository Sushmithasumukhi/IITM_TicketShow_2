 active<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#" style="font-size:x-large;">TicketShow</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <ul class="navbar-nav ml-auto mb-2 mb-lg-0">
            <li class="nav-item">
                <router-link class="nav-link active" :to="{ name: 'AdminLogin' }" style="font-size: large;">Admin</router-link>
            </li>
    
            <li class="nav-item">   
                <router-link :to="{ name:'u_SignUp'}" style="font-size: large;" class="nav-link active">User Sign Up</router-link>
            </li>
            </ul>
        </div>
        </nav>
        <section class="position-relative py-4 py-xl-5">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center mx-auto">
          <h3>Welcome User</h3>
          <h2 class="text-center">Login</h2>
          <p class="text-center">Fill this page to Login.</p>
          <div class="row d-flex justify-content-center">
            <div class="col-md-6">
            <div>
                <div class="my-4">
                    <img alt="User Image" class="rounded-circle flex-shrink-0 me-3" style="object-fit: cover" width="100" height="100" src="http://127.0.0.1:5000/static/img/default.png"/>
                </div>
                </div>
                <form @submit.prevent="LoginUser()">
                    <div v-if="error_msg !== ''">
                        <p style="font-size: 15px; color: red; font-style: italic;">{{ error_msg }}</p>
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="email" name="email" placeholder="Email" v-model="email" required/>                  
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="password" name="password" placeholder="Password" v-model="password" required/>
                    </div>
                    <div class="mb-3">
                    <button class="btn btn-primary d-block w-100" @click.prevent="LoginUser()">Login</button>
                    </div>
                    <div>
                    Create an account? <router-link :to="{ name:'u_SignUp'}">Sign Up</router-link>
                    </div>
                </form>
            </div>
        </div>
        
        </div>
        </div>
        </div>

  </section>
    </div>
</template>

<script>


 
export default {
    name: "u_login",
    data(){
        return {
            email: '',
            password: '',
            error_msg:''
        };
    },
    methods: {
        async LoginUser() {
            if(!this.email || !this.password){
                alert("Please fill all the fields")
                return;
            }
            
            
            const resp = await fetch('http://127.0.0.1:5000/login?include_auth_token',{
                method: 'POST',
                headers:{
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            })
            if (resp.status === 200){
                const data = await resp.json();
                const loginresp = await fetch('http://127.0.0.1:5000/user/login',{
                    method:'GET',
                    headers:{
                        'Authentication-Token': data.response.user.authentication_token,
                        'Content-Type':'application/json'
                    }
                })
                if (loginresp.status === 200){
                    const logindata = await loginresp.json()
                    
                    sessionStorage.current_user = logindata.current_user,
                    sessionStorage.auth_token = data.response.user.authentication_token
                    this.$router.push('/user/shows/all')
                }else if(loginresp.status === 403){
                    const error = await loginresp.json();
                    console.log(error)
                    this.error_msg = error.response.errors[0]
                }
            }else if(resp.status === 400){
                const error = await resp.json();
                this.error_msg = error.response.errors[0]
            }else{
                const error = await resp.json()
                console.log(error)
                alert('Somrthing went wrong')
            }
        }
    },
}
</script>
