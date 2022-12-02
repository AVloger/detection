import Vue from 'vue'
import VueRouter from 'vue-router'
import store from "@/store";
import axios from 'axios';

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: () => import('../views/Manage.vue'),
        redirect: "/home",
        children: [
            {path: 'home', name: '首页', component: () => import('../views/Home.vue')},
            {path: 'user', name: '用户管理', component: () => import('../views/User.vue')},
            {path: 'person', name: '个人信息', component: () => import('../views/Person.vue')},
            {path: 'webcamera', name: '目标检测', component: () => import('../views/WebCamera.vue')},
            
        ]
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('../views/About.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
    localStorage.setItem("currentPathName", to.name)  // 设置当前的路由名称，为了在Header组件中去使用
    store.commit("setPath")  // 触发store的数据更新
    if (to.path === '/login' || to.path === '/register') { // 如果跳转登录页面,则移除token
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        next()
    } else {
        let token = localStorage.getItem('token');
        if (token === null || token === '') { //token不存在页跳转到登录页面
            router.replace({path:'/login'}).catch(err => { console.log(err) })
        } else {
            // 检验token是否正确
            axios({
                url: 'http://localhost:9090/user/checkToken', //在controller中写一个接口用来token校验
                method: 'get',
                //将token信息保存在header里
                headers: {
                    token: token
                }
            }).then((response) => {
                if (!response.data) {
                    console.log('检验失败')
                    router.replace({path:'/login'}).catch(err => { console.log(err) }) // 如果token失效,返回到登录页面
                }
            })
        }
    }
    next()  // 放行路由
})

export default router
