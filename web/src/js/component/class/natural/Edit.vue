<template>
    <DialogFrame :show="show" :closeFunc="close">
        <span slot="header" v-text="header"></span>
        <div class="ui form mini">
            <div class="three fields">
                <div class="field">
                    <label>编号</label>
                    <input placeholder="编号" type="text" v-model="entity['Code']">
                </div>
                <div class="field">
                    <label>姓名</label>
                    <input placeholder="姓名" type="text" v-model="entity['Name']">
                </div>
                <div class="field">
                    <label>电话</label>
                    <input placeholder="电话" type="text" v-model="entity['Phone']">
                </div>
            </div>
            <div class="three fields">
                <div class="field">
                    <label>单位</label>
                    <input placeholder="单位" type="text" v-model="entity['Unit']">
                </div>
                <div class="field">
                    <label>部门</label>
                    <input placeholder="单位" type="text" v-model="entity['Dept']">
                </div>
                <div class="field">
                    <label>邮箱</label>
                    <input placeholder="邮箱" type="text" v-model="entity['Email']">
                </div>
            </div>
            <div class="field">
                <label>备注</label>
                <textarea rows="3" style="resize: none;" placeholder="备注"
                          v-model="entity['Comment']"></textarea>
            </div>
        </div>
        <div slot="actions">
            <div class="ui red cancel inverted button" @click="close()">
                <i class="remove icon"></i>
                取消
            </div>
            <div class="ui green ok inverted button" @click="closeAndSave()">
                <i class="checkmark icon"></i>
                保存
            </div>
        </div>
    </DialogFrame>
</template>

<script>
    import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
    import DialogFrame from '../util/DialogFrame.vue'
    import {SHOW_LIST_WINDOW, CREATE_ENTITY, MODIFY_ENTITY} from './state.js'

    let lastShowState = false;

    const TeacherEdit = {
        data() {
            return {
                entity: {},
                header: '',
                mode: 0,
            };
        },
        computed: {
            ...mapGetters({
                showState: 'teacher$editDialogState',
                editEntity: 'teacher$editEntity',
            }),
            show() {
                // show 变化时
                if (lastShowState !== this.showState) {
                    lastShowState = this.showState;
                    if (this.showState) { // show为真，显示弹窗时
                        this.entity = this.editEntity;
                        if ('undefined' === typeof(this.entity['Id']) || this.entity['Id'].length === 0) {
                            this.header = '新建教师信息';
                            this.mode = 0;
                        }
                        else {
                            this.header = '修改教师信息';
                            this.mode = 1;
                        }
                    }
                }
                return this.showState;
            },
        },
        components: {
            DialogFrame,
        },
        methods: {
            ...mapMutations({
                showListWindow: SHOW_LIST_WINDOW,
            }),
            ...mapActions({
                createEntity: CREATE_ENTITY,
                modifyEntity: MODIFY_ENTITY,
            }),
            close() {
                this.showListWindow();
            },
            closeAndSave() {
                if (this.mode === 0) {
                    this.createEntity({entity: this.entity});
                }
                else {
                    this.modifyEntity({entity: this.entity});
                }
            },
        },
    };

    export default TeacherEdit;
</script>