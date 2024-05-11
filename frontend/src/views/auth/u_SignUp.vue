<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#" style="font-size:x-large;">TicketShow</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="true" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <router-link class="nav-link active" :to="{ name: 'AdminLogin' }" style="font-size: large;">Admin</router-link>
            </li>
    
            <li class="nav-item">
                <router-link class="nav-link active" :to="{ name: 'u_login' }" style="font-size: large;">User Login</router-link>
            </li>
            </ul>
        </div>
        </nav>
        <section class="position-relative py-4 py-xl-5">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center mx-auto">
          <h3>Welcome User</h3>
          <h2 class="text-center">Sign up</h2>
          <p class="text-center">Fill this page to create an account.</p>
          <div class="row d-flex justify-content-center">
            <div class="col-md-6">
            <div>
                <div class="my-4">
                    <img alt="User Image" class="rounded-circle flex-shrink-0 me-3" style="object-fit: cover" width="100" height="100" src="http://127.0.0.1:5000/static/img/default.png"/>
                </div>
                </div>
                <form @submit.prevent="registerUser()">
                    <div v-if="error_msg !==''">
                        <p style="font-size: 15px; color: red; font-style: italic;">{{ error_msg }}</p>
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="email" name="email" placeholder="Email" v-model="email" required/>
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="text" name="username" placeholder="Enter Username" v-model="username" required/>                       
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="password" name="password" placeholder="Password"  v-model="password"  required/>
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="password" name="password2" placeholder="Re-enter Password" v-model="password2" required/>
                    </div>
                    <div class="mb-3">
                    <button class="btn btn-primary d-block w-100" @click.prevent="registerUser()">Sign up</button>
                    </div>
                    <div>
                    Have an account? <router-link class="nav-link" :to="{ name: 'u_login' }">login</router-link>
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
    name: "u_SignUp",
    data(){
        return {
            username: "",
            password: "",
            password2: "",
            email: "",
            error_msg: ""
        };
    },
    methods: {
        async registerUser(){
            if(!this.username || !this.email || !this.password || !this.password2){
                alert("Please fill all the fields")
                return;
            }

            if (!this.email.includes("@")||!this.email.includes(".com")){
                alert("Invalid Email, Enter proper Email");
                return;
            }

            if (this.password != this.password2){
                alert("Re-enter Password!! Passwords dont match!!");
                return;
            }

            const resp = await fetch("http://127.0.0.1:5000/user/signup",{
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    password2: this.password2,
                })
            })
            if (resp.status === 200) {
                await resp.json()
                // alert("Signup Successful")
                this.$router.push('/user/login')
            } else {
                if(resp.status === 401){
                    const error = await resp.json()
                    console.log(error)
                    this.error_msg = error.resp.errors[0]
                }
                else if(resp.status === 409){
                    this.error_msg = 'email already exist'
                    return;                    
                }
                else {
                    alert("An error occured while registering the user, please try again later"); }
                const error = await resp.text()
                console.error(error)
                
            }
            }
        }    
    }   
</script>
