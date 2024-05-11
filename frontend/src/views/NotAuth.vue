<template>
    <div class="container py-4 py-xl-5">
        <div class="text-center">
            <h3 style="color: gray;">401 NOT AUTHORIZED</h3>
            <hr>
            <p><i>Please 
                <router-link :to="{name:'AdminLogin'}">Admin Login</router-link> | 
                <router-link :to="{name:'u_login'}">User Login</router-link> to access this page 
            </i></p>
        </div>
    </div>
</template>

<script>

export default {
    name:'NotAuth',
    
    // sessionStorage.removeItem('auth_token')
    // sessionStorage.removeItem('current_user')
    
}
</script>
