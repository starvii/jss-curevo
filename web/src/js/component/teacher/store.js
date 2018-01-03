import jQuery from 'jquery'
import * as types from '../../vuex/types'
import * as dao from './api'

export const MOD_PREFIX = 'teacher$'; // 除了 state 之外，其他 getters, mutations, actions 都是全局共享的，所以必须加上命名空间
export const SHOW_EDIT_DIALOG = MOD_PREFIX + types.SHOW_EDIT_DIALOG;
export const SHOW_VIEW_DIALOG = MOD_PREFIX + types.SHOW_VIEW_DIALOG;
export const SHOW_LIST_WINDOW = MOD_PREFIX + types.SHOW_LIST_WINDOW;
export const SHOW_ERROR_DIALOG = MOD_PREFIX + types.SHOW_ERROR_DIALOG;
export const REFRESH_LIST = MOD_PREFIX + types.REFRESH_LIST;
export const SET_FUNCTIONS = MOD_PREFIX + types.SET_FUNCTIONS;

export const CREATE_ENTITY = MOD_PREFIX + types.CREATE_ENTITY;
export const MODIFY_ENTITY = MOD_PREFIX + types.MODIFY_ENTITY;
export const REMOVE_ENTITY = MOD_PREFIX + types.REMOVE_ENTITY;


export const EDIT_DIALOG_STATUS = MOD_PREFIX + types.EDIT_DIALOG_STATUS;
export const VIEW_DIALOG_STATUS = MOD_PREFIX + types.VIEW_DIALOG_STATUS;
export const ERROR_DIALOG_STATUS = MOD_PREFIX + types.ERROR_DIALOG_STATUS;

export const EDIT_ENTITY = MOD_PREFIX + types.EDIT_ENTITY;
export const VIEW_ENTITY = MOD_PREFIX + types.VIEW_ENTITY;

const state = {
    mode: 0,
    entity: {
        edit: {},
        view: {},
    },
    // 以后设计原则就是，把需要在 store 中调用的函数传进来
    refreshListFunc: null,
    showErrorFunc: null,
};

const getters = {
    [EDIT_DIALOG_STATUS]: state => {
        return state.mode === 1;
    },
    [VIEW_DIALOG_STATUS]: state => {
        return state.mode === 2;
    },
    [ERROR_DIALOG_STATUS]: state => {
        return state.mode === 3;
    },
    [EDIT_ENTITY]: state => {
        return jQuery.extend(true, {}, state.entity.edit); // deep copy
    },
    [VIEW_ENTITY]: state => {
        return state.entity.view;
    },
};

const mutations = {
    [SHOW_LIST_WINDOW] (state) {
        state.mode = 0;
    },
    [SHOW_EDIT_DIALOG] (state, payload) {
        state.entity.edit = payload.entity;
        state.mode = 1;
    },
    [SHOW_VIEW_DIALOG] (state, payload) {
        state.entity.view = payload.entity;
        state.mode = 2;
    },
    [SHOW_ERROR_DIALOG] (state, payload) {
        state.showErrorFunc(payload);
    },
    [REFRESH_LIST] (state) {
        state.refreshListFunc();
    },
    [SET_FUNCTIONS] (state, payload) {
        state.showErrorFunc = payload.showErrorFunc;
        state.refreshListFunc = payload.refreshListFunc;
    }
};

const actions = {
    async [CREATE_ENTITY] ({commit}, payload) {
        if ('undefined' !== typeof(payload) && 'undefined' !== typeof(payload.entity)) {
            const entity = payload.entity;
            try {
                let result = await dao.create_entity(entity);
                if (result === 'success') {
                    commit(REFRESH_LIST);
                }
                else {
                    commit(SHOW_ERROR_DIALOG, {
                        title: '错误',
                        message: '数据写入失败，请联系系统管理员。',
                    });
                }
            }
            catch (err) {
                console.error(err);
                commit(SHOW_ERROR_DIALOG, {
                    title: '错误',
                    message: '连接后台服务器失败，请检查网络情况。',
                });
            }
        }
        commit(SHOW_LIST_WINDOW);
    },
    async [MODIFY_ENTITY] ({commit}, payload) {
        if ('undefined' !== typeof(payload) && 'undefined' !== typeof(payload.entity)) {
            const entity = payload.entity;
            try {
                let result = await dao.modify_entity(entity);
                if (result === 'success') {
                    commit(REFRESH_LIST);
                }
                else {
                    commit(SHOW_ERROR_DIALOG, {
                        title: '错误',
                        message: '数据写入失败，请联系系统管理员。',
                    });
                }
            }
            catch (err) {
                console.error(err);
                commit(SHOW_ERROR_DIALOG, {
                    title: '错误',
                    message: '连接后台服务器失败，请检查网络情况。',
                });
            }
        }
        commit(SHOW_LIST_WINDOW);
    },
    async [REMOVE_ENTITY] ({commit}, payload) {
        if ('undefined' !== typeof(payload) && 'undefined' !== typeof(payload.entity)) {
            const entity = payload.entity;
            try {
                let result = await dao.remove_entity(entity);
                if (result === 'success') {
                    commit(REFRESH_LIST);
                }
                else {
                    commit(SHOW_ERROR_DIALOG, {
                        title: '错误',
                        message: '数据删除失败，请联系系统管理员。',
                    });
                }
            }
            catch (err) {
                console.error(err);
                commit(SHOW_ERROR_DIALOG, {
                    title: '错误',
                    message: '连接后台服务器失败，请检查网络情况。',
                });
            }
        }
    },
    async [SHOW_EDIT_DIALOG] ({commit}, payload) {
        if (undefined === payload || undefined === payload.id || payload.id.length === 0) {
            commit(SHOW_EDIT_DIALOG, {entity: {}});
        }
        else {
            const id = payload.id;
            try {
                let entity = await dao.query_entity(id);
                commit(SHOW_EDIT_DIALOG, {entity});
            }
            catch (err) {
                console.error(err);
                commit(SHOW_ERROR_DIALOG, {
                    title: '错误',
                    message: '数据加载失败，请检查网络情况。',
                });
            }
        }
    },
    async [SHOW_VIEW_DIALOG] ({commit}, payload) {
        if (undefined === payload || undefined === payload.id || payload.id.length === 0) {
            // do nothing
            console.error('There is no id in payload.');
        }
        else {
            const id = payload.id;
            try {
                let entity = await dao.query_entity(id);
                commit(SHOW_VIEW_DIALOG, {entity});
            }
            catch (err) {
                console.error(err);
                commit(SHOW_ERROR_DIALOG, {
                    title: '错误',
                    message: '数据加载失败，请检查网络情况。',
                });
            }
        }
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};