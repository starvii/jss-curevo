import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import Vuex from 'vuex'

Vue.use(Vuex);
Vue.use(VueResource);
Vue.use(VueRouter);

window.Vue = Vue;

Vue.http.options.emulateJSON = false;
Vue.http.options.emulateHTTP = true;

Vue.http.headers.common['Content-Type'] = 'application/json; charset=utf-8';


export const debug = process.env.NODE_ENV !== 'production';