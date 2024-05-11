import { createRouter, createWebHistory } from 'vue-router'

import u_SignUp from '../views/auth/u_SignUp.vue';
import AdminLogin from '../views/auth/AdminLogin.vue';
import u_login from '../views/auth/u_login.vue';
import NotAuth from '../views/NotAuth.vue';
import NotFound from '../views/NotFound.vue';

import CreateTheater from '../views/theater/CreateTheater.vue';
import GetTheater from '../views/theater/GetTheater.vue';
import UpdateTheater from '../views/theater/UpdateTheater.vue';
import AddShow from '../views/theater/AddShow.vue';
import ViewShow from '../views/theater/ViewShow.vue';

import ShowCreate from '../views/shows/ShowCreate.vue';
import ShowGet from '../views/shows/ShowGet.vue';
import S_Details from '../views/shows/S_Details.vue';
import ShowUpdate from '../views/shows/ShowUpdate.vue';

import User_show from '../views/user/User_show.vue';
import user_show_detail from '../views/user/user_show_detail.vue';
import booking_details from '../views/user/booking_details.vue';
import show_search from '../views/user/show_search.vue';
import theater_search from '../views/user/theater_search.vue';
import theater_details from '../views/user/theater_details.vue';
import user_profile from '../views/user/user_profile.vue';



const routes = [
  {
    path: '/',
    name: 'u_SignUp',
    component: u_SignUp
  },
  {
    path: '/user/login',
    name: 'u_login',
    component: u_login
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/admin/theater/create',
    name: 'CreateTheater',
    component: CreateTheater,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/theater',
    name: 'GetTheater',
    component: GetTheater,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/theater/update/:id',
    name: 'UpdateTheater',
    component: UpdateTheater,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/theater/show/:id',
    name: 'AddShow',
    component: AddShow,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/theater/:id',
    name: 'ViewShow',
    component: ViewShow,
    meta:{
      requiresAdmin: true
    }
  },

  {
    path: '/admin/show/all',
    name: 'ShowGet',
    component: ShowGet,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/show/:id',
    name: 'S_Details',
    component: S_Details,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/show/upload',
    name: 'ShowCreate',
    component: ShowCreate,
    meta:{
      requiresAdmin: true
    }
  },
  {
    path: '/admin/show/update/:id',
    name: 'ShowUpdate',
    component: ShowUpdate,
    meta:{
      requiresAdmin: true
    }
  },

  {
    path: '/user/shows/all',
    name: 'User_show',
    component: User_show,
  },
  {
    path: '/user/show/:id',
    name: 'user_show_detail',
    component: user_show_detail,
  },
  {
    path: '/user/:user_id/booking/details',
    name: 'booking_details',
    component: booking_details,
  },
  {
    path: '/user/shows/search',
    name: 'show_search',
    component: show_search,
  },
  {
    path: '/user/theaters/search',
    name: 'theater_search',
    component: theater_search,
  },
  {
    path: '/user/theater/:id',
    name: 'theater_details',
    component: theater_details,
  },
  {
    path: '/user/:id/profile',
    name: 'user_profile',
    component: user_profile,
  },




  // ERROR PAGES
  {
    path: '/not-authorized',
    name: 'NotAuth',
    component: NotAuth
  },
  {
    path: '/not-found',
    name: 'NotFound',
    component: NotFound
  },
  {
    path: '/:catchAll(.*)',  //custom regex expression catchAll param 
    name: 'NotFound',
    component: NotFound
  },
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
// let routecount = 0;
router.beforeEach(async(to, from, next) => {
  // routecount++;
  // console.log(`beforeEachCallCount-(${routecount})`)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);


  if(requiresAdmin){
    const auth_token = sessionStorage.getItem('auth_token');
    if(auth_token){
      try{
        const response = await fetch('http://127.0.0.1:5000/auth-admin',{
          method: 'GET',
          headers:{
          'Authentication-Token': auth_token
          }
      });
      if(response.status===200){
        next();
      }else{
        next('/not-authorized');
      }
      }catch(error){
        console.log(error);
        next('/not-authorized');
      }
    }else{
      next('/not-authorized');
    }
  }
  next();
});


export default router
