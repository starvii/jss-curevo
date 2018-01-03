import './const'
import router from './router'
import store from './vuex/index'
import Index from './Index.vue'

window.vue = new Vue({
    el: '#application',
    render: h => h(Index),
    router: router,
    store: store,
});
