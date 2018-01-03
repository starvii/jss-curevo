const state = {
    outSize: false,
};

const getters = {
    frame$isOutSize: state => {
        return state.outSize;
    },
};

const mutations = {
    frame$setOutSize(state, payload) {
        state.outSize = payload.outSize;
    },
};

const actions = {

};

export default {
    state,
    getters,
    actions,
    mutations
};