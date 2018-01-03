<template>
    <DialogFrame :show="show" :closeFunc="close" :dimmerFunc="close">
        <span slot="header">查看教师信息</span>
        <div class="ui form mini">
            <div class="three fields">
                <div class="field">
                    <label>编号</label>
                    <input placeholder="编号" type="text" readonly="readonly" v-model="entity['Code']">
                </div>
                <div class="field">
                    <label>姓名</label>
                    <input placeholder="姓名" type="text" readonly="readonly" v-model="entity['Name']">
                </div>
                <div class="field">
                    <label>电话</label>
                    <input placeholder="电话" type="text" readonly="readonly" v-model="entity['Phone']">
                </div>
            </div>
            <div class="three fields">
                <div class="field">
                    <label>单位</label>
                    <input placeholder="单位" type="text" readonly="readonly" v-model="entity['Unit']">
                </div>
                <div class="field">
                    <label>部门</label>
                    <input placeholder="部门" type="text" readonly="readonly" v-model="entity['Dept']">
                </div>
                <div class="field">
                    <label>邮箱</label>
                    <input placeholder="邮箱" type="text" readonly="readonly" v-model="entity['Email']">
                </div>
            </div>
            <div class="field">
                <label>备注</label>
                <textarea rows="3" style="resize: none;" placeholder="备注" readonly="readonly"
                          v-model="entity['Comment']"></textarea>
            </div>
        </div>
        <div slot="actions">
            <div class="ui green ok inverted button" @click="close()">
                <i class="checkmark icon"></i>
                关闭
            </div>
        </div>
    </DialogFrame>
</template>

<script>
    import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
    import DialogFrame from '../util/DialogFrame.vue'
    import * as store from './store'

    const vm = {
        computed: {
            ...mapGetters({
                show: 'teacher$viewDialogState',
                entity: 'teacher$viewEntity',
            }),
        },
        components: {
            DialogFrame
        },
        methods: {
            ...mapMutations({
                close: store.SHOW_LIST_WINDOW,
            }),
        },
    };

    export default vm;
</script>