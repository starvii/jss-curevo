import VueRouter from 'vue-router'

const routes = [
    {
        path: '/',
        component: require('./component/Frame.vue'),
        children: [
            {
                path: '',
                component: require('./component/curevo/Index.vue'),
            },
            // {
            //     path: 'teacher/',
            //     component: require('./component/teacher/Index.vue'),
            // },
            // {
            //     path: 'class/natural/',
            //     component: require('./component/class/natural/Index.vue'),
            // },
            // {
            //     path: 'class/teaching/',
            //     component: require('./component/class/teaching/Index.vue'),
            // },
            // {
            //     path: 'course/',
            //     component: require('./component/course/Index.vue'),
            // },
            // {
            //     path: 'course/dependency/',
            //     component: require('./component/course/dependency/Index.vue'),
            // },
        ],
    },
    // {
    //     path: '/login/',
    //     component: require('./component/login/Index.vue'),
    // },
    // {
    //     path: '/logout/',
    //     component: require('./component/logout/Index.vue'),
    // },
    // {
    //     path: '/register/',
    //     component: require('./component/register/Index.vue'),
    // },
];

export default new VueRouter({routes});