<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#" style="font-size:x-large;">TicketShow</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <router-link class="nav-link active" :to="{ name:'u_login'}" style="font-size: large;">User Login</router-link>
            </li>
            </ul>
        </div>
        </nav>
        <section class="position-relative py-4 py-xl-5">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center mx-auto">
          <h3>Welcome Admin</h3>
          <h2 class="text-center">Login</h2>
          <p class="text-center">Fill this page to Login.</p>
          <div class="row d-flex justify-content-center">
            <div class="col-md-6">
            <div>
                <div class="my-4">
                    <img alt="User Image" class="rounded-circle flex-shrink-0 me-3" style="object-fit: cover" width="100" height="100" src="http://127.0.0.1:5000/static/img/admin.png"/>
            </div>
                </div>
                <form @submit.prevent="LoginAdmin()">
                    <div v-if="error_msg !== ''">
                        <p style="font-size: 15px; color: red; font-style: italic;">{{ error_msg }}</p>
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="email" name="email" placeholder="Admin email" v-model="email" required/>
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="password" name="password" placeholder="password" v-model="password" required/>
                    </div>
                    <div class="mb-3">
                    <button class="btn btn-primary d-block w-100" @click.prevent="LoginAdmin()">Login</button>
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
    name: "AdminLogin",
    data(){
        return {
            email: "",
            password: "",

            error_msg:""
        };
    },
    methods: {
        async LoginAdmin() {
            if(!this.email || !this.password){
                alert("Please fill all the fields")
                return;
            }
            
           const response =  await fetch('http://127.0.0.1:5000/login?include_auth_token',{
                method: 'POST',
                headers:{
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            })
            if (response.ok){
                const data =  await response.json()
                const dummyresp = await fetch('http://127.0.0.1:5000/auth-admin',{
                    method: 'GET',
                    headers:{
                    'Authentication-Token': data.response.user.authentication_token,
                    'Content-Type':'application/json'
                    }
                })
                if (dummyresp.status===200){
                    const dd = await dummyresp.json()
                    sessionStorage.current_user = dd.current_user,
                    sessionStorage.auth_token = data.response.user.authentication_token,
                    // console.log(data)
                    this.$router.push('/admin/show/all')
                }else if(dummyresp.status === 403){
                    const error = await dummyresp.json()
                    this.error_msg = error.response.errors[0]
                }
                
            }else if(response.status === 400 ){
                    const error = await response.json()
                    this.error_msg = error.response.errors[0]
                }else{
                    const error = await response.json()
                    console.log(error)
                    alert('Somrthing went wrong')
                }
        }
    },
}
</script>
