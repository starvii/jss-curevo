import Vuex from 'vuex'
import {debug} from '../const'
import frame from '../component/store'
import teacher from '../component/teacher/store'
import natural from '../component/class/natural/store'

const store = new Vuex.Store({
    modules: {
        frame,
        teacher,
        natural,
    },
    strict: debug,
});

export default store;

