<template>
    <div class="container margin10">
        <table class="ui celled table">
            <thead>
            <tr v-if="outSize">
                <th colspan="6">
                    <div class="to-center">
                        <Pagination :conf="conf"></Pagination>
                    </div>
                </th>
            </tr>
            <tr>
                <th>
                    <button class="ui labeled icon button orange" @click="create()">
                        <i class="plus icon white"></i>
                        新建
                    </button>
                </th>
                <th>编号</th>
                <th>姓名</th>
                <th>单位</th>
                <th>电话</th>
                <th>
                    <div class="ui search">
                        <div class="ui icon input">
                            <input class="prompt" placeholder="搜索" type="text" v-model="keyword"
                                   @keyup.enter="query()">
                            <i class="search link icon" @click="query()"></i>
                        </div>
                    </div>
                </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(item, index) in dataList">
                <td>
                    <a @click="view(item)" href="javascript:void(0);" title="详细"
                       v-text="(conf.currentPage - 1) * conf.itemsPerPage + index + 1"></a>
                </td>
                <td><a @click="view(item)" href="javascript:void(0);" v-text="item['Code']"></a></td>
                <td><a @click="view(item)" href="javascript:void(0);" v-text="item['Name']"></a></td>
                <td><a @click="view(item)" href="javascript:void(0);" v-text="item['Unit']"></a></td>
                <td><a @click="view(item)" href="javascript:void(0);" v-text="item['Phone']"></a></td>
                <td>
                    <a href="javascript:void(0);" title="修改" @click="modify(item)">
                        <i class="large write square icon"></i>
                    </a>
                    <a href="javascript:void(0);" title="删除" @click="remove(item)">
                        <i class="large trash icon"></i>
                    </a>
                </td>
            </tr>
            </tbody>
            <tfoot>
            <tr>
                <th colspan="6">
                    <div class="to-center">
                        <Pagination :conf="conf"></Pagination>
                    </div>
                </th>
            </tr>
            </tfoot>
        </table>
        <TeacherEdit></TeacherEdit>
        <TeacherView></TeacherView>
        <ConfirmDialog :params="removeConfirmParams"></ConfirmDialog>
        <MessageDialog :params="messageDialogParams"></MessageDialog>
    </div>
</template>

<style scoped>

</style>

<script>
    import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
    import Pagination from '../util/Pagination.vue'
    import Edit from './Edit.vue'
    import View from './View.vue'
    import ConfirmDialog from '../util/ConfirmDialog.vue'
    import MessageDialog from '../util/MessageDialog.vue'
    import * as store from './store'
    import * as api from './api'
    import '../../../css/style.css'

    let self = null;
    // 不知道为什么访问不到 this.$http 对象（但可以访问 window.Vue.http 对象），不得不出此下策。
    // 在 vm.created() 中将 this 保存至 self 中

    const vm = {
        data() {
            return {
                conf: {
                    currentPage: 1,
                    totalItems: 0,
                    itemsPerPage: 10,
                    refreshCount: 0,
                    uid: null,
                    async onChange(owner) {
                        if (this.uid === owner._uid) {
                            try {
                                let data = await api.query_entities(
                                    this.currentPage,
                                    this.itemsPerPage,
                                    self.keyword);
                                this.totalItems = data.count;
                                self.dataList = data.data;
                            }
                            catch (err) {
                                console.error(err);
                                self.showErrorDialog({
                                    title: '错误',
                                    message: '数据加载失败，请检查网络情况。',
                                });
                            }
                        }
                    }
                },
                keyword: '',
                dataList: [],
                removeConfirmParams: {
                    show: false,
                    title: '',
                    message: '',
                    confirmFunc: this.removeEntity,
                    params: [],
                },
                messageDialogParams: {
                    show: false,
                    title: '',
                    message: '',
                }
            };
        },
        created() {
            self = this;
            this.setFunctions({
                showErrorFunc: this.showError,
                refreshListFunc: this.refreshList,
            }); // 将显示错误信息弹窗的方法传入 store 中，方便其他组件统一调用
        },
        mounted() {
            this.refreshList();
        },
        computed: {
            ...mapGetters({
                errorDialogState: store.ERROR_DIALOG_STATUS,
                outSize: 'frame$isOutSize',
            }),

        },
        methods: {
            ...mapMutations({
                refresh: store.REFRESH_LIST,
                showErrorDialog: store.SHOW_ERROR_DIALOG,
                setFunctions: store.SET_FUNCTIONS,
            }),
            ...mapActions({
                showListWindow: store.SHOW_LIST_WINDOW,
                showEditDialog: store.SHOW_EDIT_DIALOG,
                showViewDialog: store.SHOW_VIEW_DIALOG,
                removeEntity: store.REMOVE_ENTITY,
            }),
            query() {
                this.refresh();
            },
            create() {
                this.showEditDialog({id: ''});
            },
            view(item) {
                this.showViewDialog({id: item['Id']});
            },
            modify(item) {
                this.showEditDialog({id: item['Id']});
            },
            remove(item) {
                this.removeConfirmParams.entity = item;
                this.removeConfirmParams.show = true;
            },
            refreshList() {
                this.conf.refreshCount++;
            },
            showError(content) {
                this.messageDialogParams.title = content.title;
                this.messageDialogParams.message = content.message;
                this.messageDialogParams.show = true;
            },
        },
        components: {
            Pagination,
            Edit,
            View,
            ConfirmDialog,
            MessageDialog,
        },
    };
    export default vm;
</script>
